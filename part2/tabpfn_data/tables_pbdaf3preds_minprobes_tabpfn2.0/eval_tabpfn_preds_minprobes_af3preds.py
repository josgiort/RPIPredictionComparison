from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from prettytable import PrettyTable

def read_csv(file_path: Path) -> pd.DataFrame:
    """Reads a CSV file into a pandas DataFrame."""
    return pd.read_csv(file_path)

# Define data parameters
data_dir = Path('')
num_features = 277
splits = ['random', 'uniprot']  # Different splits
versions = ['full', 'seq', 'no_kmer']  # Different versions

# Prepare table for aggregated results
table = PrettyTable()
table.field_names = ["Split", "Version", "Accuracy", "Precision", "Recall", "F1 Score", "ROC AUC"]

# Loop over all combinations of split and version
for split in splits:
    for version in versions:
        try:
            # Load ground truth and predictions
            gt_path = data_dir / f'split_{split}_{num_features}_features_test_{version}.csv'
            preds_path = data_dir / f'tabpfn_preds_{split}_{num_features}_features_test_{version}.csv'

            gt = read_csv(gt_path)
            preds = read_csv(preds_path)

            # Keep only relevant columns
            preds = preds[['Id', 'interaction_prob_0', 'interaction_prob_1']]
            # preds = preds[['interaction_prob_0', 'interaction_prob_1']]
            eval_df = gt.merge(preds, on='Id', how='left')[['Id', 'interaction_prob_0', 'interaction_prob_1', 'interaction']]
            # eval_df = gt.merge(preds, on='Id', how='left')[['interaction_prob_0', 'interaction_prob_1', 'interaction']]

            # Compute predicted labels
            eval_df['pred'] = np.where(eval_df['interaction_prob_1'] > 0.5, 1, 0)

            # Compute classification metrics
            accuracy = accuracy_score(eval_df['interaction'], eval_df['pred'])
            precision = precision_score(eval_df['interaction'], eval_df['pred'])
            recall = recall_score(eval_df['interaction'], eval_df['pred'])
            f1 = f1_score(eval_df['interaction'], eval_df['pred'])
            roc_auc = roc_auc_score(eval_df['interaction'], eval_df['interaction_prob_1'])

            # Add results to the table
            table.add_row([split, version, f"{accuracy:.4f}", f"{precision:.4f}", f"{recall:.4f}", f"{f1:.4f}", f"{roc_auc:.4f}"])

            # Generate confusion matrix
            conf_matrix = confusion_matrix(eval_df['interaction'], eval_df['pred'])

            # Plot confusion matrix
            plt.figure(figsize=(6, 5))
            sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", xticklabels=["Pred 0", "Pred 1"], yticklabels=["True 0", "True 1"])
            plt.xlabel("Predicted Label")
            plt.ylabel("True Label")
            plt.title(f"Confusion Matrix: {split} - {version}")
            plt.show()

        except FileNotFoundError as e:
            print(f"⚠️ Missing file: {e}")

# Print final summary of results
print("\nAggregated Binary Classification Metrics:")
print(table)
