import pandas as pd
import math
import numpy as np
from pathlib import Path
import streamlit as st
from taxontabletools2.utilities import collect_traits
from taxontabletools2.utilities import strip_traits
from taxontabletools2.utilities import collect_metadata
from taxontabletools2.utilities import load_df
from taxontabletools2.utilities import collect_replicates
from taxontabletools2.utilities import export_taxon_table
from taxontabletools2.utilities import simple_taxontable
from taxontabletools2.utilities import update_taxon_table

def presence_absence_table(taxon_table_xlsx, taxon_table_df, samples, metadata_df, traits_df):
    ## create copies of the dataframes
    taxon_table_df = taxon_table_df.copy()
    metadata_df = metadata_df.copy()
    traits_df = traits_df.copy()

    ## set all element to 0/1
    taxon_table_df[samples] = taxon_table_df[samples].apply(lambda x: (x != 0).astype(int))

    ## export table
    suffix = 'PA'
    export_taxon_table(taxon_table_xlsx, taxon_table_df, traits_df, metadata_df, suffix)

def simplify_table(taxon_table_xlsx, taxon_table_df, samples, metadata_df, traits_df):
    # merge duplicate OTUs
    save = False
    filtered_df = simple_taxontable(taxon_table_xlsx, taxon_table_df, samples, metadata_df, save)
    ## export the dataframe
    new_TaXon_table_xlsx = str(Path(taxon_table_xlsx)).replace('.xlsx', '_simplified.xlsx')
    with pd.ExcelWriter(new_TaXon_table_xlsx) as writer:
        filtered_df.to_excel(writer, sheet_name='Taxon Table', index=False)
        metadata_df.to_excel(writer, sheet_name='Metadata Table', index=False)

def add_traits_from_file(taxon_table_xlsx, taxon_table_df, samples, metadata_df, traits_df, new_traits_df, taxon_col):
    ## create copies of the dataframes
    taxon_table_df = taxon_table_df.copy()
    metadata_df = metadata_df.copy()
    traits_df = traits_df.copy()

    for row in new_traits_df.values.tolist():
        taxon = row[0]
        traits = row[1:]
        for trait, trait_name in zip(traits, new_traits_df.columns.tolist()[1:]):
            # Find the index of the rows in taxon_table_df that match the taxon
            indices = taxon_table_df[taxon_table_df[taxon_col] == taxon].index
            # Add traits to each matching row in taxon_table_df
            for index in indices:
                traits_df.loc[index, trait_name] = trait

    traits_df = traits_df.fillna('')
    update_taxon_table(taxon_table_xlsx, taxon_table_df, traits_df, metadata_df, '')

def sort_samples(taxon_table_xlsx, taxon_table_df, samples, metadata_df, traits_df):
    ## create copies of the dataframes
    taxon_table_df = taxon_table_df.copy()
    metadata_df = metadata_df.copy()
    traits_df = traits_df.copy()

    # Collect the sorted samples
    sorted_samples = metadata_df['Sample'].values.tolist()
    taxon_table_df_sorted = taxon_table_df[taxon_table_df.columns.tolist()[:9] + sorted_samples]

    update_taxon_table(taxon_table_xlsx, taxon_table_df_sorted, traits_df, metadata_df, '')

def rename_samples(taxon_table_xlsx, taxon_table_df, samples, metadata_df, traits_df, selected_metadata):
    # Create copies of the dataframes
    taxon_table_df = taxon_table_df.copy()
    metadata_df = metadata_df.copy()
    traits_df = traits_df.copy()

    # Collect the new sample names from the selected_metadata column
    sorted_samples = metadata_df['Sample'].values.tolist()
    new_names = metadata_df[selected_metadata].values.tolist()

    # Rename columns in taxon_table_df using the old and new sample names
    for old, new in zip(sorted_samples, new_names):
        taxon_table_df.rename(columns={old: new}, inplace=True)

    # Update the metadata DataFrame with the old and new sample names
    metadata_df['Old names'] = sorted_samples
    metadata_df['Sample'] = new_names

    # Call the update function to apply changes
    update_taxon_table(taxon_table_xlsx, taxon_table_df, traits_df, metadata_df, '')

