### Model Preparation

Our codebase integrates CheXbert [3] for report labeling and RadGraph [4] for evaluation. Download the required model checkpoints from the [repository here](https://github.com/rajpurkarlab/CXR-Report-Metric) and place them in the `./models/` directory.

### Environment Preparation

To set up the project environment, use the following command:

```
conda env create --name=<env_name> -f cxr-green.yml
```

If you're already on DSI cluster, use the following command to activate environment:

```
conda activate /net/projects/chai-lab/miniconda3/envs/cxr-green
```

### Test Example

Here is an example how to run evaluation:

```
python test.py \
--gt_csv /net/projects/chacha/cxr_eval/test/gt_imp_sample.csv \
--gen_csv /net/projects/chacha/cxr_eval/test/gen_imp_sample_3_1.csv \
--output_metrics /net/projects/chacha/cxr_eval/results/metrics.csv \
--output_combined /net/projects/chacha/cxr_eval/results/metrics_w_green.csv \
--output_dir /net/projects/chacha/cxr_eval/results
```

### Running Notes

1. Based on our testing, we can successfully run metrics without (GREEN, BertScore, RadGraph F1) on A40 GPU. We'll continue updating requirement for environment and gpu to run (GREEN, BertScore, RadGraph F1).
2. Each input csv should contain columns **['study_id', 'report']**. Each column needs to be str and 'study_id' should not include any other characters except numbers.
3. Ensure each input csv has no empty values.

