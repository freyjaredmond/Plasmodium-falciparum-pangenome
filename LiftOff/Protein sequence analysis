# This script performs pairwise protein sequence comparison between original genome annotations and 3D7 LiftOff annotations for non-exact GffCompare matches
# It consists of three functions:
# parse_liftoff_gff_get_sequences() - Extracts CDS features from a GFF3 file, concatenates exons in the correct order, applies phase offsets, and translates to protein sequences
#read_tracking_non_exact() - Reads a GffCompare tracking file and returns all non-exact matches with their query gene, reference gene and classification code
#compare_proteins() - Performs global pairwise alignment of two protein sequences using Biopython pairwise2 
#For each non-exact match, the script compares the original and LiftOff protein sequences and reports identity statistics for GffCompare tracking code.
#Input:  Original genome GFF3 and FASTA, LiftOff GFF3, filtered tracking TSV
# Output: TSV of protein comparison results, summary statistics by class code


import pandas as pd
from Bio import SeqIO
from Bio.Seq import Seq
from Bio import pairwise2
import os

def parse_liftoff_gff_get_sequences(gff_file, genome_fasta): 
    """
    Extract CDS sequences from Liftoff GFF3 and translate to protein.
    Returns dict: {gene_id: protein_sequence}
    """
    proteins = {}
    genome = SeqIO.to_dict(SeqIO.parse(genome_fasta, "fasta"))
    print(f"Loaded {len(genome)} chromosomes")

    transcript_cds = {}  # {transcript_id: cds info}
    transcript_to_gene = {}  # {transcript_id: gene_id}
    
    #parse gff file
    with open(gff_file, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            
            fields = line.strip().split('\t')
            if len(fields) < 9:   
                continue
            feature_type = fields[2]
            if feature_type != 'CDS': #only want protein coding
                continue
            
            chrom = fields[0]
            start = int(fields[3]) - 1  # Convert to 0-based indexing
            end = int(fields[4])
            strand = fields[6]
            phase = int(fields[7]) if fields[7] != '.' else 0  
            attributes = fields[8]
            
            # Parse attributes
            attr_dict = {}
            for attr in attributes.split(';'):
                if '=' in attr:
                    key, value = attr.split('=', 1) 
                    attr_dict[key] = value 
            
            transcript_id = attr_dict.get('Parent')
            gene_id = attr_dict.get('gene_id')
            
            if not transcript_id or not gene_id or chrom not in genome:
                continue
            
            # Store gene-transcript mapping
            transcript_to_gene[transcript_id] = gene_id
            
            # Store CDS coordinates with phase
            if transcript_id not in transcript_cds:  
                transcript_cds[transcript_id] = []
            transcript_cds[transcript_id].append((chrom, start, end, strand, phase)) 
    
    print(f"Found {len(transcript_cds)} transcripts with CDS features")
    
    # Translate each transcript
    translation_errors = 0
    phase_applied_count = 0
    multi_exon_count = 0
    
    for transcript_id, cds_list in transcript_cds.items():
        gene_id = transcript_to_gene.get(transcript_id) 
        if not gene_id:
            continue
        
        # Track multi-exon genes (genes with introns)
        if len(cds_list) > 1:  
            multi_exon_count += 1 
        
        strand = cds_list[0][3] 
        
        # Sort CDS features by genomic position
        # This ensures exons are concatenated in the correct order
        if strand == '+':
            cds_list.sort(key=lambda x: x[1])  # Sort by start position (ascending), x is the tuple
        else:
            cds_list.sort(key=lambda x: x[1], reverse=True)  # Reverse for minus strand
        
        # Build complete CDS sequence by concatenating exons
        cds_seq = ""
        
        for i, (chrom, start, end, _, phase) in enumerate(cds_list): 
            # Extract sequence for this CDS segment (exon)
            segment = str(genome[chrom].seq[start:end])
            
            # Apply phase offset ONLY to the first CDS segment
            # Phase indicates how many nucleotides to skip at the start
            # to reach the correct reading frame, everything downstream is already correct
            if i == 0 and phase > 0:
                if strand == '+':
                    segment = segment[phase:] #cut at the start
                else:
                    segment = segment[:-phase] #cut at the end
                phase_applied_count += 1
            cds_seq += segment
        
        # Reverse complement if gene is on minus strand
        if strand == '-':
            cds_seq = str(Seq(cds_seq).reverse_complement())
        
        # Ensure CDS length is a multiple of 3 
        remainder = len(cds_seq) % 3
        if remainder != 0:
            # Drop incomplete codon at the end
            cds_seq = cds_seq[:-remainder]  
        
        # Translate CDS to protein
        try: #doesnt stop if fails goes to exception 
            # Translate and stop at first stop codon
            protein_seq = str(Seq(cds_seq).translate(to_stop=True))
            
            # Handle cases with very short proteins or internal stops
            if len(protein_seq) < 10:
                # Try translating without stopping
                protein_seq = str(Seq(cds_seq).translate())
                if '*' in protein_seq:
                    # Truncate at first stop codon
                    protein_seq = protein_seq.split('*')[0] #only want sequence infront of stop
            
            # Only keep proteins with reasonable length
            if len(protein_seq) >= 10:
                proteins[gene_id] = protein_seq
        except Exception as e:
            translation_errors += 1
            if translation_errors <= 5:
                print(f"Warning: Could not translate {gene_id} ({transcript_id}): {e}")
                print(f"  CDS length: {len(cds_seq)} bp, CDS segments: {len(cds_list)}, Strand: {strand}")
    
    print(f"Successfully translated {len(proteins)} genes")
    print(f"  Multi-exon genes (with introns): {multi_exon_count}")
    print(f"  Applied phase offset: {phase_applied_count} transcripts")
    if translation_errors > 0:
        print(f"  Translation errors: {translation_errors} genes")
    
    return proteins

def read_tracking_non_exact(tracking_file):
    non_exact = []
    with open(tracking_file, 'r') as f:
        for line in f:
            fields = line.rstrip("\n").split('\t')
            if len(fields) < 5:
                continue

            class_code = fields[3]
            if class_code == '=':
                continue

            # Query gene 
            query_info = fields[2]
            query_gene = query_info.split('|')[0] if query_info else None

            # Reference gene 
            ref_info = fields[4]
            if 'q1:' not in ref_info:
                continue
            ref_gene = ref_info.split('q1:')[1].split('|')[0]

            if query_gene and ref_gene:
                non_exact.append((query_gene, ref_gene, class_code))

    print(f"Found {len(non_exact)} non-exact matches")
    return non_exact


def compare_proteins(protein1, protein2):
  
    if protein1 == protein2:
        return {
            'identity': 100.0,
            'matches': len(protein1),
            'alignment_length': len(protein1),
            'protein1_length': len(protein1),
            'protein2_length': len(protein2),
            'length_diff': 0,
            'length_ratio': 1.0
        }
    
    # Perform global alignment with match/mismatch scoring
    alignments = pairwise2.align.globalms(protein1, protein2, 
                                           2,    # match score
                                           -1,   # mismatch score
                                           -0.5, # gap open
                                           -0.1) # gap extend
    
    if not alignments:
        return None
    
    best_alignment = alignments[0]
    aligned1 = best_alignment.seqA
    aligned2 = best_alignment.seqB  #includes the gaps
    
    # Calculate identity across entire alignment (including gaps)
    matches = sum(a == b for a, b in zip(aligned1, aligned2))
    alignment_length = len(aligned1)
    identity = (matches / alignment_length) * 100 if alignment_length > 0 else 0
    
    len1 = len(protein1)
    len2 = len(protein2)
    
    return {
        'identity': identity,
        'matches': matches,
        'alignment_length': alignment_length,
        'protein1_length': len1,
        'protein2_length': len2,
        'length_diff': abs(len1 - len2),
        'length_ratio': min(len1, len2) / max(len1, len2) if max(len1, len2) > 0 else 0
    }

# 7G8-2019 annotations 
native_7G8_gff = "Lift_Off/LiftOff_Output/pf7G8-2019/gff_compare_out/orf_analysis/protein_comparison/PlasmoDB-68_Pfalciparum7G8-2019.gff"
native_7G8_fasta = "Lift_Off/LiftOff_Output/pf7G8-2019/gff_compare_out/orf_analysis/protein_comparison/PlasmoDB-68_Pfalciparum7G8-2019_Genome (2).fasta"

# 3D7 annotations lifted to 7G8-2019 coordinates
lifted_3D7_gff = "Lift_Off/LiftOff_Output/pf7G8-2019/pf7G8-2019_liftover.gff3"
lifted_3D7_fasta = "Lift_Off/LiftOff_Output/pf7G8-2019/gff_compare_out/orf_analysis/protein_comparison/PlasmoDB-68_Pfalciparum7G8-2019_Genome (2).fasta"

tracking_file = "Lift_Off/LiftOff_Output/pf7G8-2019/gff_compare_out/orf_analysis/pf7G8-2019_filtered_valid_orf.tsv"
output_dir = "Lift_Off/LiftOff_Output/pf7G8-2019/gff_compare_out/orf_analysis/protein_comparison"

print("="*70)
print("Protein sequence comparison")
print("="*70)

# Extract proteins from 7G8-2019 annotations
native_7G8_proteins = parse_liftoff_gff_get_sequences(native_7G8_gff, native_7G8_fasta)

# Extract proteins from 3D7 liftoff annotations
lifted_3D7_proteins = parse_liftoff_gff_get_sequences(lifted_3D7_gff, lifted_3D7_fasta)

non_exact = read_tracking_non_exact(tracking_file)

results = []
compared_count = 0

for query_gene, ref_gene, class_code in non_exact:
    native_7G8_prot = native_7G8_proteins.get(query_gene)
    lifted_3D7_prot = lifted_3D7_proteins.get(ref_gene)
    
    if not native_7G8_prot and not lifted_3D7_prot:
        results.append({
            'query_gene': query_gene,
            'ref_gene': ref_gene,
            'class_code': class_code,
            'status': 'both_missing',
            'identity': None,
            'query_length': 0,
            'ref_length': 0,
            'length_diff': None,
            'length_ratio': None
        })
        continue
    
    if not lifted_3D7_prot:
        results.append({
            'query_gene': query_gene,
            'ref_gene': ref_gene,
            'class_code': class_code,
            'status': 'ref_missing',
            'identity': None,
            'query_length': len(native_7G8_prot),
            'ref_length': 0,
            'length_diff': None,
            'length_ratio': None
        })
        continue
    
    if not native_7G8_prot:
        results.append({
            'query_gene': query_gene,
            'ref_gene': ref_gene,
            'class_code': class_code,
            'status': 'query_missing',
            'identity': None,
            'query_length': 0,
            'ref_length': len(lifted_3D7_prot),
            'length_diff': None,
            'length_ratio': None
        })
        continue
    
    compared_count += 1
    
    # Compare protein sequences
    comparison = compare_proteins(native_7G8_prot, lifted_3D7_prot)
    
    if comparison:
        results.append({
            'query_gene': query_gene,
            'ref_gene': ref_gene,
            'class_code': class_code,
            'status': 'compared',
            'identity': comparison['identity'],
            'query_length': comparison['protein1_length'],  
            'ref_length': comparison['protein2_length'],    
            'length_diff': comparison['length_diff'],
            'length_ratio': comparison['length_ratio']
        })
    else:
        results.append({
            'query_gene': query_gene,
            'ref_gene': ref_gene,
            'class_code': class_code,
            'status': 'alignment_failed',
            'identity': None,
            'query_length': len(native_7G8_prot),
            'ref_length': len(lifted_3D7_prot),
            'length_diff': None,
            'length_ratio': None
        })

print(f"Compared {compared_count} protein pairs")

# Save results to TSV
results_df = pd.DataFrame(results)
output_file = os.path.join(output_dir, "pf7G8-2019_protein_comparison_non_exact.tsv")
results_df.to_csv(output_file, sep='\t', index=False)
   

# Protein identity statistics
compared = results_df[results_df['status'] == 'compared']
if len(compared) > 0:
    print(f"\n=== Protein Identity Statistics (n={len(compared)}) ===")
    print(f"Mean identity: {compared['identity'].mean():.2f}%")
    print(f"Median identity: {compared['identity'].median():.2f}%")
    print(f"Min identity: {compared['identity'].min():.2f}%")
    print(f"Max identity: {compared['identity'].max():.2f}%")
    print(f"Std deviation: {compared['identity'].std():.2f}%")
    

    # By class code
    print(f"\n=== By Class Code ===")
    for code in sorted(compared['class_code'].unique()):
        subset = compared[compared['class_code'] == code]
        print(f"  {code}: n={len(subset):3d}, mean={subset['identity'].mean():6.2f}%, median={subset['identity'].median():6.2f}%, min={subset['identity'].min():6.2f}%")
