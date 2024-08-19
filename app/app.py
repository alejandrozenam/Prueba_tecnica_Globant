from flask import Flask, request, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, MetaData
from models import Base
from config import engine, parameter
import pandas as pd
import sqlite3

app = Flask(__name__)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

con = sqlite3.connect('data_migration.db', check_same_thread=False)

#----------------API-----------------------------------------------------------------------------------------------------------------------------------------
@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    
    if 'file' not in request.files:
        return jsonify({'error': 'Se debe subir el archivo. (key=file)'}), 400
    
    if 'table' not in request.form:
        return jsonify({'error': 'Se debe agregar el nombre de la tabla. (key=table)'}), 400
    
    file = request.files['file']
    table = request.form['table']

    if file and file.filename.endswith('.csv'):

        if table not in parameter.table_columns:
            return jsonify({'error': 'Nombre no encontrado. Debe ser departments,jobs o employees.'}), 400
        
        columns = parameter.table_columns[table]

        df = pd.read_csv(file, header=None, names=columns)

        df.to_sql(table, engine, if_exists='append', index=False)

        return jsonify({'message': 'Archivo subido correctamente.'})
    
    return jsonify({'error': 'El formato del archivo debe ser CSV.'}), 400

#No solicitaron esta funcionalidad, pero la emplee para validar que las tablas se hayan cargado correctamente.
@app.route('/select_table/<table_name>',methods=['GET'])
def select_table(table_name):
    metadata = MetaData()
    metadata.reflect(bind=engine)

    if table_name not in metadata.tables:
        return jsonify({'error': f'Tabla {table_name} no existe.'}), 400

    table = Table(table_name, metadata, autoload_with=engine)
    
    data = session.query(table).all()

    result = []
    for row in data:
        row_dict = {column.name: getattr(row, column.name) for column in table.columns}
        result.append(row_dict)
    
    return jsonify(result)

#----------------SQL----------------------------------------------------------------------------------------------------------------------------------------
#
#Pregunta1: Number of employees hired for each job and department in 2021 divided by quarter. 
#           The table must be ordered alphabetically by department and job.


#Comentarios:
#Opte por SQLlite debido a que los problemas no eran complejos y no era necesario instalar una BD. 
#A pesar de ello, quiero comentar que en SQL hubiese empleado la función PIVOT y castear la fecha de una forma más adecuada, ya que SQLite tiene sus limitaciones.

#Por lo tanto, desarrolle el ejercicio de la siguiente forma:

@app.route('/Question2_NumberEmployees',methods=['GET'])
def Question2_NumberEmployees():

    query="""
    WITH BASE AS 
    (
    SELECT 
    IFNULL(d.department,'ND') AS department,
    IFNULL(j.job,'ND') AS job,
    'Q'||( FLOOR((CAST(STRFTIME('%m',DATE(SUBSTRING(e.datetime,1,10))) AS INTEGER) -1 )/3 ) + 1 ) AS QUARTER ,
    COUNT(e.id) AS CANTIDAD
    FROM employees e
    LEFT JOIN departments d ON e.department_id = d.id
    LEFT JOIN jobs j ON e.job_id = j.id 
    WHERE strftime('%Y', DATE(SUBSTRING(e.datetime,1,10))) ='2021'
    GROUP BY 1,2,3
    )
    SELECT 
    department,
    job,
    sum(CANTIDAD) filter (where QUARTER = 'Q1') as "Q1",
    sum(CANTIDAD) filter (where QUARTER = 'Q2') as "Q2",
    sum(CANTIDAD) filter (where QUARTER = 'Q3') as "Q3",
    sum(CANTIDAD) filter (where QUARTER = 'Q4') as "Q4",
    sum(CANTIDAD) as "TOTAL_2021"
    FROM BASE
    GROUP BY 1,2
    ORDER BY 1 ASC,2 ASC
    ;
    """
    result = pd.read_sql_query(query, con)
    result_json = result.to_json(orient='records', indent=4)
    return result_json

#Observación: Emplee como universo principal la tabla empleados, ya que busque realizar en este ejercicio un modelado dimensional (Fact: Empleados, Dimension: Departamentos, Puestos). 

#Para ver el resultado correctamente se debe usar la función Visualize en Postman con el código mencionado en Github.




#
#Pregunta2: List of ids, name and number of employees hired of each department that hired more employees than the mean of employees
#           hired in 2021 for all the departments, ordered by the number of employees hired (descending).


#Comentarios:
#En este caso, primero tuve identificar la cantidad de empleados contratados en el 2021 por cada departamento, luego calcule el promedio 
#y finalmente se realizó el filtro de los departamentos con una cantidad de empleado contratados mayor al promedio.

@app.route('/Question3_Department_NumberEmployees',methods=['GET'])
def Question3_Department_NumberEmployees():

    query="""
    WITH BASE AS 
    (
    SELECT 
    d.id,
    d.department,
    COUNT(e.id) AS CANTIDAD
    FROM departments d
    LEFT JOIN employees e ON d.id = e.department_id
    WHERE strftime('%Y', DATE(SUBSTRING(e.datetime,1,10))) ='2021'
    GROUP BY 1,2
    )
    SELECT 
    id,
    department,
    CANTIDAD
    FROM BASE
    WHERE  CANTIDAD > (SELECT AVG(CANTIDAD)
                    FROM BASE)
    ORDER BY 3 DESC
    ;
    """
    result = pd.read_sql_query(query, con)
    result_json = result.to_json(orient='records', indent=4)
    return result_json

#Para ver el resultado correctamente se debe usar la función Visualize en Postman con el código mencionado en Github.

if __name__ == '__main__':
    app.run(debug=True)