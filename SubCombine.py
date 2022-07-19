# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 03:11:53 2022
@author: Elu5iv3
"""

# importing pandas
import pandas as pd
  
# read text file into pandas DataFrame
df = pd.read_table("testP.srt", delimiter="\n")


lineID = [1] 
startTime = [] 
endTime = [] 
text = []
time = []

# Add each value to the correct list
for index, row in df.iterrows():
    if index % 3 == 0: 
        time.append(row[0])
    
    elif index % 3 == 1:
        text.append(str(row[0]))
    
    elif index % 3 == 2:
        lineID.append(int(row[0]))

# Create a DataFrame with the values
dfde7ko = pd.DataFrame(list(zip(lineID, time, text)),
               columns =['ID', 'Time', 'Text'])

dfde7ko[['Start_Time', 'End_Time']] = dfde7ko['Time'].str.split(' --> ', expand=True, n=1)


dfSRTForm = dfde7ko.drop(columns=['Time'])

dfde7ko['Start_Time'] = pd.to_datetime(dfde7ko['Start_Time'])
dfde7ko['End_Time'] = pd.to_datetime(dfde7ko['End_Time'])

dfClean = dfde7ko.drop(columns=['Time'])

dfClean['Difference'] = (dfClean['End_Time']-dfClean['Start_Time']).astype('timedelta64[s]')


# Create a loop to go over the rows and update it to fit the min seconds on screen requirement
indexKeep = len(dfClean.index)
minSec = 3 # min number of seconds of screen time per line of subtitles.

for i in range(0, indexKeep):
    try:
        while dfClean.at[i, 'Difference'] < minSec:
            dfClean.at[i, 'Text'] = dfClean.at[i, 'Text'] + ' ' + dfClean.at[i+1, 'Text']
            dfSRTForm.at[i, 'Text'] = dfSRTForm.at[i, 'Text'] + ' ' + dfSRTForm.at[i+1, 'Text']
        
            dfClean.at[i, 'End_Time'] = dfClean.at[i+1, 'End_Time']
            dfSRTForm.at[i, 'End_Time'] = dfSRTForm.at[i+1, 'End_Time']
        
            dfClean = dfClean.drop(i+1)
            dfSRTForm = dfSRTForm.drop(i+1)
        
            dfClean = dfClean.reset_index()
            dfClean = dfClean.drop(columns='index')
        
            dfSRTForm = dfSRTForm.reset_index()
            dfSRTForm = dfSRTForm.drop(columns='index')
        
            dfClean['Difference'] = (dfClean['End_Time']-dfClean['Start_Time']).astype('timedelta64[s]')
            
            indexKeep = len(dfClean.index)
    except KeyError: # Takes care of condensed number of rows
        pass
    
###########################################################
#                Clean lists and Exporting                #
###########################################################

lineID = [] 
text = []
time = []

columns = ['Start_Time', 'End_Time']
dfExport = dfSRTForm
dfExport['Time'] = dfExport.agg('{0[Start_Time]} --> {0[End_Time]}'.format, axis=1)
dfExport.drop(columns, inplace=True, axis=1)

for l in range(1, indexKeep+1):
    lineID.append(l)
for l in range(0, indexKeep):
    time.append(str(dfExport.at[l, 'Time']))
    text.append(str(dfExport.at[l, 'Text']))

with open(r'D:\SubCombine\test_polished.srt', 'w', encoding="utf-8") as f:
    for xyz in zip(lineID, time, text):
        f.write('%s\n%s\n%s\n\n'%xyz)
