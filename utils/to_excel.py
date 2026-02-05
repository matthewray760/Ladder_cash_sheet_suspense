import pandas as pd
import numpy as np
import openpyxl
import xlsxwriter
import os



def def_init_excel(cashsheet_filename,tran_check,final_merge_yn,final_merge_y_w_trn,cashsheet,entry_date):

    date_obj = pd.to_datetime(entry_date)

    month = date_obj.strftime('%m.%Y')

    output_dir = fr'C:\Users\matthewray\OneDrive - Clearwater\Desktop\Ladder\Python\GL_Entries\outputs\{month}'

    # Create the directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Define the complete file path for the Excel output
    pathway = fr'{output_dir}\{cashsheet_filename}.xlsx'

    writer = pd.ExcelWriter(pathway,engine= 'openpyxl', mode='w')

    final_merge_y_w_trn.to_excel(writer, sheet_name= 'Bulk_final_Y_trn', index=False)
    final_merge_yn.to_excel(writer, sheet_name= 'Bulk_final_Y_N', index=False)
    tran_check.to_excel(writer, sheet_name= 'tran_check', index=False)
    cashsheet.to_excel(writer, sheet_name= 'cash_activity_raw', index=False)


    for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            for column_cells in worksheet.columns:
                max_length = 0
                column = column_cells[0].column_letter
                for cell in column_cells:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except:
                        pass
                adjusted_width = (max_length + 6)
                worksheet.column_dimensions[column].width = adjusted_width
    print("Python: Executed successfully. Output file created")
    writer.save()


def bulk_wire_tool(bulk_df,entry_date,merged,filename):

    date_obj = pd.to_datetime(entry_date)

    month = date_obj.strftime('%m.%Y')

    pathway = fr'C:\Users\matthewray\OneDrive - Clearwater\Desktop\Ladder\Python\GL_Entries\outputs\{month}\transaction_ids_{filename}.xlsx'

    writer = pd.ExcelWriter(pathway,engine= 'openpyxl', mode='w')

    bulk_df.to_excel(writer, sheet_name= 'bulk_upload', index=False)
    merged.to_excel(writer, sheet_name= 'raw', index=False)



    for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            for column_cells in worksheet.columns:
                max_length = 0
                column = column_cells[0].column_letter
                for cell in column_cells:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except:
                        pass
                adjusted_width = (max_length + 6)
                worksheet.column_dimensions[column].width = adjusted_width
    print("Python: Executed successfully. Output file created")
    writer.save()

