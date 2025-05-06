# AI4NA_AF3_eval
A repository for evaluations of AlphaFold3 predicitons for RNA-Protein interactions

## Installation
Make a new conda environment with ```conda create -n ai4na_af3_eval python=3.10``` and activate it with ```conda activate ai4na_af3_eval```. 

Then run ```pip install pandas matplotlib plotly```.

## Run example script
```
python -m example
```

## Generate plots of part two

Run:
```
chmod +x generate_plots.sh
```
Then
...
./generate_plots.sh
...
## Generate pLDDT density comparison between two datasets (RNACompete maxprobes and minprobes)
The pLDDT's values are set in bins.
The densities sum up to 1.0

Just run:
```
python compare_plddt.py
```



## Generate PAE density comparison between two datasets (RNACompete maxprobes and minprobes)
The PAE's values are set in bins.
The densities sum up to 1.0

Just run:
```
python compare_pae.py
```





## TabPFN Playground
We also provide a playground for classification of RPI using tabPFN API.
To generate a csv file with features for tabPFN pedictions, run
```
python prepare_tabpfn_data.py
```
The script generates 3 versions of test and training csvs for the TabPFN API:
- **full** with all 5mer count features (limited by the number of top 5mers to use)
- **seq** with only RNA and protein sequences in there
- **no_kmer** with some features but without the features computed from the 5mer counts.
And two different splits, **random** and **uniprot**, either split at random or based on uniprot ids.

After having run predictions for the testset in the tabPFN API (using the generated train set as training table on top of the API), you can save the csv as
```
f'tabpfn_preds_{split}_{num_features}_features_test_{version}.csv'
```
Currently, the TabPFN API can only handle the data with 159 features (15 top 5mers) that is in the ```tabpfn_data``` directory.

You can evaluate the predictions by running
```
python eval_tabpfn_preds.py
```
