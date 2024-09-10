import pandas as pd
import numpy as np

def valid_T1_filter(df, T1_types):
    # Filter the DataFrame to include only rows with any of the T1 types
    df_T1 = df[df['image_description'].isin(T1_types)]
    
    # Group by 'pGUID' and 'EventName', and collect the unique 'image_description' for each group
    id_event_datatypes = df_T1.groupby(['pGUID', 'EventName'])['image_description'].apply(set)
    
    # Identify 'pGUID' and 'EventName' pairs that have at least one of the T1 types
    ids_with_any_T1 = id_event_datatypes.index
    
    # Filter the original DataFrame to keep only the valid 'pGUID' and 'EventName' pairs
    df_valid = df[df.set_index(['pGUID', 'EventName']).index.isin(ids_with_any_T1)]
    
    return df_valid


def required_fmaps_filter(df, fmaps_required):    
    # Group by 'pGUID' and 'EventName' and collect unique datatypes for each group
    id_event_datatypes = df.groupby(['pGUID', 'EventName'])['image_description'].apply(set)
    
    # Identify 'pGUID' and 'EventName' pairs that have all required datatypes
    ids_with_all_datatypes = id_event_datatypes[id_event_datatypes.apply(lambda x: fmaps_required.issubset(x))].index
    
    # Filter the original DataFrame to keep only these 'pGUID' and 'EventName' pairs
    df_valid = df[df.set_index(['pGUID', 'EventName']).index.isin(ids_with_all_datatypes)]
    
    return df_valid

def save_sublist_to_csv(df, csv_filepath):
    # Identify unique subject/session pairs and save to csv
    sublist=df.drop('image_description', axis=1)
    sublist=sublist.drop_duplicates(subset=['pGUID', 'EventName'])

    # Rename columns
    new_column_names = {
    'pGUID': 'subject',
    'EventName': 'session'}
    df.rename(columns=new_column_names, inplace=True)

    sublist.to_csv(csv_filepath, index=False)



