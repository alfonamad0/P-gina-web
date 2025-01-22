# Importamos las herramientas necesarias
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

# Inicializamos la aplicación Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instagram_clone.db'  # Esta es la base de datos
app.config['SECRET_KEY'] = 'mysecretkey'  # Para la seguridad de las sesiones
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Donde vamos a guardar las fotos que suban
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  # Tipos de imágenes permitidos

db = SQLAlchemy(app)  # Inicializamos la base de datos

# Creamos la base de datos
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)  # No estamos encriptando la contraseña en este caso
    posts = db.relationship('Post', backref='author', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_filename = db.Column(db.String(120), nullable=False)
    caption = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Página principal (feed)
@app.route('/')
def index():
    posts = Post.query.all()  # Obtenemos todos los posts
    return render_template('index.html', posts=posts)

# Página de perfil de usuario
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Si no estás logueado, te mandamos a la página de login
    
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        file = request.files['image']  # Subir una imagen
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)  # Aseguramos que el nombre del archivo sea seguro
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # Guardamos la imagen
            
            caption = request.form['caption']  # El texto que escriba el usuario sobre la imagen
            new_post = Post(image_filename=filename, caption=caption, user_id=user.id)
            db.session.add(new_post)
            db.session.commit()

            flash('Post created successfully!', 'success')  # Mostramos un mensaje de éxito
            return redirect(url_for('profile'))
    
    posts = Post.query.filter_by(user_id=session['user_id']).all()
    return render_template('profile.html', user=user, posts=posts)

# Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()  # Buscamos si el usuario existe
        if user and user.password == password:
            session['user_id'] = user.id  # Guardamos el ID del usuario en la sesión
            return redirect(url_for('profile'))  # Si todo está bien, vamos a su perfil
        
        flash('Invalid username or password!', 'danger')  # Si algo está mal, mostramos un error

    return render_template('login.html')

# Verificar si el archivo tiene una extensión permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

if __name__ == '__main__':
    app.run(debug=True)  # Ejecutamos la app en modo de depuración
