from Module1 import classify_value
import pandas as pd
import streamlit as st

def custom_interleave(a, b):
    result = []
    pattern = [3, 'b', 2, 'b', 1, 'b', 2, 'b']
    a_idx, b_idx = 0, 0

    for p in pattern:
        if isinstance(p, int):  # take p elements from a
            result.extend(a[a_idx:a_idx+p])
            a_idx += p
        elif p == 'b':  # take 1 element from b
            if b_idx < len(b):
                result.append(b[b_idx])
                b_idx += 1
    return result

def process_and_export_data(lines_split_into_words):
    
    combined_list = []
    for i in range(0, len(lines_split_into_words), 2):
        a = lines_split_into_words[i]
        b = lines_split_into_words[i+1] if i+1 < len(lines_split_into_words) else []
        combined = custom_interleave(a, b)
        combined_list.append(combined)
    
    '''
    # Step 1: Iterate backwards through the data list
    for i in range(len(lines_split_into_words) - 1, 0, -2):  # Start from the second-to-last item, step -2
        # Insert values from the current row (lines_split_into_words[i]) into the previous row (lines_split_into_words[i-1])
        lines_split_into_words[i-1].insert(3, lines_split_into_words[i][0])  # Insert 1st element from current row to 3rd position in previous row
        lines_split_into_words[i-1].insert(6, lines_split_into_words[i][1])  # Insert 2nd element from current row to 6th position in previous row
        lines_split_into_words[i-1].insert(8, lines_split_into_words[i][2])  # Insert 3rd element from current row to 8th position in previous row
        lines_split_into_words[i-1].append(lines_split_into_words[i][3])    # Append 4th element from current row to the end of the previous row

        # Delete the current row (lines_split_into_words[i])
        del lines_split_into_words[i]
    '''
    # Step 2: Process date and loan number for each sublist
    for sublist in combined_list:
        date = sublist[1]  # The second column is the date
        loan_num = sublist[0]  # The first column is the loan number

        # Check for asterisk in the date and process accordingly
        if '*' in date:
            sublist[1] = date.rstrip('*')  # Remove asterisk from the date
            sublist.append('*')  # Append '*' to the end if asterisk exists in the date
        else:
            sublist.append('')  # Append empty string if no asterisk in date

        # Check for double asterisks in the loan number (first column) and process accordingly
        if '**' in loan_num:
            sublist[0] = loan_num.lstrip('**')  # Remove leading '**' from loan number
            sublist.append('**')  # Append '**' to the end if double asterisk exists in loan number
        else:
            sublist.append('')  # Append empty string if no '**' in loan number

    # Step 3: Classify and convert all values in the sublists (handle negatives and classification)
    modified_data = [
        [classify_value(value) for value in row]
        for row in combined_list
    ]
    # Step 4: Define the column names for the DataFrame
    cols = [
        "AccountNo",
        "Next Pmt Due Date",
        "Lst Yr Cushion",
        "New Cushion",
        "PrinInt Pmt",
        "Curr Esc Pmt",
        "New Esc Pmt",
        "Curr Balance",
        "Ant Balance",
        "Balance Reqd",
        "Surplus/Shortage",
        "Deficiency Amt",
        "Past Due",
        "BK"
    ]


    # Step 5: Create the DataFrame
    export_df = pd.DataFrame(modified_data, columns=cols)
    

    # First, create the new column 'Shtg + Def/ Surplus' by adding 'Surplus/Shortage' and 'Deficiency Amt'
    export_df['Shtg + Def/ Surplus'] = export_df['Surplus/Shortage'] + export_df['Deficiency Amt']

    # Remove the column and then insert it at position 14
    column_data = export_df.pop('Shtg + Def/ Surplus')
    export_df.insert(12, 'Shtg + Def/ Surplus', column_data)

    # Step 6: Return the DataFrame
    return export_df