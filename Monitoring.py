import pandas as pd

initial_data = {
    'date': 0,
    'inv_mr_1': 0,
    'inv_mr_2': 0,
    'inv_mr_3': 0,
    'backorder_mr': 0,
    'inv_ws': 0,
    'backorder_ws': 0
}
# Create DataFrame to monitor Supply Chain data.
sc_data = pd.DataFrame(initial_data)


def append_data(**kwargs):
    new_data = initial_data
    for key, value in kwargs.items():
        new_data.update({key, value})
    for key, value in new_data:
        if value == 0:
            # Obtain values of last row.
            new_data.update({key, sc_data.key.iat[-1]})
    sc_data.append(other=new_data)
