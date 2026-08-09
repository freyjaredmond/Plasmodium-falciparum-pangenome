import pandas as pd
## mapx data
gold = pd.read_csv("MAP-X/gold_standard.csv")
pred = pd.read_csv("MAP-X/all_predictions.csv")
# put columns in the same order
gold['p1'] = gold[['protein1', 'protein2']].min(axis=1)
gold['p2'] = gold[['protein1', 'protein2']].max(axis=1)

pred['p1'] = pred[['protein1', 'protein2']].min(axis=1)
pred['p2'] = pred[['protein1', 'protein2']].max(axis=1)

#dedup the gold data
gold = gold.drop_duplicates(subset=['p1', 'p2'])
#merge
merged = gold.merge(pred, on=['p1', 'p2'], how="inner")

from sklearn.metrics import roc_curve, auc, precision_recall_curve
import numpy as np
## have to seperate by time point as the paper shows declining specificity across time points
results = {}
for hpi in sorted(merged['condition'].dropna().unique()):
    subset = merged[merged['condition'] == hpi]
    # a high auc gives confidence that MAP-X is correctly identifying interactiors
    fpr, tpr, _ = roc_curve(subset['complex'], subset['calpred'])
    roc_auc = auc(fpr, tpr)
    # precision- how many that passed the threshold were correct
    # recall- how many did I correctlu catch 
    precision, recall, pr_thresholds = precision_recall_curve(subset['complex'], subset['calpred'])
    pr_auc = auc(recall, precision)
    # try at 0.9
    # try at 0.8
    #try at 0.7
    idx = np.argmax(precision >= 0.9) #get the first point where precision clears 0
    thresh_at_90 = pr_thresholds[idx] if idx < len(pr_thresholds) else None
    recall_at_90 = recall[idx]
    idx2 = np.argmax(precision >= 0.8)
    thresh_at_80 = pr_thresholds[idx2] if idx2 < len(pr_thresholds) else None
    recall_at_80 = recall[idx2]
    idx3 = np.argmax(precision >= 0.85)
    thresh_at_85 = pr_thresholds[idx3] if idx3 < len(pr_thresholds) else None
    recall_at_85 = recall[idx3]
    results[hpi] = {
        'n_pos': (subset['complex']==1).sum(),
        'n_neg': (subset['complex']==0).sum(),
        'roc_auc': roc_auc,
        'pr_auc': pr_auc,
        'threshold_p90': thresh_at_90,
        'recall_at_p90': recall_at_90,
        "threshold_p80":thresh_at_80,
        "recall_at_p80": recall_at_80,
        "threshold_p85":thresh_at_85,
        "recall_at_p85":recall_at_85
    }

results_df = pd.DataFrame(results).T
print(results_df)
results_df.to_csv("precision_recall_roc.tsv", sep="\t")