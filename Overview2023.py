"""
Created on Fri March 31 2023

@author: Alfonso Ortigado-Lopez.

"""
print('\n===============================================')
print('Beginning of the summary report of the results')
print('===============================================')

import os, shutil
import glob
import pandas as pd
import numpy as np

# Input to define the path to the folder with the result file
resultpath = input("""Define the path to the result file:  """).strip()
print()

# Change to the directory where the file is located
os.chdir(resultpath)
file = glob.glob("Result*")[0]

# Get the filename without the extension.
filename = os.path.splitext(file)[0]

# Read the file
df = pd.read_csv(file, delimiter = ';', header = 0)

# Remove 'Others' interactions
df = df.drop(index=df.loc[df['Representative_Pose'] == 'Others'].index).reset_index(drop=True)

# Generate two new columns H and Pi in order to count their occurrences.
for i in range(len(df)):
  if df.loc[i,'Interaction'].startswith('H') :
    df.at[i,'H'] = 1
  if df.loc[i,'Interaction'].startswith('P') :
    df.at[i,'Pi'] = 1
df.fillna(0, inplace=True)

# Generate a list to store the loop files
list_df = []

for c in df.Compound.unique(): 
  # Group by compounds
  grupos = (df.loc[df['Compound'] == c ]).groupby('Cluster_Num')

  # Record the compound as many times as there are clusters.
  Compound = []
  for i in range(len(grupos)):
    Compound.append(c)

  # Group the number of clusters in one row
  cluste_num = []
  cluste_num = np.array(grupos['Cluster_Num'].unique())

  # Group the cluster members in a row
  cluste_memb = []
  cluste_memb = np.array(grupos['Cluster_Members'].unique())

  # Group the representative pose of the cluster in a line
  Rep_Pose = []
  Rep_Pose = np.array(grupos['Representative_Pose'].unique())

  # Count the H and Pi interactions of the representative pose of each cluster.
  H_count = []
  Pi_count = []
  H_count = np.array(grupos['H'].sum())
  Pi_count = np.array(grupos['Pi'].sum())

  # Group the interactions of each cluster
  Residue = []
  Residue = np.array(grupos['Residue'].apply(lambda x: ''.join(x)))

  # Group data in a temporary table
  df_temporal =  pd.DataFrame({'Compound': Compound,
                               'Cluster_Num': cluste_num,
                               'Cluster_Memb': cluste_memb,
                               'Representative_pose': Rep_Pose,
                               'H_interactions': H_count,
                               'Pi_Interactions': Pi_count,
                               'Residues': Residue})

  # Add the results to the table list
  list_df.append(df_temporal)

# Save the table in a final file
df_final = pd.concat(list_df, axis=0, ignore_index=True)


# Adjust the content of the boxes
columns_to_adjust = ['Cluster_Memb', 'Cluster_Num', 'Representative_pose', 'Residues']

for column in columns_to_adjust:
    df_final[column] = df_final[column].astype(str)
    df_final[column] = df_final[column].str.replace('[', '').str.replace(']', '').str.strip("'")
    if column == 'Residues':
        df_final[column] = df_final[column].str.replace(':', ', ').str.replace(':', ', ').apply(lambda x: x[2:] if x.startswith(', ') else x)

# Function to transform the value of 'Representative_pose'.
def transform_pose(pose):
    suffix = pose.split('_')[1]
    return 'P' + suffix

# Function to transform the value of 'Cluster_Memb'.
def transform_pose_cluster(pose):
    poses = pose.split(', ')
    cluster = ', '.join([f'P{p.split("_")[1]}' for p in poses])
    return cluster

# Apply the generated functions
df_final['Representative_pose'] = df_final['Representative_pose'].apply(transform_pose)
df_final['Cluster_Memb'] = df_final['Cluster_Memb'].apply(transform_pose_cluster)

# Export the data frame
df_final.to_csv(f"overview_results_{filename}.csv", sep=";", index=False)

print('\n==================================================================================')
print(f'\n The summary report has been saved as: overview_results_{filename}.csv')
print(f'\n File location: {resultpath}')
print(f'\n The analysis is finished ')
print('==================================================================================')