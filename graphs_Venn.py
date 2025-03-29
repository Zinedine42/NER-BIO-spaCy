import os
import json
import csv
from matplotlib_venn import venn2
import matplotlib.pyplot as plt

NER_DIR = "NER-OUTPUT"
POS_DIR = "POS-OUTPUT"
OUTPUT_DIR = "venn_results"
CSV_PATH = os.path.join(OUTPUT_DIR, "venn_stats.csv")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Extraire de NER
def extract_ner_words(ner_path):
    with open(ner_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return {ent["word"].lower() for ent in data.get("entities", [])}

# Extraire de POS mais que les PROPN
def extract_pos_words(pos_path):
    with open(pos_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return {token["text"].lower() for token in data if token.get("pos") == "PROPN"}

# Fichier CSV pour les statistiques
with open(CSV_PATH, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Fichier", "Taille REN", "Taille PROPN", "Intersection"])

    # Associer les NER et les POS
    for root, _, files in os.walk(POS_DIR):
        for file in files:
            if file.endswith("_PROPN.json"):
                pos_path = os.path.join(root, file)
                base_name = file.replace("_PROPN.json", ".json")

                ner_match = None
                for ner_root, _, ner_files in os.walk(NER_DIR):
                    if base_name in ner_files:
                        ner_match = os.path.join(ner_root, base_name)
                        break

                if ner_match:
                    ner_words = extract_ner_words(ner_match)
                    pos_words = extract_pos_words(pos_path)
                    intersection = ner_words & pos_words

                    # Affichage pour vérification
                    print(f"Fichier : {base_name}")
                    print(f"REN = {len(ner_words)}")
                    print(f"PROPN = {len(pos_words)}")
                    print(f"INTERSECTION = {len(intersection)}")
                    print("----------------------")

                    # Ecriture dans le CSV
                    writer.writerow([base_name.replace(".json", ""), len(ner_words), len(pos_words), len(intersection)])

                    # Création du diagramme
                    plt.figure(figsize=(6,6))
                    venn2([ner_words, pos_words], set_labels=("Entités Nommées", "PROPN"))
                    venn = venn2([ner_words, pos_words], set_labels=("Entités Nommées", "PROPN"))
                    # Remmetre l'affichage droit
                    label_propn = venn.get_label_by_id("01")
                    label_inter = venn.get_label_by_id("11")
                    if label_propn and label_inter:
                        text_propn = label_propn.get_text()
                        text_inter = label_inter.get_text()
                        label_propn.set_text(text_inter)
                        label_inter.set_text(text_propn)
                    plt.title(base_name.replace(".json", ""))

                    # Sauvegarde
                    save_name = base_name.replace(".json", ".png")
                    save_path = os.path.join(OUTPUT_DIR, save_name)
                    plt.savefig(save_path)
                    plt.close()

