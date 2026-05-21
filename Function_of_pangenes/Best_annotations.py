### A script to get the best GO annotations for the pangenes##
## This prefers curated annotations where possible ##
## Input: GO terms from PlasmoDB for the pangenes ##
## Output: tsv file with the best GO annotations for the gene
## A bar chart showing the percentage of core and cloud that have GO annotations ##

import pandas as pd
import matplotlib.pyplot as plt
data=pd.read_csv("Functional_analysis/Clusterprofiler/GO.txt", sep="\t")
print(data.head)

#select the curated annotation if present- if not take the computed
best_annotations=[]
no_annotations_component=[]
no_annotations_function=[]
no_annotations_process=[]
for idx, row in data.iterrows():
    gene_id = row["Gene ID"]

#components
    if pd.notna(row["Curated GO Component IDs"]) and row["Curated GO Component IDs"] != "N/A":
        component_id = str(row["Curated GO Component IDs"]).split(";")
        component_term = str(row["Curated GO Components"]).split(";")
        component_source = "curated"
    elif pd.notna(row["Computed GO Component IDs"]) and row["Computed GO Component IDs"] != "N/A":
        component_id = str(row["Computed GO Component IDs"]).split(";")
        component_term = str(row["Computed GO Components"]).split(";")
        component_source = "computed"
    else:
        component_id = []
        component_term = []
        component_source = None
        no_annotations_component.append(gene_id)
#Functions
    if pd.notna(row["Curated GO Function IDs"]) and row["Curated GO Function IDs"] != "N/A":
        function_id = str(row["Curated GO Function IDs"]).split(";")
        function_term = str(row["Curated GO Functions"]).split(";")
        function_source = "curated"
    elif pd.notna(row["Computed GO Function IDs"]) and row["Computed GO Function IDs"] != "N/A":
        function_id = str(row["Computed GO Function IDs"]).split(";")
        function_term = str(row["Computed GO Functions"]).split(";")
        function_source = "computed"
    else:
        function_id = [] #create empty list
        function_term = []
        function_source = None
        no_annotations_function.append(gene_id)
#Processes
    if pd.notna(row["Curated GO Process IDs"]) and row["Curated GO Process IDs"] != "N/A":
        process_id = str(row["Curated GO Process IDs"]).split(";")
        process_term = str(row["Curated GO Processes"]).split(";")
        process_source = "curated"
    elif pd.notna(row["Computed GO Process IDs"]) and row["Computed GO Process IDs"] != "N/A":
        process_id = str(row["Computed GO Process IDs"]).split(";")
        process_term = str(row["Computed GO Processes"]).split(";")
        process_source = "computed"
    else:
        process_id = []
        process_term = []
        process_source = None
        no_annotations_process.append(gene_id)

    if component_id:
        component_dict=dict(zip(component_id,component_term))
        for id, term in component_dict.items():
            best_annotations.append({"Gene_ID":gene_id,
                                 "GO_ID":id.strip(),
                                 "GO_term":term.strip(),
                                 "Type":"CC",
                                 "GO_source":component_source})
    if function_id:
        function_dict=dict(zip(function_id, function_term))
        for id, term in function_dict.items():
            best_annotations.append({"Gene_ID":gene_id,
                                 "GO_ID":id.strip(),
                                 "GO_term":term.strip(),
                                 "Type":"MF",
                                 "GO_source":function_source})
    if process_id:
        process_dict=dict(zip(process_id,process_term))
        for id, term in process_dict.items():
            best_annotations.append({"Gene_ID":gene_id,
                                 "GO_ID":id.strip(),
                                 "GO_term":term.strip(),
                                 "Type":"BP",
                                 "GO_source":process_source})
final=pd.DataFrame(best_annotations)
final.to_csv("GET_PANGENES_pseudo/Best_annotations_16", sep="\t")


#percentage of occupancy with any GO terms
print(f"No component_total:{len(no_annotations_component)}\n")
print(f"No component_total:{len(no_annotations_function)}\n")
print(f"No component_total:{len(no_annotations_process)}\n")

core_list=pd.read_csv("GET_PANGENES_pseudo/Core_genes_3D7_cluster_sixteen.txt", sep="\t", header=None)
cloud_list=pd.read_csv("GET_PANGENES_pseudo/Cloud_genes_3D7_cluster_sixteen.txt", sep="\t", header=None)

has_annotation_core=[]
no_annotation_core=[]
has_annotation_cloud=[]
no_annotation_cloud=[]
best_annotations_list=[]

for idx, row in final.iterrows():
    gene_id=row["Gene_ID"]
    best_annotations_list.append(gene_id)

for genes in core_list[0]:
    if genes in best_annotations_list:
        has_annotation_core.append(genes)
    else:
        no_annotation_core.append(genes)

for genes in cloud_list[0]:
    if genes in best_annotations_list:
        has_annotation_cloud.append(genes)
    else:
        no_annotation_cloud.append(genes)

percentage_core=len(has_annotation_core)/len(core_list)*100
percentage_cloud=len(has_annotation_cloud)/len(cloud_list)*100
    
print(f"Percentage of core:{percentage_core}\n")
print(f"Percentage of cloud:{percentage_cloud}\n")
groups = ["Core", "Cloud"]
percentages = [percentage_core, percentage_cloud]
colours=["red", "blue"]

#PLOT

fig,ax=plt.subplots(figsize=(6,12))
ax.bar(groups, percentages,color=colours )
ax.set_xlabel("Groups")
ax.set_ylabel("Percentage with GO Term (%)")
plt.show()
