
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm



def load_data(filepath):
    """Loads the data from a CSV containing two tables."""
    df = pd.read_csv(filepath)
    
    #identify the column headers of second table for seperation
    separator_part1 = 'Variable Question'
    separator_part2 = 'Variable Label'
    separator_index = -1

    first_row = df.iloc[0].astype(str)
    
    #splitting the 2 tables line by line
    for i in range(len(first_row) - 1):
        if first_row[i].strip() == separator_part1 and first_row[i + 1].strip() == separator_part2:
            separator_index = i
            break

    #error handling
    if separator_index == -1:
        raise ValueError("Table separation not found.")

    table1 = df.iloc[:, :separator_index]
    table2 = df.iloc[:, separator_index:]
    table2 = table2.iloc[1:]

    # Trim table1 and table2
    table1 = table1.iloc[:, :-2]  # Remove the last two columns
    table2 = table2.iloc[:8, :] # Remove rows after row 8 (indexes 0 to 8 are kept)

    return table1, table2

def map_response_ids(table1, table2):
    """Maps response IDs in table1 to their meanings in table2."""

    # Create a mapping dictionary from table2.
    mapping = dict(zip(table2.iloc[:, 0], table2.iloc[:, 1]))

    # Rename columns in table1 based on the mapping
    cols_to_rename = [col for col in table1.columns if col.startswith('q2_')]
    table1.rename(columns={col: mapping.get(col, col) for col in cols_to_rename}, inplace=True)

    return table1

def clean_data(table1):
    """Cleans and prepares the data for analysis."""
    # Check for duplicates
    table1.drop_duplicates(inplace=True)

    # Replace 'NA' with NaN (for easier handling)
    table1.replace('NA', np.nan, inplace=True)

    # Convert response columns to numeric (if possible)
    response_cols = [col for col in table1.columns if col not in ['date', 'response_id', 'group']]
    for col in response_cols:
        table1[col] = pd.to_numeric(table1[col], errors='ignore')

    # Fill NaN with 0, as NaN in this case means that the response was not selected.
    table1.fillna(0, inplace=True)

    # Convert Date column to date
    table1['date'] = pd.to_datetime(table1['date'], errors='coerce').dt.date

    # Check for consistent Group values
    #print("Unique Group Values:", table1['group'].unique())

    # Check for null values.
    #print(table1.isnull().sum())

    return table1

def create_bar_chart(table1, save_filepath):
    """Groups responses by group and creates a horizontal bar chart with percentages."""
    #cleaning the group column 
    table1['group'] = table1['group'].str.strip() 
    response_cols = table1.columns[3:]
    grouped_data = table1.groupby('group')[response_cols].sum() 

    # Normalise to percentages
    grouped_percentages = grouped_data.apply(lambda row: row / row.sum() * 100, axis=1)

    grouped_percentages = grouped_percentages.T

    #plotting graph
    ax = grouped_percentages.plot(kind='barh', figsize=(12, 6), color=['#00AEEF', '#FB349C', '#FFC000']) #barh creates horizontal bar chart.
    plt.title('Percentage of Responses by Group', fontproperties=font_prop)
    plt.xlabel('Percentage (%)', fontproperties=font_prop)
    plt.ylabel('Responses', fontproperties=font_prop)
    plt.xticks(fontproperties=font_prop)
    plt.yticks(fontproperties=font_prop)
    plt.legend(prop=font_prop)
    
    plt.tight_layout()
    plt.savefig(save_filepath, dpi=500)
    plt.show()
    
    return
    
    
font_path = 'C:\WINDOWS\FONTS\ARIAL.TTF' 
font_prop = fm.FontProperties(fname=font_path)
filepath = r'C:\Users\willp\OneDrive\Desktop\TMP Tasks\JDA Task 2 - Market Research\task_2_data.csv'
table1, table2 = load_data(filepath)
table1 = map_response_ids(table1, table2)
table1 = clean_data(table1)
create_bar_chart(table1, save_filepath="Task_2_Bar_Chart.png")

#print("Table 1 (Trimmed):")
#print(table1.head())

