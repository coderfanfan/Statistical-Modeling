# -*- coding: utf-8 -*-
'''
These functions can generate variables related to the trends of lake data
'''

from pandas import Series, DataFrame
import numpy as np
import pandas as pd

LakeNeighbor = pd.read_csv("allLakeNeighborhood_panel_dt_v3.csv")

def consistentyear (df, yearcol):
    #add new column 'consistentYear' to a dataframe indicating the number of consistent years 
    #since the earliest year
    #df: the inpute data frame
    #yearcol: column containing the year
    df = df.sort(yearcol, ascending = True)
    df['consistentYear'] = 0
    for i in range(1,len(df)):
        if df[yearcol].iloc[i] == df[yearcol].iloc[i-1] + 1:
            df['consistentYear'].iloc[i] = df['consistentYear'].iloc[i-1] + 1 
        else:
            df['consistentYear'].iloc[i] = 0
    return df
        

def uptrend (df, yearcol, attrcol):
    #add new column 'uptrenyears' to a dataframe indicating the number of consistent years 
    #that an attribute increases
    #df: the inpute dataframe
    #yearcol: column containing the year 
    #attrcol: column containing the attribute
    df['uptrendyears'] = 0
    for row in range(1,len(df)):
        if df[yearcol].iloc[row] == df[yearcol].iloc[row-1]+ 1 and df[attrcol].iloc[row] > df[attrcol].iloc[row-1]:
            df['uptrendyears'].iloc[row] = df['uptrendyears'].iloc[row-1] + 1
        else:
            df['uptrendyears'].iloc[row] = 0
    return df


def downtrend (df, yearcol, attrcol):
    #add new column 'downtrenyears' to a dataframe indicating the number of consistent years 
    #that an attribute decreases
    #df: the inpute dataframe
    #yearcol: column containing the year 
    #attrcol: column containing the attribute
    df['downtrendyears'] = 0
    for row in range(1,len(df)):
        if df[yearcol].iloc[row] == df[yearcol].iloc[row-1] + 1 and df[attrcol].iloc[row] < df[attrcol].iloc[row-1]:
            df['downtrendyears'].iloc[row] = df['downtrendyears'].iloc[row-1] + 1
        else:
            df['downtrendyears'].iloc[row] = 0
    return df


LakeNeighbor_trans = DataFrame()        
for i in LakeNeighbor['pw_MCES_Map_Code1'].unique():
    df = LakeNeighbor[LakeNeighbor['pw_MCES_Map_Code1'] == i]
    df = consistentyear (df, 'p_year')
    df = uptrend (df, 'p_year','avgTP')
    df = downtrend (df, 'p_year','avgTP')
    LakeNeighbor_trans = LakeNeighbor_trans.append(df)

#LakeNeighbor_trans.to_csv("LakeNeighbor_trans_6year_v3.csv")