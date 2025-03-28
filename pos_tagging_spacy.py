import os
import json
import spacy

def process_text(text, nlp):
    """Analyse le texte et renvoie les annotations POS."""
    doc = nlp(text)
    annotations = [
        {"text": token.text, "lemma": token.lemma_, "pos": token.pos_, "tag": token.tag_, "dep": token.dep_}
        for token in doc
    ]
    return annotations

def process_directory(input_dir, output_dir):
    """Parcourt les fichiers et applique l'analyse morpho-syntaxique."""
    nlp = spacy.load("fr_core_news_sm")
    os.makedirs(output_dir, exist_ok=True)
    
    for author in os.listdir(input_dir):
        author_path = os.path.join(input_dir, author)
        if os.path.isdir(author_path):
            output_author_path = os.path.join(output_dir, author)
            os.makedirs(output_author_path, exist_ok=True)
            
            for version in os.listdir(author_path):
                version_path = os.path.join(author_path, version)
                if os.path.isdir(version_path):
                    output_version_path = os.path.join(output_author_path, version)
                    os.makedirs(output_version_path, exist_ok=True)
                    
                    for file in os.listdir(version_path):
                        if file.endswith(".txt"):
                            input_file_path = os.path.join(version_path, file)
                            output_file_path = os.path.join(output_version_path, file.replace(".txt", ".json"))
                            
                            with open(input_file_path, "r", encoding="utf-8") as f:
                                text = f.read()
                            
                            annotations = process_text(text, nlp)
                            
                            with open(output_file_path, "w", encoding="utf-8") as f:
                                json.dump(annotations, f, ensure_ascii=False, indent=4)
                            
                            print(f"Annotation terminée pour {file}")

# Exécution
data_directory = "DATA-ELTeC"
output_directory = "POS-OUTPUT"
process_directory(data_directory, output_directory)
