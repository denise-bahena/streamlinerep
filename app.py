import streamlit as st
import pandas as pd
import os
from io import StringIO
from Module1 import process_file  # Import the cleaning function from Module1.py
from Module2 import process_and_export_data  # Import the whole_process function from Module2.py
from Module3 import merge_files
# Apply the Times New Roman font to the title using custom CSS
import streamlit as st

# Inject custom CSS to style the buttons
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #D8AF65;  /* Set button color to #D8AF65 */
        color: white;  /* Set button text color to white */
        border-radius: 5px;  /* Optional: Rounded corners */
        padding: 10px 20px;  /* Optional: Adjusts the padding */
        font-size: 16px;  /* Optional: Adjusts the font size */
    }
    .stButton>button:hover {
        background-color: #C89A5A;  /* Optional: Set hover effect color */
    }
    </style>
    """, unsafe_allow_html=True
)

# Add a title to your app with Times New Roman font
st.title("Escrow Analysis Generator")


# Dictionary to store DataFrames by their filenames (to avoid overwriting)
df_dict = {}

# Allow the user to upload multiple files
uploaded_files = st.file_uploader("Please upload all files pertinent to the report", accept_multiple_files=True)

# Variable to control when to display data
show_results = st.button("Process Data")

# Check if any files have been uploaded
if uploaded_files and show_results:
    
    for file in uploaded_files:
        # Get the file extension to determine how to process the file
        file_extension = file.name.split('.')[-1].lower()  # Get the file extension
        
        # Handle CSV files
        if file_extension == 'csv':
            df = pd.read_csv(file)  # Read CSV file into a DataFrame

            # Store the DataFrame in the dictionary with the filename as the key
            df_dict[file.name] = df

        # Handle .lis files (use cleaning function from Module1.py)
        else:
            # Read the .lis file as text
            file_content = file.read().decode("utf-8")

    # Clean the .lis file using the cleaning function from Module1.py
    module1_data = process_file(file_content)

    # Process the cleaned data using the function from Module2.pry
    module2_data = process_and_export_data(module1_data)
            
    module3_data = merge_files(df_dict, module2_data)

    st.write(module3_data)
    # Convert the DataFrame to CSV
    csv = module3_data.to_csv(index=False)  # `index=False` to exclude the index column

    # Create a download button
    st.download_button(
        label="Download Report",  # Label for the button
        data=csv,              # The CSV data
        file_name="export.csv",  # Name of the file to be downloaded
        mime="text/csv"        # MIME type for CSV
        )
else:
    # No files uploaded or "Process Data" button hasn't been clicked yet
    st.write("Upload your files and click the button to process them.")







