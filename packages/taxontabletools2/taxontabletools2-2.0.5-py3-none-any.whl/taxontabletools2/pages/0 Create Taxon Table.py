import streamlit as st
import pandas as pd
import numpy as np
import subprocess
import glob, sys, time, statistics, os.path, random
from pathlib import Path
import psutil
import plotly.graph_objects as go
from taxontabletools2.start import TTT_variables
from taxontabletools2.utilities import load_df
from taxontabletools2.utilities import collect_replicates
from taxontabletools2.utilities import collect_sample_stats
from taxontabletools2.basic_stats import basic_stats_reads
from taxontabletools2.basic_stats import basic_stats_OTUs
from taxontabletools2.basic_stats import taxonomic_resolution
from taxontabletools2.basic_stats import taxonomic_richness
from taxontabletools2.utilities import collect_traits
from taxontabletools2.utilities import strip_traits
from taxontabletools2.utilities import check_replicates
from taxontabletools2.table_processing import replicate_merging
from taxontabletools2.table_processing import negative_control_subtraction
from taxontabletools2.table_processing import read_based_filter
from taxontabletools2.table_processing import read_based_normalisation
from taxontabletools2.table_processing import taxonomic_filtering
from taxontabletools2.table_processing import sample_filtering
from taxontabletools2.taxontable_conversion import taxon_table_converter_ttt
from taxontabletools2.taxontable_conversion import taxon_table_converter_qiime2
from taxontabletools2.start import start

# Call the sidebar function
settings = start()
users_settings = settings['new_user_preferences_dict']

## Page title
st.write(""" ## Taxon Table conversion """)

a1, a2 = st.columns(2)
with a1:
    st.session_state['otu_table_path'] = st.file_uploader('Select your Read table:')
    st.session_state['otu_table_format'] = st.selectbox('Read table format', ['APSCALE'])

    if st.session_state['otu_table_path'] == None:
        st.write('Please select a Read table!')

with a2:
    st.session_state['taxonomy_table_path'] = st.file_uploader('Select your Taxonomy table:')
    st.session_state['taxonomy_table_format'] = st.selectbox('Taxonomy table format', ['APSCALE', 'BOLDigger'])
    st.session_state['genus_species_merge'] = st.selectbox('Merge the genus and species epithet column', ['Merge', 'No merge'], index=1)

    if st.session_state['taxonomy_table_path'] == None:
        st.write('Please select a Taxonomy table!')

## Save table to project folder
st.session_state['taxon_table_name'] = st.text_input('Taxon table name',
                                                     f'{st.session_state["path_to_outdirs"].name}_taxon_table') + '.xlsx'
st.session_state['taxon_table_path'] = st.session_state['path_to_outdirs'].joinpath('TaXon_tables',
                                                                                  st.session_state['taxon_table_name'])

if st.session_state['taxonomy_table_path'] != None and st.session_state['otu_table_path'] != None:
    if st.button('Convert to TaXon table format'):

        ## collect all individual colummns from the OTU table
        otu_table = pd.read_excel(st.session_state['otu_table_path']).fillna('')
        # otu_table = pd.read_excel('/Volumes/Coruscant/APSCALE_projects/GeDNA_MZB_all_apscale/7_otu_clustering/GeDNA_MZB_all_apscale_OTU_table.xlsx').fillna('')

        ## collect all individual columns from the taxonomy table
        if st.session_state['taxonomy_table_format'] == 'APSCALE':
            sheet_name = 'Taxonomy table'
        elif st.session_state['taxonomy_table_format'] == 'BOLDigger':
            sheet_name = 'BOLDigger hit'
        taxonomy_table = pd.read_excel(st.session_state['taxonomy_table_path'], sheet_name=sheet_name).fillna('')
        # taxonomy_table = pd.read_excel('/Volumes/Coruscant/APSCALE_projects/GeDNA_MZB_all_apscale/10_local_BLAST/BOLDResults_GeDNA_MZB_all_apscale_OTUs_part_1.xlsx', sheet_name=sheet_name).fillna('')

        ## check if the IDs are identical
        otu_table_IDs = otu_table['unique_ID'].values.tolist()
        taxonomy_table_IDs = taxonomy_table['unique_ID'].values.tolist()

        if otu_table_IDs != taxonomy_table_IDs:
            st.error('WARNING: The IDs of the Read table and Taxonomy table do not match! Make sure they are identically sorted!')
        else:
            ## merge the two dataframes
            taxon_table = taxonomy_table.merge(otu_table, how='inner', on='unique_ID')
            ## move the Seq column
            first_sample = otu_table.columns.tolist()[2]
            loc_first_sample = taxon_table.columns.tolist().index(first_sample)
            # Get the Seq column
            seq = taxon_table['Seq']
            # Drop the Seq column from its current position
            taxon_table.drop('Seq', axis=1, inplace=True)
            # Insert the Seq column at the desired location
            taxon_table.insert(loc_first_sample, 'Seq', seq)
            # Rename the ID column
            taxon_table.rename(columns={"unique_ID": "ID"}, inplace=True)

            ## create a metadata_df
            samples = otu_table.columns.tolist()[1:-1]
            metadata_df = pd.DataFrame([[i, ''] for i in samples], columns=['Sample', 'Metadata'])

            ## also add the column 'Kingdom' if that is not included
            if 'Kingdom' not in taxon_table.columns.tolist():
                # Get the index of the column 'Phylum'
                loc_phylum = taxon_table.columns.tolist().index('Phylum')
                # Insert the 'Kingdom' column at the desired location with value 'Life' for all rows
                taxon_table.insert(loc_phylum, 'Kingdom', 'Life')

            if st.session_state['genus_species_merge'] == 'Merge':
                taxon_table['Species'] = taxon_table.apply(
                    lambda row: row['Genus'] + ' ' + row['Species'] if row['Genus'] and row['Species'] else row[
                        'Species'], axis=1)

            ## Display the table!
            st.success('Successfully merged your tables:')
            st.dataframe(taxon_table)

            with pd.ExcelWriter(st.session_state['taxon_table_path']) as writer:
                taxon_table.to_excel(writer, sheet_name='Taxon Table', index=False)
                metadata_df.to_excel(writer, sheet_name='Metadata Table', index=False)
            st.success(f'Saved as \"{st.session_state["taxon_table_path"]}\"')















