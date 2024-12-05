# conda activate /net/projects/chai-lab/miniconda3/envs/cxr-green
# Successfully run metrics without green on (4) A40 GPU
# Input: gt_imp_sample.csv; gen_imp_sample.csv. Each csv needs two columns ['study_id', 'report']. 
# Each column needs to be str and 'study_id' should not include characters except numbers.
# Ensure each input csv has no empty values.
# Output (without green): metrics.csv; metrics_avg.csv
# python test.py --gt_csv /net/projects/chacha/cxr_eval/test/gt_imp_sample.csv --gen_csv /net/projects/chacha/cxr_eval/test/gen_imp_sample_3_1.csv --output_metrics_Nogreen /net/projects/chacha/cxr_eval/results/metrics.csv --output_combined /net/projects/chacha/cxr_eval/results/metrics_w_green.csv --output_dir /net/projects/chacha/cxr_eval/results

import argparse
import os
import pandas as pd
from CXRMetric.run_eval import calc_metric
from CXRMetric.test_GREEN import green_main

def combine_csv(csv_path_1, csv_path_2, output_path): # TO-DO: delete this function and merge this step into calc_metric function
    df1 = pd.read_csv(csv_path_1)
    df2 = pd.read_csv(csv_path_2)
    df = pd.concat([df1, df2], axis=1)
    df.to_csv(output_path, index=False)

def parse_args():
    parser = argparse.ArgumentParser(description="CXR Metric Evaluation Script")
    
    parser.add_argument('--gt_csv', help="Path to the groundtruth CSV file")
    parser.add_argument('--gen_csv', help="Path to the generated CSV file")
    parser.add_argument('--output_metrics_Nogreen', help="Path to output metrics CSV file except green")
    parser.add_argument('--output_combined', help="Path to output metrics CSV file with green")
    parser.add_argument('--green_model', default="StanfordAIMI/GREEN-radllama2-7b",
                        help="Model to use for green_main function")
    parser.add_argument('--output_dir', help="Directory for output files")
    # Add argument for the column name (defaults to "report")
    parser.add_argument('--column_name', default="report",
                        help="Column name in the CSV files to be used in the green_main function")

    # decide whether to add GREEN
    parser.add_argument('--if_green', action='store_true', default=False,
                        help='Calculation of GREEN might take some time and is only suitable for cxr-green environment. Please decide whether to involve it.')
    # decide whether to add BertScore
    parser.add_argument('--if_bert', action='store_true', default=False,
                        help='Calculation of BertScore might take some time and is only suitable for cxr-green environment. Please decide whether to involve it.')
    # decide whether to add RadGraph
    parser.add_argument('--if_radgraph', action='store_true', default=False,
                        help='Calculation of RadGraph F1 might take some time and is only suitable for cxr_eval environment. Please decide whether to involve it.')   


    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    # Automatic metric calculation
    calc_metric(args.gt_csv, 
                args.gen_csv, 
                args.output_metrics_Nogreen, 
                use_idf=False, 
                if_bert=args.if_bert, 
                if_radgraph=args.if_radgraph)

    # GREEN calculation # TO-DO: merge GREEN calculation into calc_metric(); codes after if __name__ == "__main__": should only contain args and calc_metric()
    if args.if_green:
        try:
            green_main(args.gt_csv, args.gen_csv, args.column_name, args.model, args.output_dir)

            # Output evaluation results with green
            csv_path_1 = args.output_metrics_Nogreen
            csv_path_2 = args.output_dir + "/results_green.csv"
            combine_csv(csv_path_1, csv_path_2, args.output_combined)
        except OSError as e:
            print(f"Error: {e}")
