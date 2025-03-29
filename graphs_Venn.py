import os
import json
from matplotlib_venn import venn2
import matplotlib.pyplot as plt

# Dossiers de base
NER_DIR = "NER-OUTPUT"
POS_DIR = "POS-OUTPUT"
OUTPUT_DIR = "venn_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Fonction pour extraire les mots d’un fichier NER
def extract_ner_words(ner_path):
    with open(ner_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return {ent["word"].lower() for ent in data.get("entities", [])}

# Fonction pour extraire les mots PROPN d’un fichier POS
def extract_pos_words(pos_path):
    with open(pos_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return {token["text"].lower() for token in data if token.get("pos") == "PROPN"}

# Fonction pour parcourir tous les fichiers POS et retrouver leur équivalent NER
for root, _, files in os.walk(POS_DIR):
    for file in files:
        if file.endswith("_PROPN.json"):
            pos_path = os.path.join(root, file)
            base_name = file.replace("_PROPN.json", ".json")

            # Rechercher le fichier NER correspondant dans NER-OUTPUT
            ner_match = None
            for ner_root, _, ner_files in os.walk(NER_DIR):
                if base_name in ner_files:
                    ner_match = os.path.join(ner_root, base_name)
                    break

            if ner_match:
                ner_words = extract_ner_words(ner_match)
                pos_words = extract_pos_words(pos_path)

                # Créer le diagramme de Venn
                plt.figure(figsize=(6,6))
                venn2([ner_words, pos_words], set_labels=("Entités Nommées", "PROPN"))
                plt.title(base_name.replace(".json", ""))

                # Sauvegarde du graphique
                save_name = base_name.replace(".json", ".png")
                save_path = os.path.join(OUTPUT_DIR, save_name)
                plt.savefig(save_path)
                plt.close()

                print(f"Diagramme enregistré : {save_path}")
            else:
                print(f"Fichier NER introuvable pour : {file}")
