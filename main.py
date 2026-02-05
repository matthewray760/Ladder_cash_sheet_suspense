import pandas as pd
from data_intake.load_data import load_mappings, load_cash_activity, load_tran_detail
from utils.to_excel import def_init_excel, bulk_wire_tool
from bulk_helios_entry.cash_tran_checks import cash_tran_check
from bulk_helios_entry.merge_bect import merge_cashtran_blkentry, merge_y_cashtran_blkentry
from cash_wire import run_cash_wire
from utils.sql import sql_cash_tran_check
from utils.config import mapping_filename, tran_detail_filename, use_excel_for_mapping,use_sql_for_cash_tran_check
from bulk_helios_entry.bulk_helios_entry import create_helios_entry


### Parameters for initial run
cashsheet_filename = '1.2026_final'
entry_date = '2026-01-01'

to_excel = True


### Parameters for cash wire tool
run_cashwire_check = False


def run_pipeline():

    ### Load data from cash activity file and mappings file
    cashsheet = load_cash_activity(cashsheet_filename)
    mappings = load_mappings(mapping_filename)

    if use_sql_for_cash_tran_check == True:
        cash_tran_detail = sql_cash_tran_check(entry_date=entry_date)[0]
    else:
        cash_tran_detail = load_tran_detail(tran_detail_filename)


    ### Create list of mappings to short description
    modifications = mappings['Short Description'].tolist()
    filtered_cashsheet = cashsheet[cashsheet['Short Description'].str.contains('|'.join(modifications))]
    merged_df = pd.merge(filtered_cashsheet,mappings, on='key_pair')
    merged_df['Date'] = merged_df['Date'].dt.date


    ### Run Bulk Helios Entries
    bulk_cash_entry, cash_tran_df, concat_df = create_helios_entry(df=merged_df)



    ### Cash transfer checks

    tran_check = cash_tran_check(bulk_entry=bulk_cash_entry,cash_transactions=cash_tran_detail) ## merg to bulk entry and create Y/N for offsetting cash transfers in bank accounts


    ### Merge cash tran check with Bulk Entry

    final_merge_yn = merge_cashtran_blkentry(bulk_entry=bulk_cash_entry, cashtran_check = tran_check)

    final_merge_y_w_trn = merge_y_cashtran_blkentry(final_merge_yn)



    if to_excel == True:
        def_init_excel(cashsheet_filename=cashsheet_filename,tran_check=tran_check,final_merge_yn=final_merge_yn,final_merge_y_w_trn=final_merge_y_w_trn,cashsheet=cashsheet,entry_date=entry_date)
    else:
        pass



    if run_cashwire_check == True:
        df_cash_wire, bulk_df = run_cash_wire(final_merge_y=final_merge_y_w_trn,entry_date=entry_date)
        bulk_wire_tool(bulk_df=bulk_df,entry_date=entry_date,merged=df_cash_wire,filename=cashsheet_filename)

    else:
        pass




if __name__ == '__main__':
     run_pipeline()






#bulk_df.to_excel(fr'C:\Users\matthewray\OneDrive - Clearwater\Desktop\Ladder\Python\GL_Entries\outputs\tran_ids_output.xlsx')
#df_cash_wire.to_excel(fr'C:\Users\matthewray\OneDrive - Clearwater\Desktop\Ladder\Python\GL_Entries\outputs\cash_wire.xlsx')
