from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
app = Flask(__name__)
app.secret_key = 'md5'
db = sqlite3.connect('data.db', check_same_thread=False)

@app.route('/', methods =['GET', 'POST'])
def start():
    if request.method == 'GET':
        return render_template('start.html')
    
    email = request.form.get('email')
    password = request.form.get('password')
    cursor = db.cursor()
    usuario = cursor.execute(""" select * from usuarios where email = ? and password = ?""",(email,password,)).fetchone()
    if usuario is None:
        #Flash
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
    cursor = db.cursor()
    print(name,email,password)
    cursor.execute(""" insert into usuarios 
        (name,
        email,
        password)
        values (?,?,?) """,(name,email,password,))
    db.commit()
    return redirect(url_for('index'))

@app.route('/categories')
def categories():
    categories = db.execute("""select * from categorias where id_usuario = ?""",(session['usuario'][0],)).fetchall()
    print (categories)
    return render_template('login/categories.html', categories = categories)
app.run(debug=True)