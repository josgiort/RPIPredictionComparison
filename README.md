# Master project
This is a documentation repository for a master project from the univerisity of freiburg

<img src="https://github.com/user-attachments/assets/23612e45-d64b-456c-9c4e-c5bd4662c32c" alt="university" width="500"/>


### Objective of the master project


This project explores the use of deep learning models for predicting RNA–protein
interactions (RPIs). We observed the performance of an RPI classifier. We
prepared a RPI dataset with the RNAcompete methodology for observing
how AlphaFold3 differentiates RPIs within some of its confidence metrics.
We used TabPFN to classify RPIs by also using the prepared dataset for
in-context learning at inference time. Results demonstrate that the classifier
might still need more generalization capabilities, AlphaFold3 can recognize
sequence level signals of RNA-protein binding and TabPFN can succeed at
RPI recognition given the right feature set.

Structured project outlook

PART 1 Examining RPIEmbeddor performance on RPI examples 1

The test set of the RPIEmbeddor tool was used to validate the predictions on it and obtain some performance metrics on this test set.
Also we evaluated the prediction behavior of the RPIEmberddor tool (Matus, D. et al, 2024) on a set of validated RPI examples.


PART 2 Comparing the AlphaFold3 output metrics distributions between RPI positives and negatives examples


PART 3 Classifying RNA-Protein Interactions with TabPFN and AlphaFold3



### Install environment

##### Install bedtools

apt-get install bedtools
