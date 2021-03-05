from flask import Flask
from flask import render_template, request, redirect, url_for
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'drivekopilot.com'
app.config['MYSQL_DATABASE_USER'] = 'dst_usuarioprueb'
app.config['MYSQL_DATABASE_PASSWORD'] = 'pruebas123456'
app.config['MYSQL_DATABASE_DB'] = 'dst_pruebas'
mysql.init_app(app)

@app.route('/')
def index():
    return render_template('usuarios/index.html')

@app.route('/devices')
def devices():
    
    sql_d = "SELECT * FROM `dispositivos`;"
    sql_u = "SELECT * FROM `usuarios`;"

    
    conn = mysql.connect()
    
    cursor_d = conn.cursor()
    cursor_u = conn.cursor()

    
    cursor_d.execute(sql_d)
    cursor_u.execute(sql_u)

    
    usuarios = cursor_u.fetchall()
    dispositivos = cursor_d.fetchall()

    
    conn.commit()
    
    return render_template('usuarios/devices.html', dispositivos = dispositivos, usuarios = usuarios)

@app.route('/edit/<int:id>')
def edit(id):
    
    sql_user = "SELECT nombre, id FROM `usuarios`;"
    
    connec = mysql.connect()
    
    cursor = connec.cursor()
    cursor_list = connec.cursor()
    cursor.execute("SELECT * FROM `dispositivos` WHERE id = %s", (id))
    dispositivos = cursor.fetchall()
    
    
    cursor_list.execute(sql_user)
    user_name = cursor_list.fetchall()
    
    print(user_name)

    connec.commit()
    
    return render_template('/usuarios/edit.html', dispositivos = dispositivos, user_name = user_name)


@app.route('/create')
def create():
    
    sql_user = "SELECT nombre, id FROM `usuarios`;"
    
    connec = mysql.connect()
    
    cursor_list = connec.cursor()
    cursor_list.execute(sql_user)
    user_name = cursor_list.fetchall()
    
    #print(user_name)
    connec.commit()
    
    
    return render_template('usuarios/create.html', user_name = user_name)

@app.route('/update', methods = ['POST'])
def update():
    
    _nombre = request.form['nombre']
    _version = request.form['version']
    _usuario = request.form['usuario']
    
    id = request.form['id']

    sql = "UPDATE dispositivos SET  nombre = %s, version = %s, usuario = %s WHERE id = %s ;"
    datos = (_nombre, _version, _usuario, id)
    
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    
    
    return redirect('/')



@app.route('/store', methods=['POST'])
def storage():

    _nombre = request.form['nombre']
    _version = request.form['version']
    _usuario = request.form['usuario']
    _configuracion = request.form['configuracion']
    
    sql = "INSERT INTO `dispositivos` (`id`, `nombre`, `version`, `usuario`, `configuracion`) VALUES (NULL, %s,  %s, %s, %s);"
    datos = (_nombre, _version, _usuario, _configuracion)
   
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    
    return redirect(url_for('create'))

if __name__== '__main__':
    app.run(debug=True)
