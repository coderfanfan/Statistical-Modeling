from pandas import Series, DataFrame
import numpy as np
import pandas as pd

#lakeNeighbor = pd.read_csv("LakeNeighbor_trans_6year_v3.csv")
lakeMeta = pd.read_csv("lake_metadata.csv")
weather = pd.read_csv("weatherdata.csv")


#merge lakeNeighbor with lake meta data
#lakeNeighbor = lakeNeighbor.merge(lakeMeta, left_on = "pw_MCES_Map_Code1", right_on = "DNR_ID_SITE_NUMBER")

#calculate by county yearly May-Sep average precipitation 
prcp = weather[(weather['MONTH'] <= 9)& (weather['MONTH'] >= 5)]
prcp = prcp.groupby(['COUNTY','YEAR']).mean()['PRCP']
prcp = prcp.reset_index()

#calculate by county June - May average snow and label with the year of the second half months 
snow1 = weather[(weather['MONTH'] <= 3)& (weather['MONTH'] >= 1)]
snow1 = snow1.groupby(['COUNTY','YEAR']).sum()['SNOW']
snow1 = snow1.reset_index()
snow2 = weather[(weather['MONTH'] <= 12)& (weather['MONTH'] >= 10)]
snow2 = snow2.groupby(['COUNTY','YEAR']).sum()['SNOW']
snow2 = snow2.reset_index()
snow2 = pd.concat([snow2.ix[:,0:2], snow2.groupby('COUNTY')['SNOW'].shift(1)],axis = 1)
snow = snow1.merge(snow2, on = ['COUNTY','YEAR'])
snow['nearwinter_snow'] = snow['SNOW_x'] + snow['SNOW_y']

#merge lakeNeighbor with prcp and snow
#lakeNeighbor = lakeNeighbor.merge(prcp, left_on = ['COUNTY','p_year'], right_on = ['COUNTY','YEAR'])
#lakeNeighbor = lakeNeighbor.merge(snow, left_on = ['COUNTY','p_year'], right_on = ['COUNTY','YEAR'])
#lakeNeighbor = lakeNeighbor.drop(['YEAR_x','YEAR_y','SNOW_x','SNOW_y'], axis = 1)

#lakeNeighbor.to_csv("lakeNeighbor_ext_v3.csv")
