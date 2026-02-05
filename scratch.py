### Create bulk cash entry
bulk_cash_entry = merged_df[['Account ID','Date','Amount', 'Transaction_Type']].copy()


bulk_cash_entry.loc[:,'Entry Date'] = bulk_cash_entry['Date']
bulk_cash_entry.loc[:,'Settle Date'] = bulk_cash_entry['Date']
bulk_cash_entry.loc[:,'Post Date'] = bulk_cash_entry['Date']
bulk_cash_entry.loc[:,'Currency'] = 'USD'
bulk_cash_entry.loc[:,'Asset ID'] = 'CCYUSD'

bulk_cash_entry = bulk_cash_entry[['Account ID','Transaction_Type', 'Entry Date', 'Settle Date', 'Post Date', 'Asset ID', 'Currency', 'Amount']]



#### creating offsetting cash transfers

cash_transfers = bulk_cash_entry.copy()
cash_transfers['Amount_1'] = cash_transfers['Amount'] * -1
cash_transfers.drop(columns='Amount', inplace= True)
cash_transfers.rename(columns={'Amount_1':'Amount'}, inplace=True)
cash_transfers['Transaction Type'] = 'TRN'




concat_df = pd.concat([bulk_cash_entry,cash_transfers])




### Create cash tran offsets with final_merge

final_merge_y = final_merge_yn.copy()
final_merge_y = final_merge_y[final_merge_y['Match'] == 'Y']

cash_transfers_2 = final_merge_y.copy()
cash_transfers_2['Amount_1'] = cash_transfers_2['Amount'] * -1
cash_transfers_2.drop(columns='Amount', inplace=True)
cash_transfers_2.rename(columns = {'Amount_1':'Amount'}, inplace=True)
cash_transfers_2['Transaction_Type'] = 'TRN'


final_merge_y_w_trn = pd.concat([final_merge_y,cash_transfers_2]) ## Goes to cash wire 