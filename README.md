# Prueba_tecnica_Globant

El proposito de este proyecto es resolver el reto: Globant’s Data Engineering Coding Challenge

Este reto consiste en 2 secciones:

1. Crear un API REST local que cargue data en una BD desde un CSV a 3 tablas (departments, jobs, employees).
2. Realizar 2 consultas SQL a la BD cargada anteriormente y generar un end-point para cada consulta.

## Funcionalidades

- Cargar arhivos CSV mediante POST requests hacia una base de datos en SQLite.
- Obtener resultados (data) mediante GET requests que engatillan consultas SQL en la base de datos.

## Prerequisitos

- Flask
- SQLAlchemy
- pandas

## Instalación

1. Clona el repositorio:
    ```bash
    git clone https://github.com/alejandrozenam/Prueba_tecnica_Globant.git
    ```
2. Ir el directorio del proyecto y ejecutar:
    ```bash
    pip install -r requirements.txt
    ```

## Uso
1. Ejecute la aplicación:
    ```bash
    python app.py
    ```

2. Cargue un archivo CSV mediante una solicitud POST a `/upload_csv`:
 - Ejemplo usando Postman:
    - URL: `http://localhost:5000/upload_csv`
    - Método: `POST`
    - Body (form-data):
        - `file`: [archivo CSV]
        - `table`: [Nombre de la tabla en la base de datos]

3. Obtener datos de cualquier tabla mediante una solicitud GET a `/select_table/<table_name>`:
 - Ejemplo usando Postman:
    - URL: `http://localhost:5000/select_table/jobs`
    - Método: `GET`

4. Obtener datos de la primera consulta SQL mediante una solicitud GET a `/Question2_NumberEmployees`:
 - Ejemplo usando Postman:
    - URL: `http://localhost:5000/Question2_NumberEmployees`
    - Método: `GET`
    - Scripts:  ```
    var template = `
        <table style="width:100%" border=1>
            <tr bgcolor="#50b9f2">
                <th>department</th>
                <th>job</th>
                <th>Q1</th>
                <th>Q2</th>
                <th>Q3</th>
                <th>Q4</th>
                <th>TOTAL_2021</th>
            </tr>
            {{#each response}}
                <tr>
                    <td>{{department}}</td>
                    <td>{{job}}</td>
                    <td>{{Q1}}</td>
                    <td>{{Q2}}</td>
                    <td>{{Q3}}</td>
                    <td>{{Q4}}</td>
                    <td>{{TOTAL_2021}}</td>
                </tr>
            {{/each}}
        </table>
    `;
    pm.visualizer.set(template, {
        response: pm.response.json()
    });
    ```

5. Obtener datos de la primera consulta SQL mediante una solicitud GET a `/Question3_Department_NumberEmployees`:
 - Ejemplo usando Postman:
    - URL: `http://localhost:5000/Question3_Department_NumberEmployees`
    - Método: `GET`
    - Scripts:  ```
    var template = `
        <table style="width:100%" border=1>
            <tr bgcolor="#50b9f2">
                <th>id</th>
                <th>department</th>
                <th>CANTIDAD</th>
            </tr>
            {{#each response}}
                <tr>
                    <td>{{id}}</td>
                    <td>{{department}}</td>
                    <td>{{CANTIDAD}}</td>
                </tr>
            {{/each}}
        </table>
    `;
    pm.visualizer.set(template, {
        response: pm.response.json()
    });
    ```
## Estructura del proyecto
- Carpeta app
    - `app.py`: archivo de aplicación.
    - `models.py`: Modelos SQLAlchemy para las tablas.
    - `config.py`: Archivo de configuración para la conexión a la base de datos y parametros.
- Carpeta docs: Archivos csv y capturas de pantallas
- `requirements.txt`: Lista de dependencias.
