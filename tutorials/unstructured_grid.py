#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 11:00:51 2022

@author: ghiggi
"""

import os
import xarray as xr
import numpy as np

from xscaler import (
    LoadScaler,
    GlobalStandardScaler,
    GlobalMinMaxScaler,
    TemporalStandardScaler,
    TemporalMinMaxScaler,
    SequentialScaler,
)

##----------------------------------------------------------------------------.
data_dir = "/home/ghiggi/Projects/DeepSphere/data/0_ToyData/Healpix_400km/"


ds_dynamic = ds_dynamic.drop(["level"])
ds_bc = ds_bc.drop(["lat", "lon"])

da_static = xr.open_zarr(os.path.join(data_dir, "DataArray", "static.zarr"))["Data"]
ds_static = da_static.to_dataset("feature").compute()

# Choose scaler to test
TemporalScaler = TemporalStandardScaler
TemporalScaler = TemporalMinMaxScaler

GlobalScaler = GlobalStandardScaler
GlobalScaler = GlobalMinMaxScaler

##----------------------------------------------------------------------------.
# xr.testing.assert_identical
# xr.testing.assert_equal

##----------------------------------------------------------------------------.
# ######################
#### GlobalScalers #####
# ######################
ds = ds_dynamic.compute()
da = ds.to_array(dim="feature", name="whatever").transpose("time", "node", "feature")

# Dataset
gs = GlobalScaler(data=ds)
gs.fit()
ds_trans = gs.transform(ds).compute()
ds_invert = gs.inverse_transform(ds_trans).compute()
xr.testing.assert_equal(ds, ds_invert)

# DataArray with variable dimension
gs = GlobalScaler(data=da, variable_dim="feature")
gs.fit()
da_trans = gs.transform(da, variable_dim="feature").compute()
da_invert = gs.inverse_transform(da_trans, variable_dim="feature").compute()
xr.testing.assert_equal(da, da_invert)

# DataArray without variable dimension
da1 = ds["z500"]
gs = GlobalScaler(data=da1, variable_dim=None)
gs.fit()
da_trans = gs.transform(da1, variable_dim=None).compute()
da_invert = gs.inverse_transform(da_trans, variable_dim=None).compute()
xr.testing.assert_equal(da1, da_invert)

# DataArray with groupby option (i.e. scaling each member ...)
gs = GlobalScaler(data=da, variable_dim="feature", groupby_dims="node")
gs.fit()
da_trans = gs.transform(da, variable_dim="feature").compute()
da_invert = gs.inverse_transform(da_trans, variable_dim="feature").compute()
xr.testing.assert_equal(da, da_invert)

# DataArray with variable_dimension but not specified
gs = GlobalScaler(data=da, variable_dim=None)
gs.fit()
da_trans = gs.transform(da, variable_dim=None).compute()
da_invert = gs.inverse_transform(da_trans, variable_dim=None).compute()
# xr.testing.assert_equal(da, da_invert)     # Not equal
xr.testing.assert_allclose(da, da_invert)  # Actually close ...

##----------------------------------------------------------------------------.
### - Fit with DataSet - Transform with DataArray
gs = GlobalScaler(data=ds)
gs.fit()
da_trans = gs.transform(da, variable_dim="feature").compute()
da_invert = gs.inverse_transform(da_trans, variable_dim="feature").compute()
xr.testing.assert_equal(da, da_invert)

### - Fit with DataArray - Transform with Dataset
gs = GlobalScaler(data=da, variable_dim="feature")
gs.fit()
ds_trans = gs.transform(ds).compute()
ds_invert = gs.inverse_transform(ds_trans).compute()
xr.testing.assert_equal(ds, ds_invert)

##----------------------------------------------------------------------------.
### - Write and load from disk
fpath = "/home/ghiggi/scaler_test.nc"
gs = GlobalScaler(data=ds)
gs.fit()
gs.save(fpath)

gs = LoadScaler(fpath)

# Dataset
ds_trans = gs.transform(ds).compute()
ds_invert = gs.inverse_transform(ds_trans).compute()
xr.testing.assert_equal(ds, ds_invert)

# DataArray (with variable dimension)
da_trans = gs.transform(da, variable_dim="feature").compute()
da_invert = gs.inverse_transform(da_trans, variable_dim="feature").compute()
xr.testing.assert_equal(da, da_invert)

# DataArray (without variable dimension)
da_trans = gs.transform(ds["z500"], variable_dim=None).compute()
da_invert = gs.inverse_transform(da_trans, variable_dim=None).compute()
xr.testing.assert_equal(ds["z500"], da_invert)

##-----------------------------------------------------------------------------.
# ########################
#### Temporal Scalers ####
# ########################
# Pixelwise --> groupby_dims = "node"
# Anomalies: center=True, standardize=False
# Standardized Anomalies: center=True, standardize=True
ds = ds_dynamic.compute()
da = ds.to_array(dim="feature", name="whatever").transpose("time", "node", "feature")

variable_dim = "feature"
time_dim = "time"
groupby_dims = "node"
time_groups = ["month", "day"]
time_groups = ["dayofyear"]
time_groups = ["hour", "weekofyear"]
time_groups = "season"

time_groups = {"hour": 6, "month": 2}

gs = TemporalScaler(data=ds, time_dim=time_dim, time_groups=None)
gs.fit()
ds_trans = gs.transform(ds).compute()
ds_invert = gs.inverse_transform(ds_trans).compute()
xr.testing.assert_equal(ds, ds_invert)

# Dataset
gs = TemporalScaler(data=ds, time_dim=time_dim, time_groups=time_groups)
gs.fit()
ds_trans = gs.transform(ds).compute()
ds_invert = gs.inverse_transform(ds_trans).compute()
xr.testing.assert_equal(ds, ds_invert)

# DataArray with variable dimension
gs = TemporalScaler(
    data=da, variable_dim=variable_dim, time_dim=time_dim, time_groups=time_groups
)
gs.fit()
da_trans = gs.transform(da, variable_dim=variable_dim).compute()
da_invert = gs.inverse_transform(da_trans, variable_dim=variable_dim).compute()
xr.testing.assert_equal(da, da_invert)

# DataArray without variable dimension
da1 = ds["z500"]
gs = TemporalScaler(
    data=da1, variable_dim=None, time_dim=time_dim, time_groups=time_groups
)
gs.fit()
da_trans = gs.transform(da1, variable_dim=None).compute()
da_invert = gs.inverse_transform(da_trans, variable_dim=None).compute()
xr.testing.assert_equal(da1, da_invert)

ds_trans = gs.transform(ds, variable_dim=None).compute()
ds_invert = gs.inverse_transform(ds_trans, variable_dim=None).compute()
xr.testing.assert_equal(ds, ds_invert)

# DataArray with groupby option (i.e. scaling each member ...)
gs = TemporalScaler(
    data=da,
    variable_dim=variable_dim,
    groupby_dims=groupby_dims,
    time_dim=time_dim,
    time_groups=time_groups,
)
gs.fit()
da_trans = gs.transform(da, variable_dim=variable_dim).compute()
da_invert = gs.inverse_transform(da_trans, variable_dim=variable_dim).compute()
xr.testing.assert_equal(da, da_invert)

# DataArray with variable_dimension but not specified
gs = TemporalScaler(
    data=da, variable_dim=None, time_dim=time_dim, time_groups=time_groups
)
gs.fit()
da_trans = gs.transform(da, variable_dim=None).compute()
da_invert = gs.inverse_transform(da_trans, variable_dim=None).compute()
# xr.testing.assert_equal(da, da_invert)     # Not equal
xr.testing.assert_allclose(da, da_invert)  # Actually close ...

##----------------------------------------------------------------------------.
## Fit with DataSet - Transform with DataArray
gs = TemporalScaler(data=ds, time_dim=time_dim, time_groups=time_groups)
gs.fit()
da_trans = gs.transform(da, variable_dim=variable_dim).compute()
da_invert = gs.inverse_transform(da_trans, variable_dim=variable_dim).compute()
xr.testing.assert_equal(da, da_invert)

## Fit with DataArray - Transform with Dataset
gs = TemporalScaler(
    data=da, variable_dim=variable_dim, time_dim=time_dim, time_groups=time_groups
)
gs.fit()
ds_trans = gs.transform(ds).compute()
ds_invert = gs.inverse_transform(ds_trans).compute()
xr.testing.assert_equal(ds, ds_invert)

##----------------------------------------------------------------------------.
# Check consistency
gs = TemporalScaler(data=ds, time_dim=time_dim, time_groups=["day", "month"])
gs.fit()
ds_trans = gs.transform(ds).compute()

gs = TemporalScaler(data=ds, time_dim=time_dim, time_groups="dayofyear")
gs.fit()

ds_trans1 = gs.transform(ds).compute()

xr.testing.assert_equal(ds_trans, ds_trans1)

##----------------------------------------------------------------------------.
### - Write and load from disk
fpath = "/home/ghiggi/scaler_test.nc"
gs = TemporalScaler(data=ds, time_dim=time_dim, time_groups=["day", "month"])
gs.fit()
gs.save(fpath)

gs = LoadScaler(fpath)
ds_trans = gs.transform(ds).compute()
ds_invert = gs.inverse_transform(ds_trans).compute()
xr.testing.assert_equal(ds, ds_invert)

##----------------------------------------------------------------------------.
### Check rename_dict
rename_dict = {"time": "forecast_time", "node": "space"}
new_ds = ds
new_ds = new_ds.rename(rename_dict)

# - GlobalScaler
groupby_dims = ["node", "time"]
groupby_dims = ["node"]
groupby_dims = None

gs = GlobalScaler(data=ds, groupby_dims=groupby_dims)
gs.fit()

ds_trans1 = gs.transform(new_ds).compute()
ds_trans = gs.transform(new_ds, rename_dict=rename_dict).compute()

ds_invert1 = gs.inverse_transform(ds_trans).compute()
ds_invert = gs.inverse_transform(ds_trans, rename_dict=rename_dict).compute()
xr.testing.assert_equal(new_ds, ds_invert)

# - Temporal scaler
time_dim = "time"
groupby_dims = "node"
groupby_dims = None
time_groups = ["month", "day"]
time_groups = {"hour": 6, "month": 2}
time_groups = None

gs = TemporalScaler(
    data=ds, time_dim=time_dim, time_groups=time_groups, groupby_dims=groupby_dims
)
gs.fit()

gs.mean_

ds_trans1 = gs.transform(new_ds).compute()
ds_trans = gs.transform(new_ds, rename_dict=rename_dict).compute()

ds_invert1 = gs.inverse_transform(ds_trans).compute()
ds_invert = gs.inverse_transform(ds_trans, rename_dict=rename_dict).compute()
xr.testing.assert_equal(new_ds, ds_invert)

##-----------------------------------------------------------------------------.
# ########################
#### SequentialScaler ####
# ########################
from modules.xscaler import SequentialScaler

# Pixelwise over all time
scaler1 = GlobalScaler(data=ds["z500"], groupby_dims="node")
# Pixelwise per month
scaler2 = TemporalScaler(
    data=ds["t850"], time_dim="time", time_groups="month", groupby_dims="node"
)

final_scaler = SequentialScaler(scaler1, scaler2)

final_scaler.fit()
print(final_scaler.list_scalers)

ds_trans = final_scaler.transform(ds).compute()
ds_invert = final_scaler.inverse_transform(ds_trans).compute()
xr.testing.assert_equal(ds, ds_invert)

##----------------------------------------------------------------------------.
# Global (over space)
scaler1 = GlobalScaler(data=ds, groupby_dims="node")
# Global (over time)
scaler2 = GlobalScaler(data=ds, groupby_dims="time")

final_scaler = SequentialScaler(scaler1, scaler2)
final_scaler.fit()
print(final_scaler.list_scalers)

ds_trans = final_scaler.transform(ds).compute()
ds_invert = final_scaler.inverse_transform(ds_trans).compute()
xr.testing.assert_allclose(ds, ds_invert)

##----------------------------------------------------------------------------.
# Pixelwise over all time
scaler1 = GlobalScaler(data=ds["z500"], groupby_dims="node")
# Pixelwise per month
scaler2 = TemporalScaler(
    data=ds["t850"], time_dim="time", time_groups="month", groupby_dims="node"
)
# Global (over space)
scaler3 = GlobalScaler(data=ds, groupby_dims="node")  # minmax

final_scaler = SequentialScaler(scaler1, scaler2, scaler3)

final_scaler.fit()
print(final_scaler.list_scalers)

ds_trans = final_scaler.transform(ds).compute()
ds_invert = final_scaler.inverse_transform(ds_trans).compute()
xr.testing.assert_allclose(ds, ds_invert)

##----------------------------------------------------------------------------.
# ###################
#### Climatology ####
# ###################
from modules.xscaler import Climatology
from modules.xscaler import LoadClimatology

reference_period = np.array(["1980-01-01T00:00", "2010-12-31T23:00"], dtype="M8")
reference_period = ("1980-01-01T00:00", "2010-12-31T23:00")

### Daily climatology
daily_clim = Climatology(
    data=ds_dynamic,
    time_dim="time",
    time_groups=["day", "month"],
    groupby_dims="node",
    reference_period=reference_period,
    mean=True,
    variability=True,
)

daily_clim1 = Climatology(
    data=ds_dynamic,
    time_dim="time",
    time_groups="dayofyear",
    groupby_dims="node",
    reference_period=reference_period,
    mean=True,
    variability=True,
)
# - Compute the climatology
daily_clim.compute()
daily_clim1.compute()

print(daily_clim.mean)
print(daily_clim1.mean)
print(daily_clim.variability)
print(daily_clim1.variability)

# - Forecast climatology
ds_forecast = daily_clim.forecast(ds_dynamic["time"].values)
ds_forecast1 = daily_clim.forecast(ds_dynamic["time"].values)
print(ds_forecast)
xr.testing.assert_allclose(ds_forecast, ds_forecast1)

### 3-hourly weekly climatology
custom_clim = Climatology(
    data=ds_dynamic,
    time_dim="time",
    time_groups={"hour": 3, "weekofyear": 1},
    groupby_dims="node",
    mean=True,
    variability=True,
)
# - Compute the climatology
custom_clim.compute()

print(custom_clim.mean)
print(custom_clim.variability)

# - Forecast climatology
ds_forecast = custom_clim.forecast(ds_dynamic["time"].values)

# - Save
fpath = "/home/ghiggi/clim_test.nc"
custom_clim.save(fpath)

# - Reload
custom_clim = LoadClimatology(fpath)

# - Forecast
custom_clim.forecast(ds_dynamic["time"].values)

##----------------------------------------------------------------------------.
# ###############
#### AnomalyScaler ####
# ###############
from modules.xscaler import AnomalyScaler
from modules.xscaler import LoadScaler

reference_period = np.array(["1980-01-01T00:00", "2010-12-31T23:00"], dtype="M8")
reference_period = ("1980-01-01T00:00", "2010-12-31T23:00")

### Daily anomalies
daily_anom = AnomalyScaler(
    data=ds_dynamic,
    time_dim="time",
    time_groups=["day", "month"],  # dayofyear
    groupby_dims="node",
    reference_period=reference_period,
)
daily_anom.fit()

ds_anom = daily_anom.transform(ds_dynamic, standardize=False).compute()
ds_std_anom = daily_anom.transform(ds_dynamic, standardize=True).compute()

ds_orig1 = daily_anom.inverse_transform(ds_anom).compute()
ds_orig2 = daily_anom.inverse_transform(ds_std_anom, standardized=True).compute()
xr.testing.assert_equal(ds, ds_orig1)
xr.testing.assert_equal(ds, ds_orig2)

# Save to disk
fpath = "/home/ghiggi/anom_test.nc"
daily_anom.save(fpath)

# - Reload
daily_anom1 = LoadScaler(fpath)
ds_anom = daily_anom1.transform(ds_dynamic, standardize=False).compute()
ds1 = daily_anom1.inverse_transform(ds_anom).compute()
xr.testing.assert_equal(ds, ds1)

##----------------------------------------------------------------------------.
# ######################
#### OneHotEncoding ####
# ######################
from modules.xscaler import OneHotEnconding
from modules.xscaler import InvertOneHotEnconding

da_slt = ds_static["slt"].round(0)

ds_OHE = OneHotEnconding(da_slt, n_categories=None)
da_slt1 = InvertOneHotEnconding(ds_OHE, name="slt")
xr.testing.assert_equal(da_slt, da_slt1)
##----------------------------------------------------------------------------.
