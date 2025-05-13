import csv

def convert_txt_to_csv(input_txt, output_csv):
    out_dir = input_txt.split("_")[0] + "_outputs"

    headers = ["prot_seq", "prot_len", "rna_seq_id", "rna_seq", "rna_len", "gt", "pred", "pred_prob"]

    with open(out_dir + "/" + input_txt, "r") as infile, open(out_dir + "/" + output_csv, "w", newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(headers)  # Write headers
        
        for line in infile:
            fields = line.strip().split("\t")
            if len(fields) != 8:
                print("Skipping malformed line:", line)
                continue
            writer.writerow(fields)

    return output_csv

if __name__ == "__main__":
    # Example usage
    convert_txt_to_csv("example1_result.txt", "example1_result.csv")