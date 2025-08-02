#!/usr/bin/env python3
"""
Script pour générer des données d'entraînement pour la reconnaissance de lettres devanagari
"""

import cv2
import numpy as np
import json
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.patches as patches
from PIL import Image, ImageDraw, ImageFont
import math

def hu_moments(contour):
    """Calcule les moments de Hu pour un contour"""
    moments = cv2.moments(contour)
    hu = cv2.HuMoments(moments).flatten()
    # Log transform pour normaliser
    return -np.sign(hu) * np.log10(np.abs(hu) + 1e-10)

def shape_features(contour, image_shape):
    """Extrait des caractéristiques de forme d'un contour"""
    if len(contour) < 5:
        return [0] * 10
    
    # Aire et périmètre
    area = cv2.contourArea(contour)
    perimeter = cv2.arcLength(contour, True)
    
    # Compacité
    compactness = 4 * math.pi * area / (perimeter * perimeter) if perimeter > 0 else 0
    
    # Rectangle englobant
    x, y, w, h = cv2.boundingRect(contour)
    aspect_ratio = w / h if h > 0 else 1
    extent = area / (w * h) if w * h > 0 else 0
    
    # Solidity (ratio aire/aire enveloppe convexe)
    hull = cv2.convexHull(contour)
    hull_area = cv2.contourArea(hull)
    solidity = area / hull_area if hull_area > 0 else 0
    
    # Position relative
    center_x = (x + w/2) / image_shape[1]
    center_y = (y + h/2) / image_shape[0]
    
    # Densité
    total_pixels = image_shape[0] * image_shape[1]
    density = area / total_pixels
    
    return [
        area, perimeter, compactness, aspect_ratio, extent,
        solidity, center_x, center_y, density, len(contour)
    ]

def extract_features(image_path):
    """Extrait les caractéristiques d'une image de lettre"""
    # Charger l'image
    img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None
    
    # Binarisation
    _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
    
    # Trouver les contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return [0] * 17  # 7 moments de Hu + 10 caractéristiques de forme
    
    # Prendre le plus grand contour
    main_contour = max(contours, key=cv2.contourArea)
    
    # Extraire les caractéristiques
    hu = hu_moments(main_contour)
    shape = shape_features(main_contour, img.shape)
    
    return list(hu) + shape

def generate_synthetic_devanagari():
    """Génère des images synthétiques de lettres devanagari"""
    # Lettres devanagari de base
    letters = {
        'a': 'अ', 'aa': 'आ', 'i': 'इ', 'ii': 'ई', 'u': 'उ', 'uu': 'ऊ',
        'e': 'ए', 'o': 'ओ', 'ka': 'क', 'kha': 'ख', 'ga': 'ग', 'gha': 'घ',
        'ca': 'च', 'cha': 'छ', 'ja': 'ज', 'jha': 'झ', 'ta': 'त', 'tha': 'थ',
        'da': 'द', 'dha': 'ध', 'na': 'न', 'pa': 'प', 'pha': 'फ', 'ba': 'ब',
        'bha': 'भ', 'ma': 'म', 'ya': 'य', 'ra': 'र', 'la': 'ल', 'va': 'व',
        'sa': 'स', 'ha': 'ह'
    }
    
    training_data = []
    
    try:
        # Essayer de charger une police Devanagari
        font_size = 72
        try:
            font = ImageFont.truetype("NotoSansDevanagari-Regular.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Arial Unicode MS.ttf", font_size)
            except:
                print("Police Devanagari non trouvée, utilisation de la police par défaut")
                font = ImageFont.load_default()
        
        for letter_name, letter_char in letters.items():
            print(f"Génération de données pour {letter_name} ({letter_char})")
            
            # Image de référence parfaite
            img = Image.new('RGB', (200, 200), 'white')
            draw = ImageDraw.Draw(img)
            
            # Centrer le texte
            bbox = draw.textbbox((0, 0), letter_char, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (200 - text_width) // 2
            y = (200 - text_height) // 2
            
            draw.text((x, y), letter_char, fill='black', font=font)
            
            # Sauvegarder temporairement
            temp_path = f"temp_{letter_name}.png"
            img.save(temp_path)
            
            # Extraire les caractéristiques
            features = extract_features(temp_path)
            if features:
                training_data.append({
                    'letter': letter_name,
                    'features': features,
                    'score': 100  # Score parfait pour la référence
                })
                
                # Générer des variations dégradées
                for score in [80, 60, 40, 20]:
                    degraded_features = add_noise_to_features(features, (100 - score) / 100)
                    training_data.append({
                        'letter': letter_name,
                        'features': degraded_features,
                        'score': score
                    })
            
            # Nettoyer
            Path(temp_path).unlink(missing_ok=True)
            
    except Exception as e:
        print(f"Erreur lors de la génération: {e}")
    
    # Ajouter des exemples de formes incorrectes
    incorrect_shapes = generate_incorrect_shapes()
    training_data.extend(incorrect_shapes)
    
    return training_data

def add_noise_to_features(features, noise_level):
    """Ajoute du bruit aux caractéristiques pour simuler des dessins imparfaits"""
    noisy_features = []
    for feat in features:
        # Ajouter du bruit gaussien
        noise = np.random.normal(0, noise_level * abs(feat * 0.2))
        noisy_features.append(feat + noise)
    return noisy_features

def generate_incorrect_shapes():
    """Génère des exemples de formes incorrectes (croix, cercles, etc.)"""
    incorrect_data = []
    
    # Croix
    for i in range(5):
        features = [
            -1.5, -2.0, -1.8, -2.5, -3.0, -2.2, -1.9,  # Moments de Hu typiques d'une croix
            100, 50, 0.3, 1.0, 0.6, 0.8, 0.5, 0.5, 0.02, 20  # Caractéristiques de forme
        ]
        # Ajouter du bruit
        features = add_noise_to_features(features, 0.1)
        incorrect_data.append({
            'letter': 'incorrect',
            'features': features,
            'score': np.random.randint(5, 25)  # Score très bas
        })
    
    # Cercles
    for i in range(5):
        features = [
            -1.8, -3.2, -2.5, -3.8, -4.0, -3.5, -2.8,  # Moments de Hu typiques d'un cercle
            80, 40, 0.8, 1.0, 0.7, 0.9, 0.5, 0.5, 0.015, 30
        ]
        features = add_noise_to_features(features, 0.1)
        incorrect_data.append({
            'letter': 'incorrect',
            'features': features,
            'score': np.random.randint(5, 25)
        })
    
    # Lignes
    for i in range(5):
        features = [
            -1.2, -1.8, -1.5, -2.0, -2.5, -1.9, -1.6,  # Moments de Hu typiques d'une ligne
            40, 80, 0.1, 0.1, 0.3, 0.4, 0.5, 0.5, 0.008, 15
        ]
        features = add_noise_to_features(features, 0.1)
        incorrect_data.append({
            'letter': 'incorrect',
            'features': features,
            'score': np.random.randint(5, 20)
        })
    
    return incorrect_data

def main():
    """Fonction principale"""
    print("Génération des données d'entraînement...")
    
    # Générer les données
    training_data = generate_synthetic_devanagari()
    
    print(f"Généré {len(training_data)} échantillons")
    
    # Sauvegarder
    output_file = "devanagari_training_data.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(training_data, f, indent=2, ensure_ascii=False)
    
    print(f"Données sauvegardées dans {output_file}")
    
    # Statistiques
    letters = set(item['letter'] for item in training_data)
    print(f"Lettres incluses: {letters}")
    scores = [item['score'] for item in training_data]
    print(f"Scores: min={min(scores)}, max={max(scores)}, moyenne={sum(scores)/len(scores):.1f}")

if __name__ == "__main__":
    main()