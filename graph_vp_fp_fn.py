import os
import json
import matplotlib.pyplot as plt
from collections import defaultdict

# Fichier d’entrée
INPUT_JSON = "NER-COMPARISON/comparison_results.json"
OUTPUT_DIR = "comparison_charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

global_counts = defaultdict(lambda: {"VP": 0, "FP": 0, "FN": 0})

with open(INPUT_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

    for author, texts in data.items():
        for text, methods in texts.items():
            for method, values in methods.items():
                vp = len(values.get("Vrais Positifs", []))
                fp = len(values.get("Faux Positifs", []))
                fn = len(values.get("Faux Négatifs", []))

                global_counts[method]["VP"] += vp
                global_counts[method]["FP"] += fp
                global_counts[method]["FN"] += fn

# Graphique
methods = list(global_counts.keys())
vp_counts = [global_counts[m]["VP"] for m in methods]
fp_counts = [global_counts[m]["FP"] for m in methods]
fn_counts = [global_counts[m]["FN"] for m in methods]

x = range(len(methods))
width = 0.25

plt.figure(figsize=(10, 6))
plt.bar([i - width for i in x], vp_counts, width, label="Vrais Positifs", color="blue")
plt.bar(x, fp_counts, width, label="Faux Positifs", color="violet")
plt.bar([i + width for i in x], fn_counts, width, label="Faux Négatifs", color="orange")

plt.xticks(x, methods)
plt.ylabel("Nombre d'entités")
plt.title("Comparaison des VP / FP / FN par méthode OCR")
plt.legend()
plt.tight_layout()

plt.savefig(os.path.join(OUTPUT_DIR, "vp_fp_fn_barplot.png"))
plt.close()
