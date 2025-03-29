import os
import json
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np

NER_DIR = "NER-OUTPUT"
CHART_DIR = "comparison_charts"
os.makedirs(CHART_DIR, exist_ok=True)

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def compare_entities(ref_entities, ocr_entities):
    ref_set = {(ent["word"], ent["BIO"]) for ent in ref_entities}
    ocr_set = {(ent["word"], ent["BIO"]) for ent in ocr_entities}

    vp = ref_set & ocr_set
    fp = ocr_set - ref_set
    fn = ref_set - ocr_set

    return len(vp), len(fp), len(fn)

# comparaison 
global_counts = defaultdict(lambda: {"VP": 0, "FP": 0, "FN": 0})

for author in os.listdir(NER_DIR):
    author_path = os.path.join(NER_DIR, author)
    if not os.path.isdir(author_path):
        continue

    ref_dir = os.path.join(author_path, "REF")
    kraken_dir = os.path.join(author_path, f"{author}_kraken")
    tess_dir = os.path.join(author_path, f"{author}_TesseractFra-PNG")

    if not os.path.exists(ref_dir):
        continue

    for ref_file in os.listdir(ref_dir):
        if not ref_file.endswith(".json"):
            continue

        base_name = ref_file.replace(".json", "")
        ref_data = load_json(os.path.join(ref_dir, ref_file)).get("entities", [])

        # Kraken
        if os.path.exists(kraken_dir):
            for f in os.listdir(kraken_dir):
                if base_name in f and f.endswith(".json"):
                    ocr_data = load_json(os.path.join(kraken_dir, f)).get("entities", [])
                    vp, fp, fn = compare_entities(ref_data, ocr_data)
                    global_counts["Kraken"]["VP"] += vp
                    global_counts["Kraken"]["FP"] += fp
                    global_counts["Kraken"]["FN"] += fn
                    break

        # Tesseract
        if os.path.exists(tess_dir):
            for f in os.listdir(tess_dir):
                if base_name in f and f.endswith(".json"):
                    ocr_data = load_json(os.path.join(tess_dir, f)).get("entities", [])
                    vp, fp, fn = compare_entities(ref_data, ocr_data)
                    global_counts["Tesseract"]["VP"] += vp
                    global_counts["Tesseract"]["FP"] += fp
                    global_counts["Tesseract"]["FN"] += fn
                    break

# graphique
methods = list(global_counts.keys())
x = np.arange(len(methods))
width = 0.25

vp_vals = [global_counts[m]["VP"] for m in methods]
fp_vals = [global_counts[m]["FP"] for m in methods]
fn_vals = [global_counts[m]["FN"] for m in methods]

plt.figure(figsize=(10, 6))
plt.bar(x - width, vp_vals, width, label="Vrais Positifs", color="green")
plt.bar(x, fp_vals, width, label="Faux Positifs", color="red")
plt.bar(x + width, fn_vals, width, label="Faux Négatifs", color="orange")

plt.xticks(x, methods)
plt.ylabel("Nombre d'entités")
plt.title("Comparaison REN : VP / FP / FN par méthode OCR")
plt.legend()
plt.tight_layout()

print("Méthodes trouvées :", methods)
print("VP :", vp_vals)
print("FP :", fp_vals)
print("FN :", fn_vals)

plt.savefig(os.path.join(CHART_DIR, "vp_fp_fn_barplot.png"))
plt.close()
