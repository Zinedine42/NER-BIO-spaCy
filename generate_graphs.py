import os
import matplotlib.pyplot as plt
from collections import Counter

# Dossier contenant les fichiers de référence et OCR
reference_dir = "path_to_reference_folder"
ocr_dir = "path_to_ocr_folder"

def compare_files(reference_dir, ocr_dir):
    all_labels_reference = []
    all_labels_ocr = []
    
    # Parcours les fichiers dans le dossier de référence
    for filename in os.listdir(reference_dir):
        ref_file_path = os.path.join(reference_dir, filename)
        ocr_file_path = os.path.join(ocr_dir, filename)

        if os.path.exists(ocr_file_path):  # Assure que le fichier OCR existe
            with open(ref_file_path, 'r') as ref_file, open(ocr_file_path, 'r') as ocr_file:
                ref_lines = ref_file.readlines()
                ocr_lines = ocr_file.readlines()

                # Assure qu'il y a le même nombre de lignes
                if len(ref_lines) == len(ocr_lines):
                    for ref_line, ocr_line in zip(ref_lines, ocr_lines):
                        # Extraire les étiquettes à partir des lignes (en supposant que le format BIO est utilisé)
                        ref_labels = ref_line.strip().split()[1]  # Récupère la deuxième colonne (l'étiquette)
                        ocr_labels = ocr_line.strip().split()[1]  # Même chose pour l'OCR

                        all_labels_reference.append(ref_labels)
                        all_labels_ocr.append(ocr_labels)
                else:
                    print(f"Le nombre de lignes diffère pour le fichier {filename}")
        else:
            print(f"Le fichier OCR {filename} n'a pas été trouvé.")

    return all_labels_reference, all_labels_ocr

def generate_comparison_graph(reference_labels, ocr_labels):
    # Compte les occurrences des étiquettes dans les deux listes
    counter_ref = Counter(reference_labels)
    counter_ocr = Counter(ocr_labels)

    # Création de l'ensemble des étiquettes uniques
    unique_labels = set(reference_labels).union(set(ocr_labels))

    # Initialisation des listes pour les étiquettes et leurs comptages
    ref_counts = [counter_ref[label] for label in unique_labels]
    ocr_counts = [counter_ocr[label] for label in unique_labels]

    # Création du graphique
    fig, ax = plt.subplots(figsize=(10, 6))
    bar_width = 0.35
    index = range(len(unique_labels))

    # Tracer les barres
    ax.bar(index, ref_counts, bar_width, label="Référence", color='b')
    ax.bar([i + bar_width for i in index], ocr_counts, bar_width, label="OCR", color='r')

    ax.set_xlabel('Étiquettes')
    ax.set_ylabel('Occurrences')
    ax.set_title('Comparaison des étiquettes entre la Référence et l\'OCR')
    ax.set_xticks([i + bar_width / 2 for i in index])
    ax.set_xticklabels(unique_labels, rotation=45, ha='right')
    ax.legend()

    plt.tight_layout()
    plt.show()

def main():
    # Comparaison des fichiers et extraction des étiquettes
    reference_labels, ocr_labels = compare_files(reference_dir, ocr_dir)

    # Génération du graphique de comparaison
    generate_comparison_graph(reference_labels, ocr_labels)

# Exécution du script principal
if __name__ == "__main__":
    main()