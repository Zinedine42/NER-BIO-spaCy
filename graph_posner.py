import os
import json
import matplotlib.pyplot as plt
from collections import defaultdict

POS_DIR = "POS-OUTPUT"
NER_DIR = "NER-OUTPUT"
OUTPUT_DIR = "pos_ner_overlap"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Fonction pour charger un fichier JSON
def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Dictionnaire : {POS: {"total": x, "entite": y}}
pos_stats = defaultdict(lambda: {"total": 0, "entite": 0})

for root, _, files in os.walk(POS_DIR):
    for file in files:
        if file.endswith(".json") and "_PROPN" not in file:  # on ignore les fichiers filtrés
            pos_path = os.path.join(root, file)
            pos_data = load_json(pos_path)

            # Récupérer le fichier NER correspondant
            relative_path = os.path.relpath(pos_path, POS_DIR)
            ner_path = os.path.join(NER_DIR, relative_path)
            if not os.path.exists(ner_path):
                continue

            ner_data = load_json(ner_path)
            ner_words = {ent["word"].lower() for ent in ner_data.get("entities", [])}

            for token in pos_data:
                word = token.get("text", "").lower()
                pos = token.get("pos")
                if pos:
                    pos_stats[pos]["total"] += 1
                    if word in ner_words:
                        pos_stats[pos]["entite"] += 1

# Préparer les données pour le graphique
labels = []
proportions = []

for pos, counts in pos_stats.items():
    if counts["total"] > 0:
        labels.append(pos)
        proportions.append(counts["entite"] / counts["total"])

# Graphique
plt.figure(figsize=(10, 6))
plt.bar(labels, proportions, color="skyblue")
plt.ylabel("Proportion reconnue comme entité nommée")
plt.xlabel("Catégorie grammaticale (POS)")
plt.title("Part des mots par POS reconnus comme entités nommées")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(os.path.join(OUTPUT_DIR, "pos_entity_overlap.png"))
plt.close()
