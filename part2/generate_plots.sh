#!/bin/bash

# Set PYTHONPATH to the current working directory
export PYTHONPATH=$(pwd)

# Directory to search (you can customize this path)
TARGET_DIR="plot_scripts/minprobes_af3pdbpreds"

# Find and run all .py files in the directory (non-interactively)
find "$TARGET_DIR" -type f -name "*.py" | while read -r script; do
    echo "Running $script..."
    python "$script"
    if [ $? -ne 0 ]; then
        echo "Error running $script"
    fi
    echo "Finished $script"
    echo "------------------------"
done



# Directory to search (you can customize this path)
TARGET_DIR="plot_scripts/rnacmpt_augmented"

# Find and run all .py files in the directory (non-interactively)
find "$TARGET_DIR" -type f -name "*.py" | while read -r script; do
    echo "Running $script..."
    python "$script"
    if [ $? -ne 0 ]; then
        echo "Error running $script"
    fi
    echo "Finished $script"
    echo "------------------------"
done

