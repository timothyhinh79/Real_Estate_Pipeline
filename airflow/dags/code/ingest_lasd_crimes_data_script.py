import json
from sqlalchemy import create_engine
import time
import pandas as pd
from datetime import date, timedelta

def ingest_crimes_data_to_postgres(input, database, user, password, host, port):

    print('database:', database)
    print('user:', user)
    print('password:', password)
    print('host:', host)
    print('port:', port)

    # basic cleaning
    lasd_crimes = pd.read_csv(input)
    lasd_crimes['INCIDENT_DATE'] = pd.to_datetime(lasd_crimes['INCIDENT_DATE'])
    lasd_crimes['INCIDENT_REPORTED_DATE'] = pd.to_datetime(lasd_crimes['INCIDENT_REPORTED_DATE'])
    lasd_crimes.drop(['REPORTING_DISTRICT','SEQ','UNIT_ID'], inplace = True, axis = 1)

    # ingesting to Postgres
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
    engine.connect()

    lasd_crimes.to_sql('crimes', con = engine, if_exists = 'append')

