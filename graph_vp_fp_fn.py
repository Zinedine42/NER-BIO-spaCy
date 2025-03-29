import os
import json
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np

# Dossier contenant les fichiers OCR et de référence
NER_DIR = "NER-OUTPUT"
OUTPUT_DIR = "NER-COMPARISON"
RESULT_FILE = os.path.join(OUTPUT_DIR, "comparison_results.json")
CHART_DIR = "comparison_charts"
os.makedirs(CHART_DIR, exist_ok=True)

# Fonction pour charger un fichier JSON
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Fonction de comparaison des entités
def compare_entities(ref_entities, ocr_entities):
    ref_set = {(ent["word"], ent["BIO"]) for ent in ref_entities}
    ocr_set = {(ent["word"], ent["BIO"]) for ent in ocr_entities}

    true_positives = ref_set & ocr_set
    false_positives = ocr_set - ref_set
    false_negatives = ref_set - ocr_set

    return {
        "Vrais Positifs": list(true_positives),
        "Faux Positifs": list(false_positives),
        "Faux Négatifs": list(false_negatives)
    }

# Comparer les fichiers REF avec Kraken et Tesseract
results = defaultdict(dict)

for author in os.listdir(NER_DIR):
    author_path = os.path.join(NER_DIR, author)
    if os.path.isdir(author_path):
        ref_path = os.path.join(author_path, "REF")
        if not os.path.exists(ref_path):
            continue

        for file in os.listdir(ref_path):
            if file.endswith(".json"):
                base_name = file.replace(".json", "")
                ref_json = load_json(os.path.join(ref_path, file))
                results[author][base_name] = {}

                # Kraken
                kraken_dir = os.path.join(author_path, f"{author}_kraken")
                if os.path.exists(kraken_dir):
                    for f in os.listdir(kraken_dir):
                        if base_name in f and f.endswith(".json"):
                            ocr_json = load_json(os.path.join(kraken_dir, f))
                            results[author][base_name]["kraken"] = compare_entities(ref_json["entities"], ocr_json["entities"])
                            break

                # Tesseract
                tesseract_dir = os.path.join(author_path, f"{author}_TesseractFra-PNG")
                if os.path.exists(tesseract_dir):
                    for f in os.listdir(tesseract_dir):
                        if base_name in f and f.endswith(".json"):
                            ocr_json = load_json(os.path.join(tesseract_dir, f))
                            results[author][base_name]["TesseractFra-PNG"] = compare_entities(ref_json["entities"], ocr_json["entities"])
                            break

# Sauvegarde en JSON
os.makedirs(OUTPUT_DIR, exist_ok=True)
with open(RESULT_FILE, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

# Barplot global
from collections import defaultdict

global_counts = defaultdict(lambda: {"VP": 0, "FP": 0, "FN": 0})

for author_data in results.values():
    for text_data in author_data.values():
        for method, data in text_data.items():
            global_counts[method]["VP"] += len(data.get("Vrais Positifs", []))
            global_counts[method]["FP"] += len(data.get("Faux Positifs", []))
            global_counts[method]["FN"] += len(data.get("Faux Négatifs", []))

methods = list(global_counts.keys())
x = np.arange(len(methods))
width = 0.25

vp_counts = [global_counts[m]["VP"] for m in methods]
fp_counts = [global_counts[m]["FP"] for m in methods]
fn_counts = [global_counts[m]["FN"] for m in methods]

plt.figure(figsize=(10, 6))
plt.bar(x - width, vp_counts, width, label="Vrais Positifs", color="green")
plt.bar(x, fp_counts, width, label="Faux Positifs", color="red")
plt.bar(x + width, fn_counts, width, label="Faux Négatifs", color="orange")

plt.xticks(x, methods)
plt.ylabel("Nombre d'entités")
plt.title("Comparaison des VP / FP / FN par méthode OCR")
plt.legend()
plt.tight_layout()

plt.savefig(os.path.join(CHART_DIR, "vp_fp_fn_barplot.png"))
plt.close()
