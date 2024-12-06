import pandas as pd
from pandas import DataFrame
import numpy as np
from pathlib import Path

# read_table_xlsx = '/Users/tillmacher/Documents/GitHub/TaxonTableTools/_tutorial_files/tutorial_read_table_TTT.xlsx'
# taxonomy_table_xlsx = '/Users/tillmacher/Documents/GitHub/TaxonTableTools/_tutorial_files/tutorial_taxonomy_table.xlsx'
# TaXon_table_name = 'this_is_a_test'
# taxonomy_table_format = 'JAMP hit'
# path_to_outdirs = '/Users/tillmacher/Desktop/ttt_projects/Projects/Dessau_Vertebrates'

def taxon_table_converter_ttt(read_table_xlsx, taxonomy_table_xlsx, TaXon_table_name, taxonomy_table_format, path_to_outdirs):

    ## format working sheet name
    if taxonomy_table_format == 'Taxonomy table (APSCALE)':
        taxonomy_table_format = 'Taxonomy table'

    ## collect both input files
    taxonomy_table_xlsx =  Path(taxonomy_table_xlsx)
    read_table_xlsx = Path(read_table_xlsx)

    #ä create filename and path for output file
    Output_name = TaXon_table_name + ".xlsx"
    Output_file = Path(path_to_outdirs) / "TaXon_tables" / Output_name

    ## store the file name for later use
    file_name = taxonomy_table_xlsx.name

    ## create dataframes for both files
    taxonomy_df = pd.read_excel(taxonomy_table_xlsx, taxonomy_table_format, header=0)
    if taxonomy_table_format == "BOLDigger hit":
        taxonomy_df = taxonomy_df.drop(columns=['Flags'])
    read_table_df = pd.read_excel(read_table_xlsx, header=0)

    ## create a new dataframe
    TaXon_table_df = taxonomy_df

    # check if all OTU are correctly sorted and present in both files
    if taxonomy_df["ID"].to_list() == read_table_df["ID"].to_list():

        ## append the sequences to the TaXon stable
        TaXon_table_df["seq"] = read_table_df["Sequences"]

        ## remove the sequence column from the read table
        read_table_df.drop('Sequences', axis='columns', inplace=True)

        ## remove the ID column from the read table
        read_table_df.drop('ID', axis='columns', inplace=True)

        ## add samples to the dataframe
        TaXon_table_df = pd.concat([TaXon_table_df, read_table_df], axis=1)

        ## check if species are present as "Genus" + "Epithet"
        new_species_column = []
        for OTU in TaXon_table_df[["Genus", "Species"]].fillna("nan").values.tolist():
            if (OTU != ["nan", "nan"] and OTU[1] != 'nan'):
                if OTU[0] not in OTU[1]:
                    new_species_column.append(OTU[0] + " " + OTU[1])
                else:
                    new_species_column.append(OTU[1])
            else:
                new_species_column.append("")

        ## add new species column to the dataframe
        TaXon_table_df["Species"] = new_species_column

        ## save the newly created Taxon table in TaXon format as excel file
        TaXon_table_df.to_excel(Output_file, sheet_name='TaXon table', index=False)

        return ('Finished: Please select your new TaXon table above.')

    else:
        return 'Error: Please check your input files!'

def taxon_table_converter_qiime2(read_table_tsv, taxonomy_table_xlsx, TaXon_table_name, taxonomy_table_format, path_to_outdirs):

    taxonomy_table_xlsx =  Path(taxonomy_table_xlsx)
    read_table_tsv = Path(read_table_tsv)

    # create filename and path for output file
    Output_name = TaXon_table_name + ".xlsx"
    Output_file = Path(path_to_outdirs) / "TaXon_tables" / Output_name

    # store the file name for later use
    file_name = taxonomy_table_xlsx.name

    # create datafrmes for both files
    taxonomy_df = pd.read_excel(taxonomy_table_xlsx, taxonomy_table_format, header=0)
    if taxonomy_table_format == "BOLDigger hit":
        taxonomy_df = taxonomy_df.drop(columns=['Flags'])

    read_table_df = pd.read_csv(Path(read_table_tsv), sep="\t")

    # drop the first row
    read_table_df = read_table_df.iloc[1:]
    read_table_df = read_table_df.reset_index(drop=True)

    ## create a new dataframe
    TaXon_table_df = taxonomy_df

    # check if all OTU are correctly sorted and present in both files
    if taxonomy_df["ID"].to_list() == read_table_df["id"].to_list():

        ## append the sequences to the TaXon stable
        TaXon_table_df["seq"] = read_table_df["Sequence"].values.tolist()

        ## remove the sequence column from the read table
        read_table_df.drop('Sequence', axis='columns', inplace=True)

        ## remove the ID column from the read table
        read_table_df.drop('id', axis='columns', inplace=True)

        ## add samples to the dataframe
        TaXon_table_df = pd.concat([TaXon_table_df, read_table_df], axis=1)

        ## check if species are present as "Genus" + "Epithet"
        new_species_column = []
        for OTU in TaXon_table_df[["Genus", "Species"]].fillna("nan").values.tolist():
            if (OTU != ["nan", "nan"] and OTU[1] != 'nan'):
                if OTU[0] not in OTU[1]:
                    new_species_column.append(OTU[0] + " " + OTU[1])
                else:
                    new_species_column.append(OTU[1])
            else:
                new_species_column.append("")

        ## add new species column to the dataframe
        TaXon_table_df["Species"] = new_species_column

        ## save the newly created Taxon table in TaXon format as excel file
        TaXon_table_df.to_excel(Output_file, sheet_name='TaXon table', index=False)

        return ('Finished: Please select your new TaXon table above.')

    else:
        return 'Error: Please check your input files!'
