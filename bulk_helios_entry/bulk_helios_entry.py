import pandas as pd


def create_helios_entry(df):
    bulk_cash_entry = df[['Account ID','Date','Amount', 'Transaction_Type']].copy()


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

    return bulk_cash_entry, cash_transfers,concat_df
