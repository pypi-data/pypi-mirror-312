from .annotation import Gene, Transcript, Exon  # Importation des classes
import matplotlib.pyplot as plt

class Annotation:
    def __init__(self, gff_file: str = None):
        """
        Initialise un objet Annotation à partir d'un fichier GFF.
        Crée des objets Gene, Transcript et Exon et les organise dans une structure interne.

        :param gff_file: Chemin vers le fichier GFF
        """
        self.genes = {}  # Dictionnaire des gènes : {gene_id: Gene}
        self.transcrits = {}  # Dictionnaire des transcrits : {transcript_id: Transcript}
        self.exons = []  # Liste des exons

        if gff_file:  # Si un fichier GFF est passé, on l'ouvre
            with open(gff_file, "r") as f:
                # Remplir les informations des gènes, transcrits, exons, etc. à partir du fichier
                self._load_gff(f)


    def _load_gff(self, f):
        """
        Lit le fichier GFF et remplit les informations des gènes, transcrits, exons, etc.
        """
        for line in f:
            line = line.strip()

            fields = line.split("\t")
            if len(fields) < 9:  # Vérification des colonnes nécessaires
                print(f"Ligne mal formée : {line}")
                continue

            # Extraction des colonnes
            seqid, source, feature_type, start, end, score, strand, phase, attributes = fields
            start, end = int(start), int(end)
            attr_dict = self.read_attributes_field(attributes)

            # Création des objets selon le type de caractéristique
            if feature_type == "gene":
                gene_id = attr_dict['ID'] if 'ID' in attr_dict else ""
                gene = Gene(
                    gene_id=gene_id,
                    name=attr_dict['Name'] if 'Name' in attr_dict else "",
                    start=start,
                    stop=end,
                    description=attr_dict['description'] if 'description' in attr_dict else "",
                    dbxref=attr_dict['Dbxref'] if 'Dbxref' in attr_dict else "",
                    gff_line=line
                )
                self.genes[gene_id] = gene

            elif feature_type == "mRNA":
                transcript_id = attr_dict.get("ID", "")
                gene_id = attr_dict.get("Parent", "")
                transcript = Transcript(
                    transcript_id=transcript_id,
                    gene_id=gene_id,
                    gff_line=line
                )
                self.transcrits[transcript_id] = transcript

            elif feature_type == "exon":
                exon_id = attr_dict.get("ID", "")
                transcript_id = attr_dict.get("Parent", "")
                exon = Exon(
                    exon_id=exon_id,
                    transcript_id=transcript_id,
                    gene_id=attr_dict.get("gene_id", ""),
                    start=start,
                    end=end,
                    strand=strand,
                    gff_line=line
                )
                self.exons.append(exon)
            else:
                #Lever une exception si le type de fonctionnalité n'est ni "gene" ni "mRNA" ni "exon"
                raise ValueError(f"Type de fonctionnalité inconnu : {feature_type}. Attendu 'gene' ou 'mRNA' ou 'exon'.")

    def __add__(self, other):
        """
        Fusionne deux objets Annotation en ajoutant tous les gènes, transcrits et exons.
        
        :param other: Autre objet Annotation à fusionner avec l'objet actuel
        :return: Une nouvelle instance de Annotation fusionnée
        """
        if not isinstance(other, Annotation):
            raise ValueError("Les deux objets doivent être des instances de la classe Annotation")

        # Crée une nouvelle instance d'Annotation vide (sans fichier)
        merged_annotation = Annotation()  # Utiliser une instanciation vide sans fichier
        # Fusionner les gènes
        for gene_id, gene in self.genes.items():
            if gene_id in other.genes:
                # Fusionner les gènes ayant le même ID
                merged_annotation.genes[gene_id] = gene + other.genes[gene_id]  # Fusionner les gènes avec la méthode __add__ de Gene
            else:
                merged_annotation.genes[gene_id] = gene  # Si le gène n'existe que dans self, on l'ajoute tel quel

        # Ajouter les gènes de l'autre annotation qui ne sont pas dans la première
        for gene_id, gene in other.genes.items():
            if gene_id not in merged_annotation.genes:
                merged_annotation.genes[gene_id] = gene  # Ajouter le gène si pas déjà présent

        # Fusionner les transcrits et exons de la même manière, si nécessaire
        # Vous pouvez appliquer une logique similaire pour les transcrits et exons si vous en avez besoin

        return merged_annotation

    def __str__(self):
        return f"Annotation({len(self.genes)} gènes, {len(self.transcrits)} transcrits, {len(self.exons)} exons)"

    def to_gff(self, output_file: str):
        """
        Exporte l'annotation sous forme de fichier GFF.

        :param output_file: Chemin du fichier de sortie
        """
        with open(output_file, 'w') as f:
            # Écrire les gènes
            for gene in self.genes.values():
                f.write(gene.gff_line + "\n")

            # Écrire les transcrits
            for transcript in self.transcrits.values():
                f.write(transcript.gff_line + "\n")

            # Écrire les exons
            for exon in self.exons:
                f.write(exon.gff_line + "\n")


    def rna_lens(self, output_file: str):
        """
        Dessine un boxplot des longueurs des transcrits pour chaque gène et
        sauvegarde le graphique dans un fichier.

        :param output_file: Chemin du fichier de sortie pour enregistrer le boxplot
        :raises ValueError: Si aucun transcrit ou exon n'est trouvé pour un gène.
        """
        # Récupérer les longueurs des transcrits pour chaque gène
        RNA_lens = []  # Liste des longueurs des transcrits pour chaque gène
        gene_names = []  # Liste des noms des gènes

        for gene_id, gene in self.genes.items():
            # Récupérer tous les transcrits associés à ce gène
            transcrit_lens = []
            for transcript_id, transcript in self.transcrits.items():
                if transcript.gene_id == gene_id:
                    # Calculer la longueur totale du transcrit (somme des longueurs des exons)
                    total_length = sum(
                        exon.end - exon.start + 1 for exon in self.exons if exon.transcript_id == transcript_id
                    )
                    if total_length > 0:
                        transcrit_lens.append(total_length)
                    else:
                        raise ValueError(f"Le transcrit '{transcript_id}' n'a aucun exon.")

            # Si aucun transcrit n'est trouvé pour le gène, lever une exception
            if not transcrit_lens:
                raise ValueError(f"Le gène '{gene_id}' ne contient aucun transcrit valide.")

            # Ajouter les longueurs des transcrits et le nom du gène
            RNA_lens.append(transcrit_lens)
            gene_names.append(gene.name if gene.name else gene_id)

        # Vérifier que des données ont été collectées pour le boxplot
        if not RNA_lens:
            raise ValueError("Aucune longueur de transcrit n'a été trouvée pour les gènes de l'annotation.")


        # Déterminer les couleurs des boîtes en fonction de la médiane
        medians = [max(lengths) for lengths in RNA_lens]
        max_median = max(medians)
        min_median = min(medians)
        color_map = ['red' if median == max_median else 'blue' if median == min_median else 'yellow' for median in medians]

        # Créer le boxplot avec matplotlib
        fig, ax = plt.subplots(figsize=(12, 6))
        boxplots = ax.boxplot(RNA_lens, patch_artist=True, labels=gene_names)

        # Appliquer les couleurs aux boîtes
        for patch, color in zip(boxplots['boxes'], color_map):
            patch.set_facecolor(color)


       # Ajouter des titres et des labels
        ax.set_title('Distribution des longueurs des transcrits pour chaque gène')
        ax.set_ylabel('Longueur des transcrits (paires de bases)')
        ax.set_xlabel('Gènes')
        plt.xticks(rotation=45, ha='right')

        # Sauvegarder le graphique dans le fichier spécifié
        fig.savefig(output_file)
        plt.close(fig)  # Fermer la figure après avoir sauvegardé le fichier


    
    def read_attributes_field(self, champ_att: str) -> dict:
        """
        Analyse un champ d'attributs du format GFF et retourne un dictionnaire.

        :param champ_att: Chaîne d'attributs à analyser
        :return: Dictionnaire des attributs
        """
        attr_dict = {}
        for item in champ_att.split(";"):
            item = item.strip()
            if " " in item:
                key, value = item.split(" ", 1)
                attr_dict[key.strip()] = value.strip()
            else:
                attr_dict[item.strip()] = ""  # Cas où il n'y a qu'une clé
        return attr_dict

    
    def get_gene(self, gene_id: str) -> Gene:
        """
        Récupère un objet Gene par son ID.
        
        :param gene_id: Identifiant du gène
        :return: Objet Gene correspondant à l'ID passé
        :raises ValueError: Si aucun gène avec cet identifiant n'est trouvé
        """
        if gene_id not in self.genes:
            raise ValueError(f"Aucun gène trouvé avec l'identifiant '{gene_id}'")
        return self.genes[gene_id]

    def get_all_genes(self) -> list:
        """
        Retourne une liste de tous les gènes dans l'annotation.

        :return: Liste des objets Gene
        """
        return list(self.genes.values())
