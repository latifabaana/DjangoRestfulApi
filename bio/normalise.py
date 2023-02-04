import pandas as pd
import os
import sys

# go back one direction from current working directory so the variable holds the midterm-proj directory
midterm_directory = os.path.normpath(os.getcwd() + os.sep + os.pardir)

# read first file (which represents the protein table) and add column names
protein_data = pd.read_csv(os.path.join(midterm_directory, 'dataSequences.csv'), names = ['proteinID', 'proteinSequence'])
# create dataframe for protein table
df = pd.DataFrame(protein_data)
df.reset_index(inplace=True)

# read the second file. 
All_data = pd.read_csv(os.path.join(midterm_directory, 'dataSet.csv'), names = ['proteinID', 'taxaID', 'cladeID','scientificName', 'domainDescription', 'domainID', 'domainStart', 'domainEnd', 'proteinLength'])
# create dataframe for second file
allData_df = pd.DataFrame(All_data)
allData_df.reset_index(inplace=True)
# split scientific name column to 2 columns: genus and species
allData_df[['genus', 'species']] = allData_df.scientificName.str.split(" ", n=1, expand = True)
allData_df['species'] = allData_df['species'].str.replace('sp.', '')

# create the organism dataframe which represents the organism table
df_organisms = allData_df[['proteinID', 'taxaID', 'cladeID', 'scientificName', 'genus', 'species']]

# create the domain dataframe which represents the domain table
df_Domain = allData_df[['proteinID', 'domainID', 'domainDescription', 'domainStart', 'domainEnd']]

# add proteinLength to the protein dataframe
df['proteinLength'] = allData_df['proteinLength']

# creates the domainFamily csv
domainFamily_data = pd.read_csv(os.path.join(midterm_directory, 'pfamDescriptions.csv'), names = ['domainID','domainFamilyDescription'])
domainFamily_df = pd.DataFrame(domainFamily_data)
domainFamily_df.reset_index(inplace=True)

# drop all duplicates
df_organisms = df_organisms.drop_duplicates()
df = df.drop_duplicates()
df_Domain = df_Domain.drop_duplicates()
domainFamily_data = domainFamily_data.drop_duplicates()

# export the dataframes into new csv files. 
df.to_csv(os.path.join(midterm_directory, 'proteins.csv'), index = False)
domainFamily_df.to_csv(os.path.join(midterm_directory, 'domainFamily.csv'), index = False)
df_organisms.to_csv(os.path.join(midterm_directory, 'organisms.csv'), index = False)
df_Domain.to_csv(os.path.join(midterm_directory, 'domain.csv') , index = False)
