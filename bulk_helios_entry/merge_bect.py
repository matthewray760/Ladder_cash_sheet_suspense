import pandas as pd



def merge_cashtran_blkentry(bulk_entry,cashtran_check):

    bulk_entry_df = bulk_entry
    cashtran_df = cashtran_check

    merged_df = bulk_entry_df.merge(
    cashtran_df[['Account ID_x', 'Post Date', 'Amount', 'Match','Transaction Id','Account ID_y']],
    left_on=['Account ID', 'Post Date', 'Amount'],
    right_on=['Account ID_x', 'Post Date', 'Amount'],
    how='left'
    )

    merged_df.drop(columns=['Account ID_x'], inplace=True)

    

    return merged_df


   
def merge_y_cashtran_blkentry(final_merge_yn):
    final_merge_y = final_merge_yn.copy()
    final_merge_y = final_merge_y[final_merge_y['Match'] == 'Y']

    cash_transfers_2 = final_merge_y.copy()
    cash_transfers_2['Amount_1'] = cash_transfers_2['Amount'] * -1
    cash_transfers_2.drop(columns='Amount', inplace=True)
    cash_transfers_2.rename(columns = {'Amount_1':'Amount'}, inplace=True)
    cash_transfers_2['Transaction_Type'] = 'TRN'


    final_merge_y_w_trn = pd.concat([final_merge_y,cash_transfers_2]) ## Goes to cash wire 

    return final_merge_y_w_trn
