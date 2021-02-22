from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# initializations
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'PRUEBA_DESARROLLO'
mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"

# routes
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("""
                	
                    SELECT 	
                            TM_CONSULTA.ID,
                            TM_CONSULTA.CANTIDAD_PACIENTES,
                            TM_CONSULTA.NOMBRE_ESPECIALISTA, 
                            TR_TIPO_CONSULTA.DESCRIPCION AS TIPO_CONSULTA,
                            TR_ESTADOS_CONSULTA.DESCRIPCION AS ESTADO
                    FROM TM_CONSULTA 
                            inner join TR_TIPO_CONSULTA
                        ON TR_TIPO_CONSULTA.ID = TM_CONSULTA.ID_TIPO_CONSULTA
                            INNER JOIN TR_ESTADOS_CONSULTA
                        ON TR_ESTADOS_CONSULTA.ID = TM_CONSULTA.ID_ESTADO
                                    
                """)
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', consultas = data)

""" @app.route('/', methods=['GET'])
def dropdown():
     return render_template(
        'index.html',
        data=[{'name':'red'}, {'name':'green'}, {'name':'blue'}]) """
    #cur = mysql.connection.cursor()
    #cur.execute('SELECT * FROM TR_ESTADOS_CONSULTA')
    #data = cur.fetchall()
    #cur.close()
    #return render_template('index.html', estados = data)

@app.route('/add_consulta', methods=['POST'])
def add_consulta():
    if request.method == 'POST':
        cantPacientes = request.form['CANTIDAD_PACIENTES']
        nombreEspecialista = request.form['NOMBRE_ESPECIALISTA']
        idTipoConsulta = request.form['TipoConsulta']
        idEstado = request.form['Estados']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO TM_CONSULTA (CANTIDAD_PACIENTES, NOMBRE_ESPECIALISTA, ID_TIPO_CONSULTA, ID_ESTADO) VALUES (%s,%s,%s,%s)", 
                    (cantPacientes, nombreEspecialista, idTipoConsulta, idEstado))
        mysql.connection.commit()
        flash('Consulta adicionada satisfactoriamente')
        return redirect(url_for('Index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM TM_CONSULTA WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-consulta.html', contact = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        cantPacientes = request.form['CANTIDAD_PACIENTES']
        nombreEspecialista = request.form['NOMBRE_ESPECIALISTA']
        cur = mysql.connection.cursor()
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE TM_CONSULTA
            SET CANTIDAD_PACIENTES = %s,
                NOMBRE_ESPECIALISTA = %s
            WHERE id = %s
        """, (cantPacientes, nombreEspecialista, id))
        flash('Consulta actualizada satisfactoriamente')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM TM_CONSULTA WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Consulta removida satisfactoriamente')
    return redirect(url_for('Index'))

# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)
