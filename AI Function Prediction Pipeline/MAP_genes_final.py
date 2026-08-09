import pandas as pd
data=pd.read_csv("MAP-X/all_predictions.csv", sep=",")

data_4=data[data["condition"]==4]
data_4=data_4[data_4["calpred"]>0.927383284316159]

data_10=data[data["condition"]==10]
data_10=data_10[data_10["calpred"]>0.828981455398792]

data_16=data[data["condition"]==16]
data_16=data_16[data_16["calpred"]>0.69079780083879]

data_22=data[data["condition"]==22]
data_22=data_22[data_22["calpred"]>0.525281991775949]

data_28=data[data["condition"]==28]
data_28=data_28[data_28["calpred"]>0.56595792791522]

data_34=data[data["condition"]==34]
data_34=data_34[data_34["calpred"]>0.552624822435894]

data_40=data[data["condition"]==40]
data_40=data_40[data_40["calpred"]>0.619907380031648]

data_all = pd.concat([data_4, data_10, data_16, data_22, data_28, data_34, data_40], ignore_index=True)

## put into the correct order
data_all['p1'] = data_all[['protein1', 'protein2']].min(axis=1)
data_all['p2'] = data_all[['protein1', 'protein2']].max(axis=1)

data_all.to_csv("mapx_pass_threshold.tsv", sep="\t")
#drop dup interactions (will be multiple across time points)

data_unique = data_all.drop_duplicates(subset=['p1', 'p2'])
print(f"Number of unique interactions: {len(data_unique)}")
data_unique.to_csv("mapx_pass_thresh_unique_interactions.tsv", sep="\t")
data_unique_proteins =set(data_unique["p1"]) | set(data_unique["p2"])
print(f"Number of unique proteins: {len(data_unique_proteins)}")
                                                  