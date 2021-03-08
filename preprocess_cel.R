# read and process cel files into a gene expression matrix

# Load libraries
library(data.table)
library(oligo)
library(limma)
library(affycoretools)

# Install libraries specific to the array 
library(pd.clariom.s.human)
library(clariomshumantranscriptcluster.db)

# file and directory names
annofile <- '~/ASSESS/Data/anno.csv'
celdir <- '~/ASSESS/Data/CEL_file'
arrayout <- '~/ASSESS/Data/array.csv'

# Import annotation file
#anno <- fread(annofile)[SYMBOL != '']

# Read the cel file names
samples <- dir(celdir)

# Check that all the cel files are output from the same platform
data.frame(samples, unlist(lapply(samples, function(x) affyio::read.celfile.header(x)[["cdfName"]])))

# Read cel files
setwd(celdir)
raw <- read.celfiles(samples)

# Take robust multichip average
eset <- rma(raw)

# log2 transform and normalize data 
eset_frame <- data.frame(exprs(eset))

# Get the gene symbol annotation and merge with the expression data
Annot <- data.frame(SYMBOL=sapply(contents(clariomshumantranscriptclusterSYMBOL), paste, collapse=", "))
gene_array <- merge(Annot, eset_frame, by.x=0, by.y=0, all=T)

# removes any rows where there is no gene symbol
gene_array <- gene_array[!(is.na(gene_array$SYMBOL) | gene_array$SYMBOL=="NA"), ]

# remove Row.names column
gene_array = subset(gene_array, select = -c(Row.names))

# collapse to gene level (avereps creates a matrix)
gene_array <- avereps(gene_array, ID = gene_array$SYMBOL)
gene_array <- as.data.table(gene_array)

# Write out to file
write.csv(gene_array, file = arrayout, row.names = FALSE)
