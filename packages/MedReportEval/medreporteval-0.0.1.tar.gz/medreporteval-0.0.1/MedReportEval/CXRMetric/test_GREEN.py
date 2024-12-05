import os
import pandas as pd
from .green import compute

# Constants for column names
STUDY_ID_COL_NAME = "study_id"  # Modify according to actual situation
REPORT_COL_NAME = "report"  # Modify according to actual situation

def extract_reports_to_list(gt_csv_path, pred_csv_path, report_col_name):
    """Extracts and formats reports from gt_csv and pred_csv."""
    
    # Cache file paths
    cache_gt_csv = os.path.join(os.path.dirname(gt_csv_path), f"cache_{os.path.basename(gt_csv_path)}")
    cache_pred_csv = os.path.join(os.path.dirname(pred_csv_path), f"cache_{os.path.basename(pred_csv_path)}")

    # Read and sort data
    gt = pd.read_csv(gt_csv_path).sort_values(by=[STUDY_ID_COL_NAME]).reset_index(drop=True)
    pred = pd.read_csv(pred_csv_path).sort_values(by=[STUDY_ID_COL_NAME]).reset_index(drop=True)

    # Get intersection of study IDs
    shared_study_ids = set(gt[STUDY_ID_COL_NAME]).intersection(pred[STUDY_ID_COL_NAME])
    print(f"Number of shared study IDs: {len(shared_study_ids)}")

    # Filter out study IDs not in the intersection
    gt = gt[gt[STUDY_ID_COL_NAME].isin(shared_study_ids)].reset_index(drop=True)
    pred = pred[pred[STUDY_ID_COL_NAME].isin(shared_study_ids)].reset_index(drop=True)

    # Cache filtered files
    gt.to_csv(cache_gt_csv, index=False)
    pred.to_csv(cache_pred_csv, index=False)

    # Validate data consistency
    assert len(gt) == len(pred), "Length of gt and pred is inconsistent"
    assert report_col_name in gt.columns and report_col_name in pred.columns, f"{report_col_name} column does not exist"
    assert gt[STUDY_ID_COL_NAME].equals(pred[STUDY_ID_COL_NAME]), "study_id in gt and pred is inconsistent"

    # Extract report columns
    return gt[report_col_name].tolist(), pred[report_col_name].tolist()

def green_main(gt_csv_path, pred_csv_path, report_col_name, model_name, output_dir):
    """Main function to extract reports and compute metrics."""
    refs, hyps = extract_reports_to_list(gt_csv_path, pred_csv_path, report_col_name)
    compute(model_name, refs, hyps, output_dir)

if __name__ == "__main__":
    # Set CSV file paths and column names
    gt_csv_path = "/net/projects/chacha/cxr_eval/test/gt_imp_sample.csv"
    pred_csv_path = "/net/projects/chacha/cxr_eval/test/gen_imp_sample_3_1.csv"
    report_col_name = REPORT_COL_NAME  # Adjust according to actual column name

    # Model name and output directory
    model_name = "StanfordAIMI/GREEN-radllama2-7b"
    output_dir = "/net/projects/chacha/cxr_eval/results"

    # Run the main function
    green_main(gt_csv_path, pred_csv_path, report_col_name, model_name, output_dir)
