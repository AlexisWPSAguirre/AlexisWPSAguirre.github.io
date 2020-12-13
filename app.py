from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
app = Flask(__name__)
app.secret_key = 'md5'
db = sqlite3.connect('data.db', check_same_thread=False)

def global_cp():
    global categories
    categories = db.execute("""select * from categorias where id_usuario = ?""",(session['usuario'][0],)).fetchall()
    global products
    products = db.execute("""select * from productos where id_usuario = ?""",(session['usuario'][0],)).fetchall()

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesion cerrada Satisfactoriamente', 'success')
    return redirect(url_for('start'))

@app.route('/', methods =['GET', 'POST'])
def start():
    if request.method == 'GET':
        return render_template('start.html')
    
    email = request.form.get('email')
    password = request.form.get('password')
    cursor = db.cursor()
    global usuario 
    usuario = cursor.execute(""" select * from usuarios where email = ? and password = ?""",(email,password,)).fetchone()
    if usuario is None:
        flash('Correo Electronico y Password no coinciden','error')
        return redirect(request.url)
    session['usuario'] = usuario
    
    return redirect(url_for('index'))


@app.route('/index')
def index():
    if not 'usuario' in session:
        return redirect(url_for('start'))
    return render_template('login/index.html')

@app.route('/create', methods=['GET', 'POST'])
def create():

    if request.method == 'GET':
        return render_template('create.html')
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        cursor = db.cursor()
        cursor.execute(""" insert into usuarios 
            (name,
            email,
            password)
            values (?,?,?) """,(name,email,password,))
        db.commit()
    except:
        flash('El correo ya está registrado como Usuario','error')
        return redirect(request.url)
    flash('Usuario creado satisfactoriamente','success')
    return redirect(url_for('index'))

@app.route('/categories')
def categorie():
    if not 'usuario' in session:
        return redirect(url_for('start'))
    global_cp()
    cont = 1
    return render_template('login/categories.html', categories = categories)

@app.route('/categories/create', methods=['GET','POST'])
def create_categories():
    if not 'usuario' in session:
        return redirect(url_for('start'))
    if request.method == 'GET':
        return render_template('login/create_categories.html')
    categoria = request.form.get('categorie')
    cursor = db.cursor()
    cursor.execute("""INSERT INTO categorias(id_usuario, nombre_categoria) values (?,?)""",(session['usuario'][0],categoria,))
    db.commit()
    flash('Categoría '+categoria+' Creada Satisfactoriamente','success')
    return redirect(url_for('categorie'))

@app.route('/categories/edit/<int:id>', methods=['GET','POST'])
def edit_categories(id):
    if not 'usuario' in session:
        return redirect(url_for('start'))
    if request.method == 'GET':  
        categoria = db.execute(""" SELECT * FROM categorias WHERE id = ? """,(id,)).fetchone()
        return render_template('login/edit_categories.html', categoria = categoria)
    name = request.form.get('name')
    cursor = db.cursor()
    cursor.execute(""" UPDATE categorias SET nombre_categoria = ? WHERE id = ?""",(name,id,))
    db.commit()
    flash('Categoría '+ name +' Editado Satisfactoriamente','success')
    return redirect(url_for('categorie'))

@app.route('/categories/delete/<int:id>')
def delete_categories(id):
    global_cp() 
    if not 'usuario' in session:
        return redirect(url_for('start'))
    cursor = db.cursor()
    flash('Categoría Eliminada Satisfactoriamente','success')
    cursor.execute(""" DELETE FROM categorias WHERE id = ?""",(id,))
    db.commit()
    
    return redirect(url_for('categorie'))

@app.route('/product')
def product():
    if not 'usuario' in session:
        return redirect(url_for('start'))
    global_cp()
    return render_template('login/products.html', products = products )

@app.route('/product/create', methods = ['GET','POST'])
def create_product():
    if not 'usuario' in session:
        return redirect(url_for('start'))
    if request.method == 'GET':
        global_cp()
        return render_template('login/create_product.html', categories = categories)
    name = request.form.get('name')
    price = request.form.get('price')
    categorie = request.form.get('categorie')
    cursor = db.cursor()
    cursor.execute("""INSERT INTO productos(id_usuario,categoria,nombre,precio) VALUES (?,?,?,?)""",(session['usuario'][0],categorie,name,price,))
    db.commit()
    flash('Producto '+categorie+' Creada Satisfactoriamente','success')
    return redirect(url_for('product'))

@app.route('/product/edit/<int:id>', methods=['GET','POST'])
def edit_product(id):
    if not 'usuario' in session:
        return redirect(url_for('start'))
    if request.method == 'GET':
        global_cp()
        producto = db.execute("""SELECT * FROM productos WHERE id = ?""",(id,)).fetchone()
        return render_template('login/edit_product.html', product = producto, categories = categories)
    name = request.form.get('name')
    price = request.form.get('price')
    categorie = request.form.get('categorie')
    cursor = db.cursor()
    cursor.execute(""" UPDATE productos SET nombre = ?, precio = ?, categoria = ? WHERE id = ? """,(name,price,categorie,id))
    db.commit()
    flash('Producto '+categorie+' Editado Satisfactoriamente','sucess')
    return redirect(url_for('product'))

@app.route('/product/delete/<int:id>')
def delete_product(id):
    if not 'usuario' in session:
        return redirect(url_for('start'))
    db.execute(""" DELETE FROM productos WHERE id = ? """,(id,))
    db.commit()
    flash('Producto Eliminado Satisfactoriamente','success')
    return redirect(url_for('product'))

@app.route('/user', methods=['GET','POST'])
def user():
    if not 'usuario' in session:
        return redirect(url_for('start'))
    if request.method == 'GET':
        users = db.execute(""" SELECT * FROM  usuarios WHERE id = ?""",(session['usuario'][0],)).fetchone()
        return render_template('login/user.html', users = users)
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    cursor = db.cursor()
    cursor.execute(""" UPDATE usuarios SET name = ?,email = ?,password = ? WHERE id = ? """,(name,email,password,session['usuario'][0],))
    db.commit()
    flash('Usuario '+name+' Editado Satisfactoriamente','success')
    return redirect(url_for('index'))


app.run(debug=True)