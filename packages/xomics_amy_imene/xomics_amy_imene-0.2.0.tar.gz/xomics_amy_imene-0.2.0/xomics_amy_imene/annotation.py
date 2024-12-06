"""
On va créer les classes : Gene, Transcrit, et Exon.
Un gène contient des transcrits, et un transcrit contient des exons.
Un gène est une entité indépendante, tandis que les transcrits et les exons sont des sous-éléments liés au gène.
"""
class Exon:
    def __init__(self, exon_id, transcript_id, gene_id, start, end, strand, gff_line=None):
        """
        Initialise un objet Exon.

        exon_id: Identifiant unique de l'exon.
        transcript_id: Identifiant du transcrit parent.
        gene_id: Identifiant du gène parent.
        start: Position de début de l'exon sur la séquence.
        Position de fin de l'exon sur la séquence.
        strand: Orientation (+ ou -) sur le brin.
        gff_line: Ligne GFF d'origine pour garder les informations initiales.
        """
        self.exon_id = exon_id
        self.transcript_id = transcript_id
        self.gene_id = gene_id
        self.start = start
        self.end = end
        self.strand = strand
        self.gff_line = gff_line

    def __repr__(self):
        return f"Exon(exon_id='{self.exon_id}', start={self.start}, end={self.end}, strand='{self.strand}')"

#t = Transcript(.., )
#t.add_exon(e)

class Transcript:
    def __init__(self, transcript_id, gene_id, model_evidence=None, gff_line=None):
        self.transcript_id = transcript_id
        self.gene_id = gene_id
        self.model_evidence = model_evidence
        self.exons:list[Exon] = [] #une liste qui va contenir des objects exons
        self.gff_line = gff_line

    def add_exon(self, exon:Exon): #utilisée pour ajouter un exon à un transcrit. Représente l'objet actuel de la classe Transcrit sur lequel la méthode est appelée. Représente l'exon à ajouter, qui doit être une instance de la classe Exon.
        if exon.transcript_id != self.transcript_id: #Cette ligne vérifie si le transcript_id de l'exon correspond bien au transcript_id du transcrit.
            raise ValueError(f"mismatching trancriptID {exon.transcript_id} {self.transcript_id}") # Pour empêcher l'ajout d'un exon incorrect au transcrit.
        self.exons.append(exon)

    def __eq__(self, other): #s == o  <==> s.__eq__(o)
        """
        Vérifie si deux objets Transcrit sont égaux.
        Prend un autre objet Transcrit.
        return: True si les transcript_id et gene_id sont identiques, sinon False.
        """
        return (
            isinstance(other, Transcript)
            and self.transcript_id == other.transcript_id
            and self.gene_id == other.gene_id
        )
    def __repr__(self):
        return f"Transcript(transcript_id='{self.transcript_id}', gene_id='{self.gene_id}')"

class Gene:
    def __init__(self, gene_id, name, start, stop, description=None, dbxref=None, gff_line=None):
        self.gene_id = gene_id
        self.name = name
        self.description = description
        self.dbxref = dbxref
        self.transcripts: list[Transcript] = []  # Liste d'objets Transcript
        self.gff_line = gff_line
        self.start = start
        self.stop = stop

    def add_transcrit(self, transcrit):
        if transcrit.gene_id != self.gene_id:
            raise ValueError(f"mismatching trancriptID {exon.transcript.gene_id} {self.gene_id}")
        self.transcripts.append(transcrit)

    def __add__(self, gene2): #g1 + g2 <==> g1.__add__(g2)
        """
        Objectif : Fusion de deux objets Gene
        Créer un nouvel objet Gene fusionné.

        L'objectif est de créer une nouvelle instance de Gene contenant tous les transcrits uniques des deux gènes initiaux.
        Conditions pour la fusion :
        1) Les deux gènes doivent avoir le même gene_id.
        Si ce n'est pas le cas, une exception ValueError est levée.
        Union des transcrits :
        Les transcrits des deux objets Gene sont ajoutés au nouvel objet, en évitant les doublons.
        """
        if not isinstance(gene2, Gene) or self.gene_id != gene2.gene_id:
            raise ValueError("Les gènes doivent avoir le même gene_id")

        # Fusion des attributs du gène
        new_description = self.description + " | " + gene2.description
        new_dbxref = self.dbxref + " | " + gene2.dbxref

        # Créer une nouvelle instance de Gene
        gene_fusionné = Gene(
            self.gene_id, 
            self.name, 
            new_description, 
            new_dbxref, 
            self.gff_line
        )

        # Fusion des transcrits sans doublons
        gene_fusionné.transcripts = list(self.transcripts)
        for transcrit in gene2.transcripts:
            if transcrit not in gene_fusionné.transcripts:
                gene_fusionné.transcripts.append(transcrit)

        return gene_fusionné

    def __repr__(self):
        return f"Gene(gene_id='{self.gene_id}', name='{self.name}', description='{self.description}')"










    