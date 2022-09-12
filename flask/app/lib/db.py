import psycopg2
from psycopg2 import sql
from flask import g, current_app, abort

def get_db():
    if "db" not in g:
        g.db = psycopg2.connect(user = current_app.config['DB_USER'],
                                password = current_app.config['DB_PASSWORD'],
                                dbname = current_app.config['DATABASE'],
                                host = current_app.config['PG_HOST']
        )
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def build_from_record(Class, record):
    if record is None: return None

    attrs = dict(zip(Class.columns, record))
    obj = Class(**attrs)
    return obj

def build_from_records(Class, records):
    return [build_from_record(Class, record) for record in records]

def get_columns_string(Class):
    return str(Class.columns)[1:-1].replace("'","")

def find_all(Class, conn):
    cursor = conn.cursor()
    sql = f"""
        SELECT {get_columns_string(Class)}
        FROM {Class.__table__}
    """
    cursor.execute(sql)
    records = cursor.fetchall()

    return build_from_records(Class, records)

def query(Class, params, conn):
    for key in params:
        if key not in Class.query_fields:
            abort(400, 'Invalid parameter defined in URL query') 
    
    where_str = 'WHERE '
    vars = []
    for field, field_type in Class.query_fields.items():
        if field in params.keys():
            if field_type==str:
                field_name = f'LOWER({field})'
            else:
                field_name = field
            if where_str != 'WHERE ': where_str += 'AND '
            where_str += f'{field_name} = %s '
            vars.append(params[field].lower())

    query = f'SELECT {get_columns_string(Class)} FROM {Class.__table__} ' + where_str
    cursor = conn.cursor()
    cursor.execute(query, vars = vars)
    records = cursor.fetchall()

    return build_from_records(Class, records)

def find_by_id(Class, id, conn):
    cursor = conn.cursor()
    sql = f"""
        SELECT {get_columns_string(Class)}
        FROM {Class.__table__}
        WHERE {Class.id_field} = %s
    """
    cursor.execute(sql, vars = (id,))
    record = cursor.fetchone()
    return build_from_record(Class, record)