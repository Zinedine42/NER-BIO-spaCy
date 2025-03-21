import os
import json
import spacy

# Charger le modèle spaCy pour le français
nlp = spacy.load("fr_core_news_md")

def get_bio_format(doc):
    """Extrait les entités en format BIO."""
    bio_tags = []
    for ent in doc.ents:
        tokens = ent.text.split()
        for i, token in enumerate(tokens):
            tag = f"{'B' if i == 0 else 'I'}-{ent.label_}"
            bio_tags.append({"word": token, "BIO": tag, "category": ent.label_})
    return bio_tags

def process_text_file(input_path, output_path):
    """Lit un fichier texte, applique NER et sauvegarde les résultats."""
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()
    
    doc = nlp(text)
    entities = get_bio_format(doc)
    
    result = {"text": text, "entities": entities}
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    
    print(f"Traitement terminé : {output_path}")

def process_directory(input_dir, output_dir):
    """Parcourt les fichiers de input_dir et génère les fichiers de sortie."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".txt"):
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(input_path, input_dir)
                output_path = os.path.join(output_dir, relative_path.replace(".txt", ".json"))
                
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                process_text_file(input_path, output_path)

# Exécution sur le dossier DATA-ELTeC
input_directory = "DATA-ELTeC"
output_directory = "NER-OUTPUT"
process_directory(input_directory, output_directory)
