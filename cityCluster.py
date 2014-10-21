'''
Adam Terwilliger
Version 1.0
October 17, 2014
Objective: Utilize large-scale climate data hosted by NASA to find
           a historical and predicted pair of cities that have similar climates
Resources: packages -- numpy, netCDF4, scikit-learn
           dataset -- NASA Earth Exchange (NEX) Downscaled Climate Projections (NEX-DCP30)
Collaborators: Dr. Ed Aboufadel
---------------------------------------------------------------------------------
We specifically worked with the greenhouse gas emissions scenario known as Representative Concentration Pathways (4.5 RCP)
for the ensemble statistics calculated from all model runs available. We ran our k-means clustering algorithm
for 36-dimensional clusters (12 months by 3 variables: monthly averaged maximum temperature, minimum temperature,
and precipitation). We choose 22 of the top 30 most populous cities as per the 2010 census to find pairwise
clusters for two years, a 2000 Retrospective Run compared to a 2050 Prospective Run.
'''

import datetime, subprocess, os
from array import array
import sys
import numpy
import netCDF4 as netCDF
from sklearn.cluster import KMeans

# find the datasets we want to work with
historical_pr = '/mnt/s3-nexdcp30/NEX-quartile/historical/mon/atmos/pr/r1i1p1/v1.0/CONUS/pr_ens-avg_amon_historical_CONUS_200001-200412.nc'
historical_tasmax = '/mnt/s3-nexdcp30/NEX-quartile/historical/mon/atmos/tasmax/r1i1p1/v1.0/CONUS/tasmax_ens-avg_amon_historical_CONUS_200001-200412.nc'
historical_tasmin = '/mnt/s3-nexdcp30/NEX-quartile/historical/mon/atmos/tasmin/r1i1p1/v1.0/CONUS/tasmin_ens-avg_amon_historical_CONUS_200001-200412.nc'

rcp45_pr = '/mnt/s3-nexdcp30/NEX-quartile/rcp45/mon/atmos/pr/r1i1p1/v1.0/CONUS/pr_ens-avg_amon_rcp45_CONUS_204601-205012.nc'
rcp45_tasmax = '/mnt/s3-nexdcp30/NEX-quartile/rcp45/mon/atmos/tasmax/r1i1p1/v1.0/CONUS/tasmax_ens-avg_amon_rcp45_CONUS_204601-205012.nc'
rcp45_tasmin = '/mnt/s3-nexdcp30/NEX-quartile/rcp45/mon/atmos/tasmin/r1i1p1/v1.0/CONUS/tasmin_ens-avg_amon_rcp45_CONUS_204601-205012.nc'

# convert the data into netCDF format
print 'Processing ' + historical_pr
py_hist_pr =  netCDF.Dataset(historical_pr, 'r')
print 'Processing ' + historical_tasmax
py_hist_tasmax = netCDF.Dataset(historical_tasmax, 'r')
print 'Processing ' + historical_tasmin
py_hist_tasmin = netCDF.Dataset(historical_tasmin, 'r')

print 'Processing ' + rcp45_pr
py_rcp45_pr = netCDF.Dataset(rcp45_pr, 'r')
print 'Processing ' + rcp45_tasmax
py_rcp45_tasmax = netCDF.Dataset(rcp45_tasmax, 'r')
print 'Processing ' + rcp45_tasmin
py_rcp45_tasmin = netCDF.Dataset(rcp45_tasmin, 'r')

print 'Getting 2000 - 2004 precipitation variables'
hist_pr_data = py_hist_pr.variables['pr'][1, :, :]
hist_pr_lat = py_hist_pr.variables['lat'][:]
hist_pr_lon = py_hist_pr.variables['lon'][:]
hist_pr_time = py_hist_pr.variables['time'][:]

print 'Getting 2000 - 2004 max temp variables'
hist_tasmax_data = py_hist_tasmax.variables['tasmax'][:]
hist_tasmax_lat = py_hist_tasmax.variables['lat'][:]
hist_tasmax_lon = py_hist_tasmax.variables['lon'][:]
hist_tasmax_time = py_hist_tasmax.variables['time'][:]

print 'Getting 2000 - 2004 min temp variables'
hist_tasmin_data = py_hist_tasmin.variables['tasmin'][:]
hist_tasmin_lat = py_hist_tasmin.variables['lat'][:]
hist_tasmin_lon = py_hist_tasmin.variables['lon'][:]
hist_tasmin_time = py_hist_tasmin.variables['time'][:]

print 'Getting 2046 - 2050 precipitation variables'
rcp45_pr_data = py_rcp45_pr.variables['pr'][:]
rcp45_pr_lat = py_rcp45_pr.variables['lat'][:]
rcp45_pr_lon = py_rcp45_pr.variables['lon'][:]
rcp45_pr_time = py_rcp45_pr.variables['time'][:]

print 'Getting 2046 - 2050 max temp variables'
rcp45_tasmax_data = py_rcp45_tasmax.variables['tasmax'][:]
rcp45_tasmax_lat = py_rcp45_tasmax.variables['lat'][:]
rcp45_tasmax_lon = py_rcp45_tasmax.variables['lon'][:]
rcp45_tasmax_time = py_rcp45_tasmax.variables['time'][:]

print 'Getting 2046 - 2050 min temp variables'
rcp45_tasmin_data = py_rcp45_tasmin.variables['tasmin'][:]
rcp45_tasmin_lat = py_rcp45_tasmin.variables['lat'][:]
rcp45_tasmin_lon = py_rcp45_tasmin.variables['lon'][:]
rcp45_tasmin_time = py_rcp45_tasmin.variables['time'][:]

print 'Compressing variables to readable format'
hist_pr_data = hist_pr_data.compressed()
hist_pr_data = hist_pr_data.astype('f8')

hist_tasmax_data = hist_tasmax_data.compressed()
hist_tasmax_data = hist_tasmax_data.astype('f8')

hist_tasmin_data = hist_tasmin_data.compressed()
hist_tasmin_data = hist_tasmin_data.astype('f8')

rcp45_pr_data = rcp45_pr_data.compressed()
rcp45_pr_data = rcp45_pr_data.astype('f8')

rcp45_tasmax_data= rcp45_tasmax_data.compressed()
rcp45_tasmax_data = rcp45_tasmax_data.astype('f8')

rcp45_tasmin_data = rcp45_tasmin_data.compressed()
rcp45_tasmin_data = rcp45_tasmin_data.astype('f8')

print '2000 - 2004 Precipitation'
print hist_pr_data, hist_pr_lat, hist_pr_lon, hist_pr_time
print '2000 - 2004 Max Temp'
print hist_tasmax_data, hist_tasmax_lat, hist_tasmax_lon, hist_tasmax_time
print '2000 - 2004 Min Temp'
print hist_tasmin_data, hist_tasmin_lat, hist_tasmin_lon, hist_tasmin_time
print '2046 - 2050 Precipitation'
print rcp45_pr_data, rcp45_pr_lat, rcp45_pr_lon, rcp45_pr_time
print '2046 - 2050 Max Temp'
print rcp45_tasmax_data, rcp45_tasmax_lat, rcp45_tasmax_lon, rcp45_tasmax_time
print '2046 - 2050 Min Temp'
print rcp45_tasmin_data, rcp45_tasmin_lat, rcp45_tasmin_lon, rcp45_tasmin_time

# next steps

# okay, we've got the six datasets, now what?

# we have to pick out only the years 2000 and 2050, 
# thus removing 2001, 2002, 2003, 2004, and
# 2046, 2047, 2048, and 2049

# pseudocode:
# 12 months * 5 years = 60 values
# hist_pr <- hist_pr[first twelve]
# hist_pr <- hist_pr[1:20]
# rcp45_pr <- rcp45_pr[last twelve]
# rcp45_pr <- rcp45_pr[49:60]

# okay, now we've got a dataset for only two years

# what do we do about the months?
# currently the data looks like:
# temp(year, month) lat lon
# 225(2000, 01)  41.5   238.1
# 229(2000, 02)  41.5   238.1
# 231(2000, 03)  41.5   238.1
# ...
# 222(2000, 12)  41.5   238.1
# 224(2000, 01)  38.4   223.5
# 225(2000, 02)  38.4   223.5
# 234(2000, 03)  38.4   223.5
# ...
# 220(2000, 12)  38.4   223.5

# what do we want it to look like?
#            Jan00  Feb00  Mar00 ...  Dec00
# Chicago    225    229    231   ...  222
# Detroit    222    224    225   ...  220 

# what is missing? 
# 1) transposition of months
# 2) labels for cities

# final step -- output data to csv files
# example output shown below
# import csv
# with open('test.csv', 'w', newline='') as fp:
#    a = csv.writer(fp, delimiter=',')
#    data = [['Me', 'You'],
#            ['293', '219'],
#            ['54', '13']]
#    a.writerows(data)
