from sqlalchemy import create_engine

DB_URI = 'sqlite:///data_migration.db' 

engine = create_engine(DB_URI)

# Columnas de las tablas
class parameter:
    table_columns = {
        'departments': ['id', 'department'],
        'jobs':  ['id', 'job'],
        'employees': ['id', 'name', 'datetime', 'department_id', 'job_id'],
    }