ChallengeEntry
==============

This should be considered the submission to the NASA Challenge: Build an App to                                                                                        Utilize OpenNEX Climate and Earth Science Data.

To test this application, please run the R script called pamAndDaisies.R.

Our python script called cityCluster.py is used to obtain the data files, manipu                                                                                       late the data, and output a csv file that our R script read in.

Due to the amount of time our python script takes to read in and manipulate the                                                                                        data, a csv file is already provided for us.

---- Only the R script needs to be run for testing purposes ----

This R script then does clustering using the functions pam and daisy, hence the                                                                                        name of our application.

The daisy function is short for dissimilarity matrix and this is helpful in dete                                                                                       rmining which cities are similiar to one another.

The pam function then uses the dissimilarity matrix to do a Partitioning Around                                                                                        Medoids, which we can extract clusters from in R.

To run the R Script, make sure you are in the directory "/usr/local/src".

From there you have two choices:

1) run R and then source
2) run the script from command line

1a) type R while located in the correct directory
1b) type source('pamAndDaisies.R')
1c) type q() to leave the R window
1d) to view the clusters, open a text editor to view 'padOut.txt'
   ex. vim padOut.txt

2a) type R CMD BATCH pamAndDaisies.R
2b) view what ran in R in the pamAndDaisies.ROut
2c) repeat step 1d, by opening a text editor to view clusters

