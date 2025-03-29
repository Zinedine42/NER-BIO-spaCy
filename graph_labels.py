import os
import json
import matplotlib.pyplot as plt
from collections import Counter, defaultdict

NER_DIR = "NER-OUTPUT"
OUTPUT_DIR = "label_distribution"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Détecter la version du fichier à partir du chemin
def detect_version(path):
    path = path.lower()
    if "ref" in path:
        return "REF"
    elif "kraken" in path:
        return "Kraken"
    elif "tesseract" in path:
        return "TesseractFra-PNG"
    else:
        return "Autre"

# Dictionnaire pour stocker les catégories par version
data_by_version = defaultdict(list)

# Parcours des fichiers .json
for root, _, files in os.walk(NER_DIR):
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = json.load(f)
                    version = detect_version(file_path)
                    for ent in content.get("entities", []):
                        label = ent.get("category")
                        if label:
                            data_by_version[version].append(label)
            except Exception as e:
                print(f"Erreur avec le fichier {file_path} : {e}")

# Générer un camembert pour chaque version
for version, labels in data_by_version.items():
    counter = Counter(labels)
    labels_list = list(counter.keys())
    sizes = list(counter.values())

    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels_list, autopct='%1.1f%%', startangle=90)
    plt.title(f"Répartition des entités nommées - {version}")
    plt.axis('equal')

    filename = f"label_distribution_{version}.png"
    plt.savefig(os.path.join(OUTPUT_DIR, filename))
    plt.close()
    print(f"Graphique enregistré : {filename}")
