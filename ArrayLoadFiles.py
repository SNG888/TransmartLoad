#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prepare the TranSMART load files for gene expression or RNASeq data 
1.  Generate the platform file
2.  Generate the mrna_annotation.params file
3.  Generate the array file
4.  Generate the sample mapping file
5.  Generate the expression.params file

The input array file is expected in the following format:
a. Row headings are in the first column and are gene symbols.  The gene symbols
should be summarized i.e no duplicate gene symbols
b. SUBJECT_IDs are the column headings from column 2 onwards
c. Values should be normalised read counts
d. For one tissue type only
"""

# load libraries
import pandas as pd
import os

# Set the path and create paths for writing transmart data load files 
path = "/Users/sandra/CLUSTER"
os.chdir(path)

parent_dir = "./RNA_MTX"
array_dir = parent_dir + "/Array"
platform_dir = parent_dir + "/Platform"

if not os.path.exists(parent_dir):
    os.mkdir(parent_dir)

if not os.path.exists(array_dir):
    os.mkdir(array_dir)

if not os.path.exists(platform_dir):
    os.mkdir(platform_dir)

# input file names
in_array_file = "/Users/sandra/CLUSTER/data/rnaMTX.csv"    

# output file names
platform_file = "platform.txt"
anno_file = "mrna_annotation.params" # do not change this name
array_file = "RNA.txt"
mapping_file = "Subject_Sample_Mapping.txt"
array_param_file = "expression.params" # do not change this name

# global variables
platform_name = "CLUSTER_RNA_MTX"
bio_type = "rna"  # change this to 'gene' if input is gene expression
tissue_type = "PBMC" # change this to relevant tissue type abbreviation
platform_title = "CLUSTER RNASeq MTX"
study_name = "MTX" # name of node in TranSMART
node_address = "BiomarkerData+RNASeq+TISSUETYPE"

# read the array input file
arrayDF = pd.read_csv(in_array_file)

# function to  generate column headers for array, get subject ID
# in this example the tissue type is PBMC - replace where appropriate
# and the data is RNA - replace with 'gene' if gene expression microarray
def SampleID(a):
    return bio_type + "_" + a + "_" + tissue_type

# generate the SAMPLE_ID from the column headings of the array
MapList = list(arrayDF.columns.values)
MapList = MapList[1:]
MAPDF = pd.DataFrame(MapList, columns=["SUBJECT_ID"])
MAPDF[["SAMPLE_ID"]] = MAPDF.apply(
    lambda row: pd.Series(SampleID(row["SUBJECT_ID"])),axis=1)


# Step 1 - generate platform file
# The platform file is the TranSMART annotation file.  
# As we are loading data at GENE_SYMBOL level rather than PROBE_ID, the platform
# file generated here has the PROBE_ID equivalent to the GENE_SYMBOL
platDF = arrayDF[["GENE_SYMBOL"]]
platDF["PROBE_ID"] = platDF[["GENE_SYMBOL"]]
platDF["GPL_ID"] = platform_name
platDF["GENE_ID"] = None
platDF["ORGANISM"] = "Homo Sapiens"
platDF = platDF[["GPL_ID","PROBE_ID","GENE_SYMBOL","GENE_ID","ORGANISM"]]
platDF.to_csv(os.path.join(platform_dir,platform_file), sep="\t", index=False)

# Step 2 - generate the mrna_annotation.params file required for loading a 
# platform file to TranSMART
anno_params = open(os.path.join(platform_dir,anno_file), 'w')
anno_lines = ["PLATFORM=" + platform_name + " \n", 
              "TITLE='" + platform_title + "' \n",
              "ANNOTATIONS_FILE=" + platform_file + " \n", 
              "ORGANISM='Homo Sapiens'"]
anno_params.writelines(anno_lines)
anno_params.close()

# Step 3 - generate the array file
# The columns of the array file to load to TranSMART has the SAMPLE_IDs as the
# column headings from column 2 to the end
# Column 1 are the GENE_SYMBOLS
arrayDF.set_index("GENE_SYMBOL", inplace=True)
array_T = arrayDF.T

array_T.reset_index(inplace=True)
array_T.rename(columns={'index':'SUBJECT_ID'}, inplace=True)
array_T = pd.merge(array_T, MAPDF, on ="SUBJECT_ID")
array_T.drop(["SUBJECT_ID"], inplace=True, axis=1)
array_T.set_index("SAMPLE_ID", inplace=True)
loadDF = array_T.T
loadDF.index.names = ["REF_ID"]
loadDF.to_csv(os.path.join(array_dir,array_file) ,index=True, sep='\t')

# Step 4 - create the sample mapping file
# This file indicates how to map SAMPLE_ID to SUBJECT_ID
MAPDF["STUDY_ID"] = study_name
MAPDF["SITE_ID"] = None
MAPDF["PLATFORM"] = platform_name
MAPDF["ATTR1"] = None
MAPDF["TISSUETYPE"] = tissue_type
MAPDF["ATTR2"] = None
MAPDF["SOURCE_CD"] = None
MAPDF["CATEGORY_CD"] = node_address

cols = ['STUDY_ID','SITE_ID','SUBJECT_ID','SAMPLE_ID','PLATFORM','ATTR1',
        'TISSUETYPE','ATTR2','CATEGORY_CD','SOURCE_CD']

MAPDF = MAPDF[cols]
MAPDF.to_csv(os.path.join(array_dir,mapping_file), index=False, sep='\t')

# Step 5 - generate the expression.params file required when loading a
# microarray file to TranSMART
exp_params = open(os.path.join(array_dir,array_param_file),'w')
exp_lines = ["DATA_FILE_PREFIX=" + array_file + " \n", 
             "DATA_TYPE=L \n",
             "MAP_FILENAME=" + mapping_file + " \n", 
             "SRC_LOG_BASE=2 \n",
             "ALLOW_MISSING_ANNOTATIONS=Y"]
exp_params.writelines(exp_lines)
exp_params.close()
