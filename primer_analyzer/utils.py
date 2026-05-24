import primer3
from Bio.SeqUtils import gc_fraction

def analyze_single_primer(seq):
    """Calculates length, GC%, Tm, and Hairpin dG for an individual sequence."""
    if not seq:
        return None
    
    length = len(seq)
    gc_content = gc_fraction(seq) * 100
    tm = primer3.calc_tm(seq)
    hairpin = primer3.calc_hairpin(seq)
    
    # Return numerical dG directly (defaults to 0.00 if no structure found)
    hp_dg = hairpin.dg / 1000 if hairpin.structure_found else 0.00
    
    return {
        "length": length,
        "gc": gc_content,
        "tm": tm,
        "hairpin_dg": hp_dg
    }

def analyze_dimer_dg(seq1, seq2):
    """Calculates dimer free energy (dG) value directly."""
    if not seq1 or not seq2:
        return 0.00
    
    dimer = primer3.calc_heterodimer(seq1, seq2)
    if dimer.structure_found:
        return dimer.dg / 1000
    return 0.00
