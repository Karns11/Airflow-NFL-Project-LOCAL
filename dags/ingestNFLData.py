from sqlalchemy import create_engine

import pandas as pd

def ingest_weekly_data(user, password, host, port, db, csv_name, table_name):

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()

    print("connection established")


    df = pd.read_csv(csv_name)

    max_season = df['season'].max()  
    filtered_df = df[df['season'] == max_season]  
    max_week = filtered_df['week'].max()  

    print("Max season = ", max_season)
    print("Max Week of most recent season = ", max_week)

    print("inserting data...")

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')


    df.to_sql(name=table_name, con=engine, if_exists='append')

    print("data inserted")

    engine.dispose()
