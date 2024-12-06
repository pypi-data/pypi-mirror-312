from .readers_gff import Annotation

def gff_to_annotation(gff_file)-> Annotation:
    a = Annotation(gff_file)
    return a