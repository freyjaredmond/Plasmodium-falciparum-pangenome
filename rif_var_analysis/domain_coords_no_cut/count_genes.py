import pandas as pd
import glob
import os
files=glob.glob("GET_PANGENES_pseudo/Var_analysis/domain_coords_no_cut/*Keys")
genome_data=[]
for file in files:
    genome=os.path.basename(file).split(".")[0]
    counter=0
    with open(file,"r") as f:
        for lines in f:
            if lines.startswith(">"):
                counter+=1
                
    genome_data.append({"Genome":genome,
                        "Count":counter})

df=pd.DataFrame(genome_data)
print(df)   

    