import pandas as pd


class Monitoring:
    def __init__(self, data_frame, initial_data):
        self.sc_data: pd.DataFrame = data_frame
        self.initial_data = initial_data

    def get_sc_data(self):
        return self.sc_data

    def append_data(self, **kwargs):
        new_data = self.initial_data
        for args in kwargs.items():
            new_data.update({args})
        helper_dict = self.initial_data
        for key in helper_dict:
            if helper_dict[key] == 0:
                # Obtain values of last row.
                new_data.update({key: self.sc_data[key].iat[-1]})
        new_index = self.sc_data.index[-1] + 1
        append_df = pd.DataFrame(new_data, index=[new_index])
        self.sc_data = self.sc_data.append(append_df, ignore_index=True)

    def print_sc_data(self):
        print(self.sc_data)

    def save_sc_data(self):
        self.sc_data.to_excel('Supply_Chain_Data_with_safety_stock_wholesaler.xlsx')

    def get_sc_data(self):
        return self.sc_data
