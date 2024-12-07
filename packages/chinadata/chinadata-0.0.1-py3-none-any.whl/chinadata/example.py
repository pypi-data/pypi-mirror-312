#1# pip install chinadata
from chinadata.pp import get_stock_data

df = get_stock_data(token='41aed146ecf59f5b7628bc6fcacf675104',ts_code='150018.SZ', start_date='20180101', end_date='20181029',asset='FD')
print(df)

from chinadata.qq import fetch_stock_data

df = fetch_stock_data(token='41aed146ecf59f5b7628bc6fcacf675104',api_name='stock_basic',fields='ts_code,symbol,name,area,industry,list_date',exchange='', list_status='L', )
print(df)
