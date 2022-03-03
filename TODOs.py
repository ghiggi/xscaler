#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 16:38:31 2022

@author: ghiggi
"""
# import xscaler
# xscaler.GlobalScaler.MinMaxScaler
# xscaler.GlobalScaler.StandardScaler

# GlobalScaler
# TemporalScaler
# xr.ALL_DIMS # ...

## Make "elapsed time" optional

## GitHub issues related to groupby(time)
# - https://github.com/pydata/xarray/issues/2237
##----------------------------------------------------------------------------.
## TODO
# - Robust standardization (IQR, MEDIAN) (https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.RobustScaler.html#sklearn.preprocessing.RobustScaler)
# - feature_min, feature_max as dictionary per variable for MinMaxScaler ...
# - Add lw and up to std scalers (avoid outliers alter the distribution)
# - In TemporalScalers, when new_data contain new time_groupby indices values, insert NaN values
#     in mean_, std_  for the missing time_groupby values
# - check_time_groups might also check that t_res specified is > to t_res data
##----------------------------------------------------------------------------.
# # Loop over each variable (for Datasets)
# gs = GlobalStandardScaler(data=ds)
# gs.fit()
# mean_ = gs.mean_
# ds['z500'] = ds['z500'] - mean_['z500']

# # Loop over each variable (for DataArray)
# gs = GlobalStandardScaler(data=da, variable_dim="feature")
# gs.fit()
# mean_ = gs.mean_
# da.loc[dict(feature='z500')] = da.loc[dict(feature='z500')] - mean_.loc[dict(feature='z500')]

# How to generalize to Dataset and DataArray:
# var = "z500"
# sel = "['" + var + "']"
# sel = ".loc[dict(" + variable_dim + "='" + var + "')]"
# exec_cmd = "x" + sel + " = x" + sel "- mean_" + sel
# exec(exec_cmd)

##----------------------------------------------------------------------------.
#### Possible future improvements
## RollingScaler
# - No rolling yet implemented for groupby xarray object
## SpatialScaler
# - Requires a groupby_spatially(gpd_poly or xr.grid)

## In future: multidimensional groupby? :
# - http://xarray.pydata.org/en/stable/groupby.html
# - http://xarray.pydata.org/en/stable/generated/xarray.IndexVariable.html#xarray.IndexVariable
# - https://github.com/pydata/xarray/issues/324
# - https://github.com/pydata/xarray/issues/1569

## sklearn-xarray
# https://phausamann.github.io/sklearn-xarray/content/pipeline.html
