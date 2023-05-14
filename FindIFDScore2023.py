"""
Created on Thursday April 13 2023

@author: Alfonso Ortigado-López.

"""

print('\n==================================================================================')
print(f'\n Starting program to integrate IFD Score in the overview file')
print('==================================================================================')

import os, shutil, re
import pandas as pd
import numpy as np
import glob

# Input to define the path to the files
resultpath = input("""Define the path to the files:  """).strip()
print()

# Read the file
# Change to the directory where the files are located
os.chdir(resultpath)

# Import dataframe overview
file = glob.glob("overview_results*")[0]
df_overview = pd.read_csv(file, delimiter = ';', header = 0)

# Import the dataframe obtained in maestro (IFD_spreadsheet)
df = pd.read_csv('IFD_spreadsheet.csv', delimiter=',', header=0)
df = df.loc[:, ["Title", "IFDScore"]]

# Change the name of the compound according to the pose
array_new = []

# counter variable to make sure the suffix is added correctly
counter = {}

# Traverse the original array and add the corresponding suffix
for value in np.array(df.Title):

  #Remove underscore
  value = value.replace('_', '')

  if value in counter:
      counter[value] += 1
      new_value = value + "_" + str(counter[value])
  else:
      counter[value] = 1
      new_value= value + "_" + str(counter[value])
  array_new.append(new_value)

df_IFDScore = pd.DataFrame({'Representative_pose': array_new, 'IFDScore': np.array(df.IFDScore)})

# Generate a dictionary to join dataframes together
df_overview['Dictionary'] = df_overview['Compound'] + '_' + df_overview['Representative_pose'].str.replace('P', '')

# Join the data frame
IFDScore = []
for i in range(len(df_overview)):
    pose = df_overview.loc[i, 'Dictionary']
    
    # Find the pose in the other table
    row = df_IFDScore.loc[df_IFDScore['Representative_pose'] == pose]
    if not row.empty:
        score = row['IFDScore'].iloc[0]
    else:
        print(pose)
        score = None
    IFDScore.append(score)

# Generate a final dataframe
final_df = pd.DataFrame({'Compound' : np.array(df_overview.Compound),
                         'Representative_pose': np.array(df_overview.Representative_pose),
                         'IFDScore': IFDScore,
                         'H_bonds': np.array(df_overview.H_interactions),
                         'Pi_bonds':np.array(df_overview.Pi_Interactions),
                         'Cluster_Memb': np.array(df_overview.Cluster_Memb),
                         'Residues': np.array(df_overview.Residues)})


# Sort the df based on the IFDScore spreadsheet
final_df['temp'] = final_df['Representative_pose'].str.replace('P', '')
# Combine the columns 'Compound' and 'Representative_pose'.
final_df['ID'] = final_df['Compound'] + '_' + final_df['temp']
final_df = final_df.drop('temp', axis=1)

# To make a list with order
orden = np.array(df_IFDScore.Representative_pose)
final_df['ID'] = pd.Categorical(final_df['ID'], orden)

# Sort the DataFrame according to the categorical column 'Diction'.
final_df = final_df.sort_values('ID')
final_df = final_df.drop('ID', axis=1)

print(final_df)

# Exporting the data frame
final_df.to_csv(f"overview_results_IFD_Score.csv", sep=";", index=False)

print('\n==================================================================================')
print(f'\n The summary report has been saved as: overview_results_IFD_Score.csv')
print(f'\n File location: {resultpath}')
print(f'\n The analysis is finished ')
print('==================================================================================')