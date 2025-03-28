import os
import json
from collections import defaultdict

def load_json(file_path):
    """Charge un fichier JSON."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def compare_entities(ref_entities, ocr_entities):
    """Compare les entités de la référence et d'un OCR."""
    ref_set = {(ent["word"], ent["BIO"]) for ent in ref_entities}
    ocr_set = {(ent["word"], ent["BIO"]) for ent in ocr_entities}
    
    true_positives = ref_set & ocr_set
    false_positives = ocr_set - ref_set
    false_negatives = ref_set - ocr_set
    
    precision = len(true_positives) / (len(true_positives) + len(false_positives)) if (len(true_positives) + len(false_positives)) > 0 else 0
    recall = len(true_positives) / (len(true_positives) + len(false_negatives)) if (len(true_positives) + len(false_negatives)) > 0 else 0
    f_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    print("Précision:", precision)
    print("Rappel:", recall)
    print("F-Score:", f_score)
    
    return {
        "Vrais Positifs": list(true_positives),
        "Faux Positifs": list(false_positives),
        "Faux Négatifs": list(false_negatives),
        "Précision": precision,
        "Rappel": recall,
        "F-Score": f_score
    }

def process_comparison(base_dir, output_dir):
    """Compare les fichiers JSON de la référence avec ceux des OCR."""
    results = defaultdict(dict)
    
    for author in os.listdir(base_dir):
        author_path = os.path.join(base_dir, author)
        if os.path.isdir(author_path):
            ref_path = os.path.join(author_path, "REF")
            
            for file in os.listdir(ref_path):
                if file.endswith(".json"):
                    base_name = file.replace("_PP.json", "")
                    ref_json = load_json(os.path.join(ref_path, file))
                    
                    for method in ["kraken", "TesseractFra-PNG"]:
                        if method == "kraken":
                            ocr_path = os.path.join(author_path, f"{author}_kraken", file.replace("_PP", "_Kraken-base"))
                        else:
                            ocr_path = os.path.join(author_path, f"{author}_TesseractFra-PNG", file.replace("_PP", "_TesseractFra-PNG"))
                        
                        if os.path.exists(ocr_path):
                            ocr_json = load_json(ocr_path)
                            results[author][base_name] = {
                                method: compare_entities(ref_json["entities"], ocr_json["entities"])
                            }
    
    output_file = os.path.join(output_dir, "comparison_results.json")
    os.makedirs(output_dir, exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    
    print(f"Comparaison terminée. Résultats enregistrés dans {output_file}")

# Exécution
input_directory = "NER-OUTPUT"
output_directory = "NER-COMPARISON"
process_comparison(input_directory, output_directory)
