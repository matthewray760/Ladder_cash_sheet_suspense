import pandas as pd


filename = 'GL_Mappings'

def load_mappings(mapping_filename):
    # Load the Excel file
    excel_file = pd.ExcelFile(fr'C:\Users\matthewray\OneDrive - Clearwater\Desktop\Ladder\Python\GL_Entries\inputs\Mappings\{mapping_filename}.xlsx')
    
    # Get all sheet names
    all_sheets = excel_file.sheet_names
    
    # Filter out the sheet that matches the excluded name
    sheets_to_load = [sheet for sheet in all_sheets if sheet != 'main']
    
    # Create an empty list to hold individual DataFrames
    dataframes = []
    
    # Load each remaining sheet into a DataFrame and append to the list
    for sheet in sheets_to_load:
        df = pd.read_excel(excel_file, sheet_name=sheet)
        dataframes.append(df)
    
    # Concatenate all DataFrames into a single DataFrame
    combined_df = pd.concat(dataframes, ignore_index=True)

    combined_df['key_pair'] = combined_df.apply(lambda row: f"{row['Company Code']}_{row['Short Description']}", axis=1)

    
    return combined_df




def load_cash_activity(cashsheet_filename):
    dataframes = []

    xls = pd.ExcelFile(fr'C:\Users\matthewray\OneDrive - Clearwater\Desktop\Ladder\Python\input_cash_sheet\{cashsheet_filename}.xlsx')


    for sheet in xls.sheet_names:
        if 'Cash Activity' in sheet:
            df = pd.read_excel(xls, sheet_name=sheet, skiprows=3)
            df['Source_Sheet'] = sheet

            dataframes.append(df)


    combined_df = pd.concat(dataframes, ignore_index=True)

    combined_df.dropna(subset=['Short Description'], inplace=True)
    combined_df = combined_df[combined_df['Source_Sheet'] != 'Cash Activity MM-DD']

    combined_df['key_pair'] = combined_df.apply(lambda row: f"{row['Entity']}_{row['Short Description']}", axis=1)

    combined_df.rename(columns = {'Acct #': 'Acct_#'}, inplace= True)

    combined_df = combined_df[combined_df['Acct_#'] != 8147891123]

    return combined_df



def load_tran_detail(tran_detail_filename):
    df = pd.read_csv(fr'C:\Users\matthewray\OneDrive - Clearwater\Desktop\Ladder\Python\GL_Entries\inputs\CW_Tran_Detail\{tran_detail_filename}.csv')
    return df
