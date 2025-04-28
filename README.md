# Master project
This is a documentation repository for a master project from the univerisity of freiburg

<img src="https://github.com/user-attachments/assets/23612e45-d64b-456c-9c4e-c5bd4662c32c" alt="university" width="300"/>


### Abstract

This project explores the use of deep learning models for predicting RNA–protein
interactions (RPIs). We observed the performance of an RPI classifier. We
prepared a RPI dataset with the RNAcompete methodology for observing
how AlphaFold3 differentiates RPIs within some of its confidence metrics.
We used TabPFN to classify RPIs by also using the prepared dataset for
in-context learning at inference time. Results demonstrate that the classifier
might still need more generalization capabilities, AlphaFold3 can recognize
sequence level signals of RNA-protein binding and TabPFN can succeed at
RPI recognition given the right feature set.




The driving biological actors of this work are the RNA-Protein Interactions (RPIs), as their hold tremendous importance in life.

In light of the recent thriving of deep learning driven prediction tools for molecules alone, the next big step in this domain would mean modeling interactions between them.
However, realizing such a task is significantly more challenging due to the complexity of binding folding and dynamics.


In the following work, we focus on using and evaluating domain-specific deep learning models which can help to describe and understand RPIs by modelling and classifying them.

The term "molecules" will also refer to either protein residues, protein aminoacids or RNA nucleotides; to denote biological entities at a greater scale than atoms.

The following concepts were of great use for the evaluations made:

\section{AlphaFold3}
AlphaFold3 \cite{Abramson2024} is the latest version of DeepMind’s protein structure prediction system, now expanded to model not only individual proteins but also protein–protein, protein–RNA, and other biomolecular complexes. 
Recently, it has gained the attention of the community for its accurate predictions on proteins alone. However, it is believed that its modeling capabilities still lack accuracy regarding some other bio-molecules and multi-molecular complexes, and therefore, more caution must be put when working with these.

In this work, AlphaFold3 was considered as a structural resource to identify points suggesting RPI within the sequences. Also, to get an impression on how correct its predictions can be on RPIs.


\subsection{PAE}
PAE (Predicted Aligned Error) is a metric of relative positional confidence between pairs of molecules (protein residues, RNA nucleotides, etc.) from the predicted structure.
More specifically, PAE(A,B) tells how much misplaced (expected positional error in Angstroms) a molecule B is with respect to the frame of reference of another molecule A, and this is calculated from each molecule's frame of reference (so the other case is PAE(B,A) for this pair of molecules). The errors can differ slightly between the two cases as a result of possible disordered regions involving any of the two molecules.


The PAE is provided in a square matrix with dimension number of residues plus number of nucleotides  in an AlphaFold3 output JSON file.


\subsection{pLDDT}

pLDDT (predicted Local Distance Difference Test) is a per-atom metric of local confidence. It is scaled from 0 to 100, with higher scores indicating higher confidence. It measures the expected local accuracy for the atoms of a given molecule. The pLDDT is provided in a one dimensional array with dimension number of atoms in an AlphaFold3 output JSON file.



\section{Distance matrix}
In several parts of this work, we leverage AlphaFold3 RPI complex predictions by creating a distance matrix between all of their protein residues and RNA nucleotides.

This matrix (with dimensions number of residues by number of nucleotides) is a crucial component.
From it, residue - nucleotide pairs being within five Angstroms from each other are identified, which can imply potential RPI points.

A cell in the matrix represents the shortest possible distance, in Angstroms, for a given residue-nucleotide pair. The distance is taken as the simple euclidean distance between the closest two atoms in the pair. For atom selection, all non-heavy atoms (i.e. Hydrogen atoms) are ignored.

The original matrix shape of the confidence metrics had to be adapted to match the molecule-wise format of the distance matrix.

The figure 1.1 provides the graphical representation of this matrix, with a colorheat map for the distances and the red dots indicating residue-nucleotide pairs at five Angstroms or less from each other.




\begin{figure}[h!]
    \centering
    \includegraphics[width=0.7\textwidth]{chapters/intro_imgs/example_dist_matrix.pdf} % adjust width as needed
    \caption{Distance matrix between residues and nucleotides of a RPI example}
    \label{fig:myplot}
\end{figure}

For example, there seems to be close enough pairs between the first five nucleotides and the first fifty residues in this RPI example.

Also in figure 1.1 the pLDDT and PAE confidence metrics are plotted to the left and upper sides of the distance matrix, likewise with a color heatmap, to illustrate what the 
prediction confidence is throughout the residues and nucleotides.




The close pairs later on are exported into a CSV file to carry out further evaluations on them.



\section{RNACompete: a powerful methodology to derive RPI positives and negatives examples}

RNAcompete \cite{ray2017rnacompete} is a high-throughput experimental platform designed to systematically measure the binding preferences of RNA-binding proteins (RBPs) against synthetic RNA sequences. It provides quantitative binding affinity scores between a given protein and numerous RNA sequences.

We utilized the RNAcompete dataset to generate positive and negative examples required for the evaluations in this work. Specifically, we selected the protein from the RNACompete dataset and extracted six RNA–protein interaction examples: the three RNA sequences with the highest binding energies (indicating strong interaction, labeled as positive) and the three with the lowest binding energies (indicating weak or no interaction, labeled as negative). 
In all six cases, the protein sequence remained constant, while only the RNA sequences varied.

We did this on 244 RNAcompete proteins, to get a total of 1464 RPI examples.

This approach allowed us to create a balanced and biologically meaningful dataset of interaction data.




\section{RPIembeddor}

RPIembeddor is a a novel transformer-based model designed for classifying ncRNA-protein interactions \cite{matus2024rna}. The input for this are two sequences: one protein aminoacid sequence and one RNA nucleotide sequence. Both of them must be at most 1022 characters in length.
The program asks the user for each of the sequences and then predicts whether they both are interacting by printing ``POSITIVE INTERACTION'' or ``NEGATIVE INTERACTION'' in the console.

\section{bedtools}

``bedtools'' \cite{quinlan2010bedtools} is a suite of methods for a wide-range of genomics analysis tasks. It allows to intersect, merge, count, complement, and shuffle genomic intervals from multiple files in widely-used genomic file formats such as BAM, BED, VCF.

The specific method we used was ``getfasta''.

With this, we extracted DNA sequences from a reference genome based on coordinates specified in a BED file. For example:

\begin{center}
\begin{verbatim}

Input:
A BED file containing genomic regions (e.g., chromosome, start, end).
A reference genome file in FASTA format.

Process:
The tool reads the coordinates from the BED file.
It extracts the corresponding DNA sequences from the reference genome.

Output:
A FASTA file containing the extracted sequences, 
with headers derived from the BED file.

\end{verbatim}
\end{center}



\section{FASTA}

A FASTA file is a text format used to store nucleotide or protein sequences. It consists of one or more entries, each starting with a header line (preceded by $>$), followed by the sequence itself. The header typically contains an identifier and optional descriptors.

\section{TabPFN}

TabPFN (Tabular Prior-Data Fitted Network) \cite{hollmann2025accurate} is a pretrained transformer-based model designed for tabular data classification. It requires no training on the target dataset and can directly perform inference by leveraging prior knowledge learned from millions of synthetic tasks. In this project, TabPFN was used as an additional model to classify RNA–protein interactions (RPIs) as positive or negative. RPI examples were encoded into feature tables, and TabPFN was applied to evaluate its performance in predicting interactions, providing a deep learning-based benchmark without the need for task-specific training.








Structured project outlook

PART 1 Examining RPIEmbeddor performance on RPI examples 1

The test set of the RPIEmbeddor tool was used to validate the predictions on it and obtain some performance metrics on this test set.
Also we evaluated the prediction behavior of the RPIEmberddor tool (Matus, D. et al, 2024) on a set of validated RPI examples.


PART 2 Comparing the AlphaFold3 output metrics distributions between RPI positives and negatives examples


PART 3 Classifying RNA-Protein Interactions with TabPFN and AlphaFold3


### Reproducing results

### Part one

Enter the folder "dataset_predictions"

There run:
python pred_embeddor.py

And then:
python ConfusionMatrix.py

File "dataset_inference.txt" contains the TS-Fam testing set of RPIembeddor
With the first program, RPIembeddor is run on the sequences of TS-Fam and the predictions are stored in "result_table.txt"
Then from this last file the confusion matrix is created and the metrics are obtained with the second program.


### Install environment

##### Install bedtools

apt-get install bedtools
