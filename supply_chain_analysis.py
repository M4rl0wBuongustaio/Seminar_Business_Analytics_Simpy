import pandas as pd
import matplotlib.pyplot as plt

file_path = '/Users/leonbecker/PycharmProjects/Seminar_Business_Analytics_Simpy/Supply_Chain_Data_with_safety_stock_wholesaler.xlsx'
supply_chain_data = pd.read_excel(io=file_path, sheet_name='Sheet1')
supply_chain_data.plot(
    x='date',
    y=['backorder_ws', 'backorder_mr'],
    kind='line',
    title='Backorders WITH safety stock and initial stock for Wholesaler',
    ylabel='count backorders',
    grid=True,
    figsize=(12, 6.6667)
)

plt.show()
