# Summarises an array by gene symbol

# load libraries
library(data.table)
library(limma)
library(dplyr)

# input file names
arrayFile <- '~/CLUSTER/data/old_RNAseq_TranSMART_11-12-20/Analysis/UCL_JIA_CPM_13Jan2020.csv'
annoFile <- '~/CLUSTER/data/EnsemblRef2.csv' #file has two columns PROBE_ID and GENE_SYMBOL

# outuput file name
arrayOut <- '~/CLUSTER/data/rnaMTX.csv'

# read array file - file details:
# normalised count
# SUBJECT_ID are column headings from column 2 onwards
# Column 1 is equivalent to PROBE_ID (eg Ensembl ID, probe ID)
rawArray <- fread(file = arrayFile, header = TRUE)
names(rawArray)[1] <- 'PROBE_ID'

# read ensembl annotation file 
# need EnsemblID/ProbeID and Gene Symbol
anno <- fread(annoFile)

# join rawArray with anno to get the gene symbol
newArray <- merge(x=rawArray, y=anno, by='PROBE_ID',all.x=TRUE)

# removes any rows where there is no gene symbol and set GENE_SYMBOL as first column
newArray <- newArray[!(is.na(newArray$GENE_SYMBOL) | newArray$GENE_SYMBOL==""), ]
newArray <- newArray %>% select(GENE_SYMBOL, everything())

# remove PROBE_ID
newArray = subset(newArray, select = -c(PROBE_ID))

# collapse to gene level (avereps creates a matrix)
newArray <- avereps(newArray, ID = newArray$GENE_SYMBOL)
newArray <- as.data.table(newArray)

# Write out newArray to file
write.csv(newArray, file=arrayOut, row.names = FALSE)

