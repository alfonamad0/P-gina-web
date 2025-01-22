import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk  # Para trabajar con imágenes

# Crear la ventana principal
root = tk.Tk()
root.title("App Estilo Instagram")
root.geometry("400x600")

# Función para manejar el inicio de sesión
def login():
    username = entry_username.get()
    password = entry_password.get()
    
    if username == "" or password == "":
        messagebox.showerror("Error", "Por favor ingresa usuario y contraseña.")
    else:
        messagebox.showinfo("Bienvenido", f"Hola, {username}!\nBienvenido a la app.")

# Función para manejar el registro
def register():
    messagebox.showinfo("Registro", "Se ha registrado con éxito.")

# Función para cargar y mostrar la imagen
def upload_image():
    file_path = filedialog.askopenfilename()  # Abrir el cuadro de diálogo para seleccionar archivo
    if file_path:
        # Abrir la imagen usando PIL
        img = Image.open(file_path)
        img = img.resize((200, 200))  # Redimensionar la imagen para que no ocupe demasiado espacio
        img = ImageTk.PhotoImage(img)
        
        # Mostrar la imagen en la etiqueta
        label_image.config(image=img)
        label_image.image = img  # Necesario para mantener la referencia de la imagen

# Crear una etiqueta (label) de bienvenida
label_welcome = tk.Label(root, text="Bienvenido a la app", font=("Arial", 20))
label_welcome.pack(pady=20)

# Crear un campo de texto para el usuario
label_username = tk.Label(root, text="Usuario:")
label_username.pack(pady=5)

entry_username = tk.Entry(root)
entry_username.pack(pady=5)

# Crear un campo de texto para la contraseña
label_password = tk.Label(root, text="Contraseña:")
label_password.pack(pady=5)

entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)

# Botón de iniciar sesión
btn_login = tk.Button(root, text="Iniciar sesión", command=login)
btn_login.pack(pady=10)

# Botón de registrarse
btn_register = tk.Button(root, text="Registrarse", command=register)
btn_register.pack(pady=10)

# Botón para subir imagen
btn_upload_image = tk.Button(root, text="Subir Imagen", command=upload_image)
btn_upload_image.pack(pady=10)

# Crear una etiqueta para mostrar la imagen
label_image = tk.Label(root)
label_image.pack(pady=20)

# Ejecutar el bucle de la aplicación
root.mainloop()