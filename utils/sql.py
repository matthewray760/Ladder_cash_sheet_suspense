import pyodbc as py
import pandas as pd
import datetime
import tkinter as tk



def cash_wire_trn(entry_date):
        # Set up the database connection parameters
        server = 'PROD-SQL-RO'
        database = 'LM'
        username = 'ARBFUND\matthewray'
        password = 'Uhglbk547895207&'
        driver = '{ODBC Driver 17 for SQL Server}'
        

        # Create the connection string
        conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Trusted_Connection=yes;TrustServerCertificate=yes;MultiSubnetFailover=yes'

        # Connect to the database
        conn = py.connect(conn_str)

        # Create a cursor object to execute the SQL statements
        cursor = conn.cursor()

        cursor.execute('SET QUERY_GOVERNOR_COST_LIMIT 300')

        # Execute a SQL query
        query = f'''
        select t.isactive,t.tsmodified, t.tscreated, SM.cusip, t.username, t.origTransactionid, t.transactionID, t.AccountID, t.EntryDate,t.SettleDate,t.PostDate,t.TransactionTypeAbbreviation, t.price, t.units, t.Proceeds, t.CashEntryAmount  from transactioninfo t
        JOIN securitymaster sm ON t.securityid = sm.ID
        WHERE 1=1
            and AccountID IN (551387,551380,551386,551375,551384,551382,551397,551370,551401,551376,551394,551398,551399,551383,551395,551385,551389,551377,551378,551404,551400,551371,551381,551392,551372,551379,551388,551402,551391,551396,551393,551390,551374,551403,551373)
            --and origTransactionid IN (1420072797)
            and t.EntryDate > '{entry_date}'
            and transactiontypeabbreviation = 'TRN'
            and isactive = 1
            and username = 'matthewray'
            --and t.transactionid IN (1508509504)

        order by EntryDate DESC
        '''

        cursor.execute(query)

        # Fetch all the rows from the query result
        cursor.fetchall()
        df = pd.read_sql(query,conn)

        # Close the cursor and the connection
        cursor.close()
        conn.close()
  

        return df, print("SQL executed within the timeout period")





def sql_cash_tran_check(entry_date):
        # Set up the database connection parameters
        server = 'PROD-SQL-RO'
        database = 'LM'
        username = 'ARBFUND\matthewray'
        password = 'Uhglbk547895207&'
        driver = '{ODBC Driver 17 for SQL Server}'
        

        # Create the connection string
        conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Trusted_Connection=yes;TrustServerCertificate=yes;MultiSubnetFailover=yes'

        # Connect to the database
        conn = py.connect(conn_str)

        # Create a cursor object to execute the SQL statements
        cursor = conn.cursor()

        cursor.execute('SET QUERY_GOVERNOR_COST_LIMIT 300')

        # Execute a SQL query
        query = f'''
        select SM.cusip, t.origTransactionid [Transaction Id], t.AccountID [Account ID], t.PostDate [Post Date],t.TransactionTypeAbbreviation, t.CashEntryAmount [Amount]  from transactioninfo t
        JOIN securitymaster sm ON t.securityid = sm.ID
        WHERE 1=1
            and AccountID IN (select accountID FROM Aggregates where aggregateID = 369118)
            --and origTransactionid IN (1420072797)
            and t.EntryDate > '{entry_date}'
            and transactiontypeabbreviation = 'TRN'
            and isactive = 1
            --and username = 'matthewray'
            --and t.transactionid IN (1508509504)

        order by EntryDate DESC
        '''

        cursor.execute(query)

        # Fetch all the rows from the query result
        cursor.fetchall()
        df = pd.read_sql(query,conn)

        # Close the cursor and the connection
        cursor.close()
        conn.close()
  

        return df, print("SQL executed within the timeout period")
