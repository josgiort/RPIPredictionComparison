import pandas as pd
import plotly.express as px

from pathlib import Path
from matplotlib import pyplot as plt

def kmercount_comparison_barplot(data):
    """
    Create a barplot of the kmer counts with bars next to each other.
    """
    kmer, dataset, count = zip(*data)
    df = pd.DataFrame({'kmer': kmer, 'dataset': dataset, 'count': count})
    
    fig = px.bar(df, x='kmer', y='count', color='dataset', title='Kmer counts')
    
    fig.update_layout(barmode='group')
    
    fig.show()    
    


def two_dataset_diagonal_scatter_plot(df1, df2, path1, path2, opacity=0.5):
    # Merge both datasets to align trimers appearing in either dataset
    merged_counts = pd.merge(df1, df2, on='kmer', how='outer').fillna(0)
    
    # Ensure axes have natural numbers
    max_count = int(max(merged_counts['count_' + path1.split("/")[-1].split(".")[0]].max(), merged_counts['count_' + path2.split("/")[-1].split(".")[0]].max()))
    tick_vals = list(range(0, max_count + 1, max(1, max_count // 10)))
    
    # Create scatter plot
    fig = px.scatter(
        merged_counts,
        x='count_' + path1.split("/")[-1].split(".")[0],
        y='count_' + path2.split("/")[-1].split(".")[0],
        hover_name="kmer",  # Show trimer pairs in hover tooltip
        hover_data={
            'count_' + path1.split("/")[-1].split(".")[0]: True,
            'count_' + path2.split("/")[-1].split(".")[0]: True,
            'normalized_' + path1.split("/")[-1].split(".")[0]: True,
            'normalized_' + path2.split("/")[-1].split(".")[0]: True,
        },
        title="Comparison of ALL Trimer Pairs: " + path1.split("/")[-1].split(".")[0] +" vs " + path2.split("/")[-1].split(".")[0],
        labels={'count_' + path1.split("/")[-1].split(".")[0]: 'Counts in ' + path1.split("/")[-1].split(".")[0], 'count_' + path2.split("/")[-1].split(".")[0]: 'Counts in ' + path2.split("/")[-1].split(".")[0]},
        opacity=opacity
    )
    
    # Add diagonal reference line
    fig.add_shape(
        type="line",
        x0=0, y0=0,
        x1=max_count, y1=max_count,
        line=dict(color="black", width=2, dash="dash")
    )
    
    # Ensure natural number ticks
    fig.update_layout(
        xaxis=dict(tickmode='array', tickvals=tick_vals),
        yaxis=dict(tickmode='array', tickvals=tick_vals)
    )
    
    # Display interactive plot
    fig.show()
