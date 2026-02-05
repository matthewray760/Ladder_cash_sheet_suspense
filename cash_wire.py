import pandas as pd
from utils.sql import cash_wire_trn
from susp_accounts import susp_accounts


def run_cash_wire(final_merge_y,entry_date):
    offsetting_cash_trans = final_merge_y[final_merge_y['Transaction_Type'] == 'TRN']
    entered_cash_trans = cash_wire_trn(entry_date=entry_date)[0] # SUSP cash transfers
    entered_cash_trans.rename(columns={'CashEntryAmount': 'Amount'}, inplace=True)

    ### Merge
    merged_df = offsetting_cash_trans.merge(
    entered_cash_trans[['AccountID', 'PostDate', 'Amount','transactionID']],
    left_on=['Account ID', 'Post Date', 'Amount'],
    right_on=['AccountID', 'PostDate', 'Amount'],
    how='left'
    )

    merged_df.rename(columns={'AccountID': 'Account ID SUSP', 'transactionID': 'Transaction Id SUSP','Account ID_y':'Account ID Bank'}, inplace = True)

    merged_df = merged_df[~merged_df['Account ID Bank'].isin(susp_accounts)]

    


    bulk_df = pd.DataFrame(columns=['Source Transaction ID', 'Destination Transaction ID', 'Amount'])

    for _, row in merged_df.iterrows():
        if row['Amount'] < 0:  # Source
            source_id = row['Transaction Id SUSP']
            dest_id = row['Transaction Id']
            amount = row['Amount']
            

            bulk_df = bulk_df.append({
                'Source Transaction ID': source_id,
                'Destination Transaction ID': dest_id,
                'Amount': amount
            }, ignore_index=True)

    for _, row in merged_df.iterrows():
        if row['Amount'] > 0:  # Source
            source_id_2 = row['Transaction Id']
            dest_id_2 = row['Transaction Id SUSP']
            amount_2 = row['Amount']
            

            bulk_df = bulk_df.append({
                'Source Transaction ID': source_id_2,
                'Destination Transaction ID': dest_id_2,
                'Amount': amount_2
            }, ignore_index=True)

    
    if bulk_df['Source Transaction ID'].notna().all():  # Check if all values are not NaN
        bulk_df['Source Transaction ID'] = bulk_df['Source Transaction ID'].astype(int)
    else:
        print("Source Transaction ID contains NaN values, conversion not performed.")


    if bulk_df['Destination Transaction ID'].notna().all():  # Check if all values are not NaN
        bulk_df['Destination Transaction ID'] = bulk_df['Destination Transaction ID'].astype(int)
    else:
        print("Source Transaction ID contains NaN values, conversion not performed.")

    bulk_df['Comma_separated'] = bulk_df.apply(
    lambda row: f"{int(row['Source Transaction ID'])}, {int(row['Destination Transaction ID'])}" 
                 if pd.notna(row['Source Transaction ID']) and pd.notna(row['Destination Transaction ID']) 
                 else None, axis=1
                )
    
    bulk_df['Notes'] = 'Per Suspense SOP'
    bulk_df[''] = ''

    bulk_df = bulk_df[['Source Transaction ID','Destination Transaction ID','Amount','','','Comma_separated','Notes']]



    return merged_df, bulk_df
