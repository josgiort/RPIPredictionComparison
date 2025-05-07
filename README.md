# Master project
This is a documentation repository for a master project from the University of Freiburg

<img src="https://github.com/user-attachments/assets/23612e45-d64b-456c-9c4e-c5bd4662c32c" alt="university" width="300"/>

## Abstract

This project explores the use of deep learning models for predicting RNA–protein
interactions (RPIs). We observed the performance of an RPI classifier. We
prepared a RPI dataset with the RNAcompete methodology for observing
how AlphaFold3 differentiates RPIs within some of its confidence metrics.
We used TabPFN to classify RPIs by also using the prepared dataset for
in-context learning at inference time. Results demonstrate that the classifier
might still need more generalization capabilities, AlphaFold3 can recognize
sequence level signals of RNA-protein binding and TabPFN can succeed at
RPI recognition given the right feature set.


## "Analysis of RNA-Protein complexes predicted with deep learning"

The driving biological actors of this project are the RNA-Protein Interactions (RPIs), as they hold tremendous importance in life.

In light of the recent thriving of deep learning-driven prediction tools for molecules alone, the next big step in this domain would be modeling interactions between them. However, realizing such a task is significantly more challenging due to the complexity of binding, folding, and dynamics.

In the following project, we focus on using and evaluating domain-specific deep learning models which can help describe and understand RPIs by modeling and classifying them.

We made use of the following tools:

### AlphaFold3

AlphaFold3 [Abramson et al., 2024] is the latest version of DeepMind’s protein structure prediction system, now expanded to model not only individual proteins but also protein–protein, protein–RNA, and other biomolecular complexes. 
In this project, AlphaFold3 was considered as a structural resource to identify points suggesting RPIs within the sequences and to get an impression on how correct its predictions can be on RPIs.

### RNACompete: A Methodology to Derive Positive and Negative RPI Examples

**RNAcompete** [Ray et al., 2017] is a high-throughput experimental platform designed to systematically measure the binding preferences of RNA-binding proteins (RBPs) against synthetic RNA sequences. It provides quantitative binding affinity scores between a protein and numerous RNA sequences.
We utilized the RNAcompete dataset to generate positive and negative examples for evaluation. Specifically, we selected proteins and extracted six RNA–protein interaction examples per protein: the three RNA sequences with the highest binding energies (strong interaction, labeled positive) and the three with the lowest (weak or no interaction, labeled negative).  

### RPIembeddor

**RPIembeddor** [Matus et al., 2024] is a novel transformer-based model designed for classifying ncRNA–protein interactions. It accepts two sequences — a protein amino acid sequence and an RNA nucleotide sequence — each of up to 1022 characters in length.  
The program outputs whether the two sequences interact by printing either **"POSITIVE INTERACTION"** or **"NEGATIVE INTERACTION"** to the console.

### TabPFN

**TabPFN** [Hollmann et al., 2025] (Tabular Prior-Data Fitted Network) is a pretrained transformer model for tabular data classification.  
It requires no training on the target dataset and can directly perform inference by leveraging prior knowledge learned from millions of synthetic tasks.
In this project, TabPFN was used to classify RNA–protein interactions (RPIs) as positive or negative.  
Feature tables were built from the RPI examples, and TabPFN was applied to provide a deep learning benchmark without task-specific training.



## Structured project outlook

### PART 1 Examining RPIEmbeddor performance on RPI examples 1

The test set of the RPIEmbeddor tool was used to validate the predictions on it and obtain some performance metrics on this test set.
Also we evaluated the prediction behavior of the RPIEmberddor tool (Matus, D. et al, 2024) on a set of validated RPI examples.

### PART 2 Comparing the AlphaFold3 output metrics distributions between RPI positives and negatives examples

### PART 3 Classifying RNA-Protein Interactions with TabPFN and AlphaFold3


## Reproducing results

<pre><pre>### Part one: Examining RPIEmbeddor performance on RPI examples 1</pre></pre>

Enter the folder "part1"

Enter the folder "dataset_predictions"

There run:

<pre>python pred_embeddor.py</pre>

And then:

<pre>python ConfusionMatrix.py</pre>

File "dataset_inference.txt" contains the TS-Fam testing set of RPIembeddor.
With the first program, RPIembeddor is run on the sequences of TS-Fam and the predictions are stored in "result_table.txt".
Then from this last file the confusion matrix is created and the metrics are obtained with the second program.


Also:

Enter the folder "part1"

There run:
<pre>python FormatForInference.py 3 example1.fasta output_example1.txt</pre>

And then:

<pre>python PredictRPIEmbeddor.py output_example1.txt result_example1.txt</pre>

Please refer to "preprocessing_script.pdf" for more details on the working of this script.



### Install environment

##### Install bedtools

<pre>apt-get install bedtools</pre>


### Part two: 
