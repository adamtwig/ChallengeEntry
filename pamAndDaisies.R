# Developer: Anonymized for Competition
# Version 2 -- October 21, 2014
# K-means clustering on climate change projections
# Data: NEX-DCP30 - Downscaled Climate Projections dataset 
#       comprised of climate scenarios for the coterminous 
#       United States for four greenhouse gas emission scenarios.
# Obtained: http://www.usgs.gov/climate_landuse/clu_rd/apps/nccv_viewer.asp
# Entry part of Innocentive NASA Challenge: 
#     Build an App to Utilize OpenNEX Climate and Earth Science Data
# Acknowledgements -- Anonymized for Competition

rawProjections <- read.csv('/usr/local/src/ProjectionData.csv')

columnHeadingsVars <- rep(c('MinTemp85','MaxTemp85','Precip85'), each=12)

columnHeadingsMonths <- rep(c('Jan', 'Feb','Mar','Apr','May','Jun',
                                    'Jul','Aug','Sep','Oct','Nov','Dec'), times=3)

topTenColumnHeadings <- paste(columnHeadingsVars, columnHeadingsMonths, sep="_")

colnames(rawProjections) <- c('County', topTenColumnHeadings)

projectionData <- rawProjections[,2:37]

row.names(projectionData) <- rawProjections[,1]

install.packages('cluster')
library(cluster)

# find dissimilarity matrix
daisyOut <- as.matrix(daisy(projectionData))

# cities shouldn't pair with themselves in different years
diag(daisyOut[1:22,23:44]) <- rep(999999, times=22)
diag(daisyOut[23:44,1:22]) <- rep(999999, times=22)

# cities shoudn't pair with cities from the same years
daisyOut[1:22,1:22] <- matrix(999999, 22, 22)
daisyOut[23:44, 23:44] <- matrix(999999, 22, 22)

# run clustering for 22 clusters (44 cities / 2 pairs each = 22 clusters)
# use the dissimilarity matrix for clustering
pamOut <- pam(daisyOut, 22, diss=TRUE)

# view the clusters
sort(pamOut$clustering)

# input own directory and run if desired to export output to text file
# write.table(sort(pamOut$clustering), ... (chosen directory) ex. "/usr/local/src.padOut.txt", sep="\t"
