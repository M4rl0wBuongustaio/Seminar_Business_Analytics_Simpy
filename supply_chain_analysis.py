import pandas as pd

file_path = '/Users/leonbecker/PycharmProjects/Seminar_Business_Analytics_Simpy/Supply_Chain_Data_no_safety_stock.xlsx'
supply_chain_data = pd.read_excel(io=file_path, sheet_name='Sheet1')
print(supply_chain_data)
