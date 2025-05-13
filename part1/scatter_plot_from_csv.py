import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_rna_len_vs_pred_prob(csv_file):
    # Read the CSV file
    out_dir = csv_file.split("_")[0] + "_outputs"
    df = pd.read_csv(out_dir + "/" + csv_file)

    # Convert necessary columns to numeric (in case they're not)
    df['rna_len'] = pd.to_numeric(df['rna_len'], errors='coerce')
    df['pred_prob'] = pd.to_numeric(df['pred_prob'], errors='coerce')

    # Drop rows with NaN values
    df = df.dropna(subset=['rna_len', 'pred_prob'])

    # Create scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(df['rna_len'], df['pred_prob'], alpha=0.6, edgecolors='k', label='Data Points')

    # Plot threshold line at 0.5
    plt.axhline(y=0.5, color='red', linestyle='--', label='Threshold = 0.5')

    # Fit and plot trendline (linear regression)
    z = np.polyfit(df['rna_len'], df['pred_prob'], 1)
    p = np.poly1d(z)
    plt.plot(df['rna_len'], p(df['rna_len']), color='blue', linestyle='-', linewidth=2, label='Trendline')

    # Labels and title
    plt.xlabel("RNA Sequence Length")
    plt.ylabel("Prediction Probability")
    plt.title("RNA Length vs. Prediction Probability")
    plt.legend()
    plt.grid(True)

    # Save plot
    plt.tight_layout()
    plt.savefig(out_dir + "/" + csv_file.split("_")[0] + "_scatter_plot.png")

if __name__ == "__main__":
    # Example usage
    plot_rna_len_vs_pred_prob("example1_result.csv")

