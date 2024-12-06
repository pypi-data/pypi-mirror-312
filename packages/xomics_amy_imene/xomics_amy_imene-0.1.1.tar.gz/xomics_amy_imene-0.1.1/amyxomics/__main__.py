
import sys
# Importez la classe Annotation depuis le fichier où elle est définie
from .readers_gff import Annotation

# Spécifiez le chemin vers votre fichier GFF
gff_file_1 = sys.argv[1]  # Remplacez par le chemin réel vers votre fichier

# Créez une instance de la classe Annotation
annotation = Annotation("gff_file_path")

# Affichez un résumé des objets lus
print(f"Nombre de gènes lus : {len(annotation.genes)}")
print(f"Nombre de transcrits lus : {len(annotation.transcrits)}")
print(f"Nombre d'exons lus : {len(annotation.exons)}")

# Exemple : Afficher les 5 premiers gènes lus
print("\nPremiers gènes lus :")
for gene_id, gene in list(annotation.genes.items())[:5]:
    print(gene)

# Exemple : Afficher les 5 premiers exons
print("\nPremiers exons lus :")
for exon in annotation.exons[:5]:
    print(exon)



#Pour tester l'addition de deux fichiers, __add__


gff_file_2 =sys.argv[2]

# Créer deux objets Annotation à partir des fichiers GFF
annotation_1 = Annotation(gff_file_1)
annotation_2 = Annotation(gff_file_2)

# Fusionner les deux annotations
merged_annotation = annotation_1 + annotation_2

# Afficher le résultat de la fusion
print(f"Nombre de gènes fusionnés : {len(merged_annotation.genes)}")
print(f"Nombre de transcrits fusionnés : {len(merged_annotation.transcrits)}")
print(f"Nombre d'exons fusionnés : {len(merged_annotation.exons)}")

# Exemple : Afficher les 5 premiers gènes fusionnés
print("\nPremiers gènes fusionnés :")
for gene in list(merged_annotation.genes.values())[:5]:
    print(gene)

#pour tester to_gff

# Crée une instance de Annotation à partir du fichier GFF
annotation = Annotation(sys.argv[3])
# Appel de la méthode pour exporter l'annotation dans un fichier GFF
annotation.to_gff(sys.argv[3])


