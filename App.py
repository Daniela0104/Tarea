from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# MySQL Connection 
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'opticatriem'

# Clave secreta para permitir el uso de flash y sesiones
app.secret_key = 'mi_clave_secreta_segura'

mysql = MySQL(app)

# settings
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM materiaprima')
    data = cur.fetchall()
    return render_template('index.html', materiaprima = data)

@app.route('/add_materiaprima', methods=['POST'])
def add_materiaprima():
    if request.method == 'POST':
       descripcion = request.form['descripcion']
       codigo = request.form['codigo']
       costo = request.form['costo']
       cantidad = request.form['cantidad']
       compra = request.form['compra']
 
       cur = mysql.connection.cursor()
       cur.execute('INSERT INTO materiaprima(descripcion, codigo, costo, cantidad, compra)VALUES(%s, %s, %s, %s, %s)', (descripcion, codigo, costo, cantidad, compra))
       mysql.connection.commit()
       flash('Materia prima agregada satisfactoriamente')
       return redirect(url_for('index'))


# Eliminar
@app.route('/delete/<int:id>')
def delete_materiaprima(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM materiaprima WHERE id = %s', (id,))
    mysql.connection.commit()
    flash('Materia prima eliminada correctamente')
    return redirect(url_for('index'))

# Mostrar formulario de edición
@app.route('/edit/<int:id>')
def get_edit_materiaprima(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM materiaprima WHERE id = %s', (id,))
    data = cur.fetchone()
    return render_template('editmateriaprima.html', materia=data)


# Editar
@app.route('/edit/<int:id>', methods=['POST'])
def edit_materiaprima(id):
    descripcion = request.form['descripcion']
    codigo = request.form['codigo']
    costo = request.form['costo']
    cantidad = request.form['cantidad']
    compra = request.form['compra']

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE materiaprima 
        SET descripcion = %s, codigo = %s, costo = %s, cantidad = %s, compra = %s 
        WHERE id = %s
    """, (descripcion, codigo, costo, cantidad, compra, id))
    mysql.connection.commit()
    flash('Materia prima actualizada correctamente')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=3000, debug=True)


