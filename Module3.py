import pandas as pd

def merge_files(df_dict, export_df):
    # Define the columns and keywords inside the function
    cols_headers = {
        "Escrow_Analysis": {
            'lookup_columns': ['Account Nbr', 'Owner Name', 'Major Type Cd', 'Last Analysis Dt'],
            'header_names': {'Owner Name': 'Owner', 'Major Type Cd': 'Major'}
        },
        "New": {
            'lookup_columns': ['Account Nbr', 'Origination Dt'],
            'header_names': {'Origination Dt': 'New'}
        },
        ">12": {
            'lookup_columns': ['Account Nbr', 'Next Sched Pymt Dt'],
            'header_names': {'Next Sched Pymt Dt': 'Disb > 12'}
        },
        "Future": {
            'lookup_columns': ['Account Nbr', 'Allot Eff Dt'],
            'header_names': {'Allot Eff Dt': 'Future Disb'}
        },
        'FLD': {
            'lookup_columns': ['Account Nbr', 'Next Sched Pymt Dt'],
            'header_names': {'Next Sched Pymt Dt': 'FLD'}
        },
        'FPI': {
            'lookup_columns': ['Account Nbr', 'Next Sched Pymt Dt'],
            'header_names': {'Next Sched Pymt Dt': 'FPI'}
        },
        'HOI': {
            'lookup_columns': ['Account Nbr', 'Next Sched Pymt Dt'],
            'header_names': {'Next Sched Pymt Dt': 'HOI'}
        },
        'PMI': {
            'lookup_columns': ['Account Nbr', 'Next Sched Pymt Dt'],
            'header_names': {'Next Sched Pymt Dt': 'PMI'}
        },
        'Taxes': {
            'lookup_columns': ['Account Nbr', 'Next Sched Pymt Dt'],
            'header_names': {'Next Sched Pymt Dt': 'Taxes'}
        },
        'WS': {
            'lookup_columns': ['Account Nbr', 'Effective Dt'],
            'header_names': {'Effective Dt': 'W/S'}
        },
        'Zero': {
            'lookup_columns': ['ACCTNBR', 'REVDATETIME'],
            'header_names': {'REVDATETIME': '$0 Inst'}
        },
        'Spread': {
            'lookup_columns': ['Account Nbr', 'Calc Variable Value'],
            'header_names': {'Calc Variable Value': 'Spread > 12'}
        }
    }
    
    keywords_dict = {
        'Escrow_Analysis': 'Escrow_Analysis',
        'New': 'new_loans',
        '>12': 'Disb_Greater',
        'Future': 'Future_Escrow',
        'FLD': 'Flood',
        'FPI': 'Force_Placed',
        'HOI': 'Homeowners',
        'PMI': 'PMI',
        'Taxes': 'Taxes',
        'WS': 'Water_Sewer',  # Handle Water/Sewer as a list
        'Zero': 'Zero_Instance',
        'Spread': 'Spread',
    }

    # Loop through the filenames and check for matches
    for filename in df_dict.keys():
        nickname = None
        
        # Check if a keyword in the filename matches any in keywords_dict
        for nickname_value, keyword in keywords_dict.items():
            if keyword.lower() in filename.lower():
                nickname = nickname_value
                break  # Exit the loop once a match is found

        # Get the columns to merge on and the header names from cols_headers
        lookup_columns = cols_headers[nickname]['lookup_columns']
        header_names = cols_headers[nickname]['header_names']

        # Ensure no duplicates in the merge key column before merging
        df_dict[filename] = df_dict[filename].drop_duplicates(subset=[lookup_columns[0]])

        # Check for duplicates in export_df before merge (if applicable)
        export_df = export_df.drop_duplicates(subset=['AccountNo'])

        # Perform the merge
        export_df = pd.merge(export_df, df_dict[filename][lookup_columns], 
                             left_on='AccountNo', 
                             right_on=lookup_columns[0], 
                             how='left', 
                             suffixes=('_export', f'_{filename}'))  # Add suffixes to avoid conflicts

        # Rename columns based on header_names
        export_df = export_df.rename(columns=header_names)

        # Drop the redundant 'Account Nbr' column (based on lookup_columns)
        export_df = export_df.drop(columns=lookup_columns[0])

        # Fill missing values with empty strings
        export_df = export_df.fillna('')

    # Define the condition and subtract 12 if the condition is met
    export_df['New Spread'] = ''
        
    # Using .loc[] to ensure proper assignment without chaining
    for i in range(len(export_df['Spread > 12'])):
        if export_df['Spread > 12'].iloc[i] != '' and export_df['Spread > 12'].iloc[i] >= 12:
            export_df.loc[i, 'New Spread'] = export_df['Spread > 12'].iloc[i] - 12
        
    export_df['Who?'] = ''
    export_df['Notes'] = ''

    cols = [
        'AccountNo',
        'Owner',
        'Major',
        'Next Pmt Due Date',
        'Lst Yr Cushion',
        'New Cushion',
        'PrinInt Pmt',
        'Curr Esc Pmt',
        'New Esc Pmt',
        'Curr Balance',
        'Ant Balance',
        'Balance Reqd',
        'Surplus/Shortage',
        'Deficiency Amt',
        'Shtg + Def/ Surplus',
        'Past Due',
        'BK',
        'New',
        'Disb > 12',
        'Future Disb',
        'FLD',
        'FPI',
        'HOI',
        'PMI',
        'Taxes',
        'W/S',
        '$0 Inst',
        'Spread > 12',
        'New Spread',
        'Last Analysis Dt',
        'Who?',
        'Notes'
    ]
    export_df = export_df[cols]
    return export_df
