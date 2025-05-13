import matplotlib.pyplot as plt
from collections import defaultdict
from Bio import SeqIO
import os


def count_kmers(sequence, k):
    """Count all k-mers in the given sequence."""
    kmer_counts = defaultdict(int)
    for i in range(len(sequence) - k + 1):
        kmer = sequence[i:i + k]
        kmer_counts[kmer] += 1
    return kmer_counts


def plot_top_kmers(kmer_counts, top_n=10):
    """Plot the top N most frequent k-mers."""
    sorted_kmers = sorted(kmer_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
    kmers, counts = zip(*sorted_kmers)

    os.makedirs("plots", exist_ok=True)

    plt.figure(figsize=(10, 6))
    plt.bar(kmers, counts, color='skyblue')
    plt.xlabel('3-mers')
    plt.ylabel('Frequency')
    plt.title(f'Top {top_n} Most Frequent 3-mers in UniProtKB (reviewed:true, organism_id:9606, annotation:"RNA binding")')
    plt.xticks(rotation=45)
    plt.savefig("plots/Freq_3mers_uniProtK.pdf")
    # plt.show()


def main(fasta_file, k=3, top_n=10):
    """Main function to process the FASTA file and plot the most frequent k-mers."""
    sequence = ""
    for record in SeqIO.parse(fasta_file, "fasta"):
        sequence += str(record.seq).upper()  # Ensure the sequence is in uppercase

    kmer_counts = count_kmers(sequence, k)
    plot_top_kmers(kmer_counts, top_n)


if __name__ == "__main__":
    fasta_file = "uniprotkb.fasta"  # Replace with your FASTA file path
    main(fasta_file, k=3, top_n=25)