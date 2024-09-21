import nfl_data_py as nfl

import pandas as pd



def scrape_weekly_data(csv_name, current_year):

    print("Current Year:", current_year)

    current_year_int = int(current_year)

    weekly_data = nfl.import_weekly_data(years=range(current_year_int - 1, current_year_int))

    num_columns = weekly_data.shape[1]
    num_rows = weekly_data.shape[0]

    weekly_data.to_csv(csv_name, index=False)

    print('saved to csv. Num cols = ', num_columns, "\n")
    print('and Num Rows = ', num_rows)


