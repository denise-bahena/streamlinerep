import re

def classify_value(value):
    # Strip leading/trailing spaces before processing
    value = value.strip()

    # Handle negative numbers by checking if there's a leading minus sign
    if value.startswith('-'):
        # Handle negative integers
        if value[1:].isdigit():  # If the part after '-' is all digits, it's an integer
            try:
                return int(value)  # Try converting to int
            except ValueError:
                return value  # Return as string if it can't be converted to int
        # Handle negative floats
        elif value[1:].replace('.', '', 1).isdigit():  # If the part after '-' is a valid float
            try:
                return float(value)  # Convert to float
            except ValueError:
                return value  # Return as string if it can't be converted to float
        else:
            return value  # Return as string if it can't be converted to int or float
    else:
        # Handle positive integers
        if value.isdigit():  # If it's all digits, it's an integer
            try:
                return int(value)  # Convert to int
            except ValueError:
                return value  # Return as string if it can't be converted to int
        # Handle positive floats
        elif value.replace('.', '', 1).isdigit() and value.count('.') <= 1:  # Valid float check
            try:
                return float(value)  # Convert to float
            except ValueError:
                return value  # Return as string if it can't be converted to float
        else:
            return value  # Return as string if it's neither an int nor a float


def process_file(file_content):
    lines = file_content.splitlines()

    # Clean up the lines: remove leading/trailing spaces and extra spaces between words
    cleaned_lines = [re.sub(r'\s+', ' ', line.strip()) for line in lines if line.strip()]

    # Split the cleaned lines into words
    lines_split_into_words = [line.split() for line in cleaned_lines]

    # Iterate over the lines in reverse order
    for i in range(len(lines_split_into_words) - 1, -1, -1):
        # Removing commas from values
        lines_split_into_words[i] = [item.replace(',', '') for item in lines_split_into_words[i]]
        temp_var = lines_split_into_words[i][0]

        # Check if '*' is in the value and handle accordingly
        if '*' in temp_var:
            temp_var = temp_var.strip('*')
            temp_var = classify_value(temp_var)
            if isinstance(temp_var, str):  # If it's still a string, delete this line
                del lines_split_into_words[i]
        else:
            # Try classifying the value
            temp_var = classify_value(temp_var)
            if isinstance(temp_var, str):  # If it's still a string, delete this line
                del lines_split_into_words[i]

    return lines_split_into_words

