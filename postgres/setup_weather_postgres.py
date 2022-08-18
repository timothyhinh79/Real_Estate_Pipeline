import json
import psycopg2

conn = psycopg2.connect(database='weather',user = 'postgres', password = 'postgres', host = 'localhost', port = '5432')
conn.autocommit = True
cursor = conn.cursor()

cursor.execute("""
    DROP TABLE IF EXISTS daily_forecasts;
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_forecasts (
        id SERIAL PRIMARY KEY,
        city VARCHAR(255),
        date DATE,
        maxtemp_c FLOAT,
        maxtemp_f FLOAT,
        mintemp_c FLOAT,
        mintemp_f FLOAT,
        avgtemp_c FLOAT,
        avgtemp_f FLOAT,
        maxwind_mph FLOAT,
        maxwind_kph FLOAT,
        totalprecip_mm FLOAT,
        totalprecip_in FLOAT,
        avgvis_km FLOAT,
        avgvis_miles FLOAT,
        avghumidity FLOAT,
        uv FLOAT
    )
""")
