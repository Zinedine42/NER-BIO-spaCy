# NER-BIO-spaCy
Extraction des Entités Nommées (NER) au format BIO à l’aide de spaCy, en comparant différentes versions du texte. 🚀📖
# NER-BIO-spaCy — Projet de Reconnaissance d'Entités Nommées

Ce projet a pour objectif d'extraire, comparer et analyser des entités nommées (REN) dans des textes OCRisés à l'aide de **spaCy**. Il inclut la création de plusieurs graphiques illustrant la qualité de la reconnaissance selon les versions de texte.

## Structure du projet

```
NER-OUTPUT/          # Fichiers JSON de REN
POS-OUTPUT/          # Fichiers JSON de POS-tagging
comparison_charts/   # Graphiques de comparaison VP/FP/FN
label_distribution/  # Camemberts par type d'entité (PER, LOC...)
pos_ner_overlap/     # Graphique POS vs REN
venn_results/         # Diagrammes de Venn REN vs PROPN
scripts/              # Tous les scripts Python
README.md            # Ce fichier
```

## Scripts principaux

Tous les scripts peuvent être lancés avec `python3 nom_du_script.py`

| Script                        | Rôle                                                                 |
|------------------------------|----------------------------------------------------------------------|
| `ner_extraction_spacy.py`    | Applique la REN (spaCy) et génère les fichiers JSON format BIO    |
| `pos_tagging_spacy.py`       | Applique le POS-tagging spaCy sur les textes                        |
| `graph_labels.py`            | Crée un camembert par version de texte selon les catégories REN   |
| `graph_vp_fp.py`             | Compare Kraken vs Tesseract avec VP / FP / FN                      |
| `graph_posner.py`            | Affiche les proportions de POS reconnus comme entités              |
| `graphs_Venn.py`             | Génère un diagramme de Venn par texte entre PROPN et REN          |

## Graphiques produits

### 1. Distribution des entités par catégorie (PER, LOC, ORG, MISC)
-  `label_distribution/`
- Affiche un camembert par version (REF, Kraken, Tesseract)

### 2. Comparaison VP / FP / FN entre Kraken et Tesseract
-  `comparison_charts/vp_fp_fn_barplot.png`
- Barplot global des performances OCR

### 3. Diagrammes de Venn PROPN vs REN
-  `venn_results/`
- Un Venn par texte pour visualiser les mots à la fois PROPN et entités nommées

### 4. Proportion de POS reconnus comme entités
-  `pos_ner_overlap/pos_entity_overlap.png`
- Barplot des catégories grammaticales les plus croisées avec la REN

##  Auteurs
Ce projet a été réalisé par Isabelle M'LANAO AMADI et Zinedine HAMADI dans le cadre d'un travail universitaire 🧠📘
