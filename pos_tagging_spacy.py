import os
import json
from collections import defaultdict

def load_json(file_path):
    """Charge un fichier JSON."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def compare_propn(ref_propn, ocr_propn):
    """Compare les PROPN entre la référence et l'OCR."""
    ref_set = {ent["text"] for ent in ref_propn}
    ocr_set = {ent["text"] for ent in ocr_propn}
    
    intersection = ref_set & ocr_set  # PROPN communs
    difference_ref_ocr = ref_set - ocr_set  # PROPN manquants dans l'OCR
    difference_ocr_ref = ocr_set - ref_set  # PROPN ajoutés par l'OCR
    union = ref_set | ocr_set  # Ensemble total des PROPN détectés
    
    return {
        "Intersection": list(intersection),
        "Différence (Réf - OCR)": list(difference_ref_ocr),
        "Différence (OCR - Réf)": list(difference_ocr_ref),
        "Union": list(union)
    }

def process_comparison(base_dir, output_dir):
    """Compare les fichiers JSON de PROPN entre la référence et les OCR."""
    results = defaultdict(dict)
    
    for author in os.listdir(base_dir):
        author_path = os.path.join(base_dir, author)
        if os.path.isdir(author_path):
            ref_path = os.path.join(author_path, "REF")
            
            for file in os.listdir(ref_path):
                if file.endswith("_PROPN.json"):
                    base_name = file.replace("_PROPN.json", "")
                    ref_json = load_json(os.path.join(ref_path, file))
                    
                    for method in ["kraken", "TesseractFra-PNG"]:
                        ocr_file = file.replace("_PP", f"_{method}")
                        ocr_path = os.path.join(author_path, f"{author}_{method}", ocr_file)
                        
                        if os.path.exists(ocr_path):
                            ocr_json = load_json(ocr_path)
                            results[author][base_name] = {
                                method: compare_propn(ref_json, ocr_json)
                            }
    
    output_file = os.path.join(output_dir, "propn_comparison_results.json")
    os.makedirs(output_dir, exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    
    print(f"Comparaison des PROPN terminée. Résultats enregistrés dans {output_file}")

# Exécution
input_directory = "POS-OUTPUT"
output_directory = "PROPN-COMPARISON"
process_comparison(input_directory, output_directory)