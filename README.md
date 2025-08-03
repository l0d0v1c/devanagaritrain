# Entraînement à l'écriture du Devanagari 🇮🇳

Application web interactive pour apprendre à écrire les lettres de l'alphabet devanagari (Sanskrit/Hindi).

## 🌐 Accès direct

**Utilisez l'application en ligne :** https://l0d0v1c.github.io/devanagaritrain/

**Code source :** https://github.com/l0d0v1c/devanagaritrain

## 🎯 Fonctionnalités

### Interface principale
- **Sélection par groupes** : Voyelles, consonnes palatales, cérébrales, dentales, labiales, ou toutes
- **Canvas de dessin** tactile et souris pour dessiner les lettres
- **Score en temps réel** pendant le tracé (0-100%)
- **Comparaison intelligente** avec algorithme d'alignement et normalisation

### Système d'apprentissage adaptatif
- **Fréquence intelligente** : les lettres mal maîtrisées reviennent plus souvent
- **Auto-évaluation** : classement OK/NOK qui influence la fréquence
- **Statistiques** : suivi du nombre de lettres pratiquées et taux de réussite

### Interface intuitive
- **Bascule de lettre** : cliquez sur la lettre latine pour voir le devanagari ⇄
- **Design responsive** : optimisé pour smartphone et tablette
- **Feedback visuel** : couleurs et animations pour une meilleure expérience

## 🚀 Utilisation

### Démarrage rapide
1. Ouvrez `index.html` dans votre navigateur
2. Choisissez un groupe de lettres (ou "Toutes")
3. Dessinez la lettre affichée sur le canvas
4. Regardez votre score en temps réel
5. Cliquez sur "Analyser" pour une comparaison détaillée
6. Évaluez votre dessin (OK/NOK) pour améliorer l'apprentissage

### Contrôles
- **Lettre à dessiner** : Cliquez sur la lettre pour basculer latin ↔ devanagari ⇄
- **Canvas** : Dessinez avec la souris ou le doigt
- **Effacer** : Nettoie le canvas
- **Analyser** : Compare votre dessin avec la référence
- **Suivant** : Passe à la lettre suivante

### Groupes de lettres disponibles

#### Voyelles (8 lettres)
- a (अ), ā (आ), i (इ), ī (ई)
- u (उ), ū (ऊ), e (ए), o (ओ)

#### Consonnes palatales (5 lettres)
- ca (च), cha (छ), ja (ज), jha (झ), ña (ञ)

#### Consonnes cérébrales (5 lettres)
- ṭa (ट), ṭha (ठ), ḍa (ḍha (ढ), ṇa (ण)

#### Consonnes dentales (5 lettres)
- ta (त), tha (थ), da (द), dha (ध), na (न)

#### Consonnes labiales (5 lettres)
- pa (प), pha (फ), ba (ब), bha (भ), ma (म)

#### Autres consonnes (7 lettres)
- ya (य), ra (र), la (ल), va (व)
- śa (श), sa (स), ha (ह)

## 🔧 Algorithme de comparaison

### Technologie utilisée
L'application utilise un algorithme avancé de **computer vision** en JavaScript :

1. **Détection de bounding box** : Trouve les limites du dessin
2. **Normalisation** : Redimensionne et centre les images à 80x80px
3. **Alignement** : Compare les formes réelles, pas les positions
4. **Métriques multiples** :
   - **IoU** (Intersection over Union) - 60% du score
   - **F1-score** (précision + rappel) - 40% du score
5. **Tolérance d'épaisseur** : Accepte les variations de trait
6. **Bonus intelligents** : Récompense les bonnes proportions et la complexité

### Interprétation des scores
- **80-100%** : Excellent, très proche de la référence
- **60-79%** : Bien, forme reconnaissable  
- **40-59%** : Correct, à améliorer
- **25-39%** : Effort visible mais imprécis
- **0-24%** : À retravailler

## 📱 Compatibilité

### Navigateurs supportés
- Chrome/Chromium 80+
- Firefox 75+
- Safari 13+
- Edge 80+

### Appareils
- **Desktop** : Souris pour dessiner
- **Tablette/Smartphone** : Interface tactile optimisée
- **Responsive** : S'adapte automatiquement à la taille d'écran

## 🎨 Fonctionnalités techniques

### Interface responsive
- Layout flexible : colonnes sur desktop, pile sur mobile
- Canvas adaptatif : 300x300px → 280x280px sur mobile
- Boutons tactiles optimisés
- Police Devanagari : Google Fonts "Noto Sans Devanagari"

### Score en temps réel
- Calcul automatique 300ms après chaque trait
- Couleurs dynamiques selon le score
- Performance optimisée pour éviter les ralentissements

### Visualisation de comparaison
- Images alignées côte à côte
- Superposition colorée des différences
- Canvas de référence vs dessin utilisateur

## 📚 Apprentissage du Devanagari

### Conseils d'utilisation
1. **Commencez par les voyelles** : plus simples pour débuter
2. **Observez bien la référence** avant de dessiner
3. **Pratiquez régulièrement** : l'algorithme adaptatif favorise la répétition
4. **Utilisez le score temps réel** pour corriger pendant le tracé
5. **Soyez honnête dans l'auto-évaluation** pour un apprentissage optimal

### Progression recommandée
1. **Voyelles** (a, ā, i, ī, u, ū, e, o)
2. **Consonnes simples** (ka, ga, ca, ja, ta, da, pa, ba, ma)
3. **Consonnes complexes** (ṭa, ṭha, ḍa, ḍha, ṇa)
4. **Consonnes rares** (ña, śa, sa, ha)

## 🔄 Algorithme adaptatif

### Système de fréquence
- **Score OK** → Fréquence × 0.8 (apparaît moins souvent)
- **Score NOK** → Fréquence × 1.5 (apparaît plus souvent)
- **Minimum** : 0.1 (ne disparaît jamais complètement)
- **Maximum** : 3.0 (plafonné pour éviter la sur-répétition)

### Auto-évaluation intelligente
- Score ≥ 45% → Automatiquement "OK"
- Score < 45% → Automatiquement "NOK"
- Possibilité de corriger manuellement

## 📁 Structure du projet

```
devanagaritrain/
├── index.html          # Application principale (tout-en-un)
└── README.md           # Documentation
```

### Application autonome
L'application est entièrement contenue dans un seul fichier `index.html` :
- ✅ HTML structure
- ✅ CSS responsive
- ✅ JavaScript avec algorithmes de computer vision
- ✅ Données des 35 lettres devanagari intégrées
- ✅ Aucune dépendance externe (sauf Google Fonts)
- ✅ Fonctionne hors ligne après premier chargement

## 🌐 Déploiement

### GitHub Pages
1. Fork le repository : https://github.com/l0d0v1c/devanagaritrain
2. Activer GitHub Pages dans Settings > Pages
3. L'application sera accessible à `https://votre-username.github.io/devanagaritrain/`

**Version officielle :** https://l0d0v1c.github.io/devanagaritrain/

### Installation locale
```bash
# Cloner le repository
git clone https://github.com/l0d0v1c/devanagaritrain.git
cd devanagaritrain

# Serveur local (optionnel)
python -m http.server 8000
# ou
npx serve .

# Ou simplement ouvrir index.html dans le navigateur
open index.html
```

## 🤝 Contribution

Améliorations possibles :
- Ajout de lettres composées (ligatures)
- Mode d'entraînement par mots
- Sauvegarde des progrès en localStorage
- Modes de difficulté (débutant/expert)
- Support audio pour la prononciation

## 📄 Licence

Projet open-source - libre d'utilisation pour l'apprentissage et l'éducation.

---

**Bon apprentissage du Devanagari ! 🙏 नमस्ते**