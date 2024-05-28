import secrets
from flask import Flask,flash, Response, redirect, render_template, request, session, url_for,send_file
from flask_mysqldb import MySQL, MySQLdb
from fpdf import FPDF
from flask_mail import Mail,Message
import random
import string
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin
from datetime import datetime,timedelta


app= Flask(__name__,template_folder='template')

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='sena_parking'
app.config['MYSQL_CURSORCLASS']='DictCursor'

mysql=MySQL(app)

#------------proteccion de rutas -------------------
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


def estatus_404 (error):
    return "<h1>pagina no encontrada</h1>",404


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/adminusu')
def admin():
    return render_template('/usuarios/inicio.html')

@app.route('/Registrar')
def registrar():
    return render_template('/Admin/eleccion/Registrar/Registrar.html')



@app.route('/adminAd')
def AdminAd():
    return render_template('/Admin/eleccion/listas/admin.html')

@app.route('/ReportElecionEstad')
def ReportElecionEstad():
    return render_template('ReportEleccionEstado.html')

@app.route('/eleccion')
def eleccionAd():
    return render_template('/Admin/eleccion/eleccion.html')

#-----------usuario view-------------------------------->
@app.route('/eleccionUsuario')
def eleccionUsu():
    return render_template('/usuarios/eleccionUsu/inicio.html')

@app.route('/RegistrarUsuario')
def registrarUsu():
    return render_template('/usuarios/eleccionUsu/RegistrarUsu/registrarUs.html')    

@app.route('/ListasUsuarios')
def ListasUsuarios():
    return render_template('/usuarios/eleccionUsu/ListaUsu/listaUsu.html')

@app.route('/RegistroVisitanteUsu')
def registroVisitanteUsu():
    return render_template('/usuarios/eleccionUsu/RegistrarUsu/registroVisitantes.html')

@app.route('/RegistroVehiculoUsu')
def RegistroVehiculoUsu():
    return render_template('/usuarios/eleccionUsu/RegistrarUsu/registroVehiculo.html')

@app.route('/RegistroestadovisitanteUsu')
def RegistroestadovisitanteUsu():
    return render_template('/usuarios/registroestadovisitante.html')

@app.route('/RegistroArtefactosExternosUsu')
def RegistroArtefactosExternosUsu():
    return render_template('/usuarios/eleccionUsu/RegistrarUsu/RegistroartefactosExternos.html')

@app.route('/RegistroEstadoVisiUsu')
def registroEstadoVisitanteUsu():
    return render_template('/usuarios/eleccionUsu/RegistrarUsu/RegistroEstadoVisitanteUsu.html')

#CrudUsuarios--------------->
@app.route('/listaArtefactoUsu')
def listaArtefactoUsu():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM artefactosexternos")
    myresult = cursor.fetchall()
    cursor.close()
    return render_template('/usuarios/eleccionUsu/ListaUsu/listaArtefactosExterno.html',data = myresult)

@app.route('/listaVisitanteUsu')
def listaVisitanteUsu():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM visitante")
    myresult = cursor.fetchall()
    cursor.close()
    return render_template('/usuarios/eleccionUsu/ListaUsu/listaVisitantes.html',data = myresult)


@app.route('/listaVehiculoUsu')
def listaVehiculoUsu():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM vehiculo")
    myresult = cursor.fetchall()
    cursor.close()
    return render_template('/usuarios/eleccionUsu/ListaUsu/listaVehiculo.html',data = myresult)

@app.route('/listaEstadovisitanteUsu')
def listaEstadovisitanteUsu():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT EV.fechaEstado, EV.horaEstado, EV.tipoEstado, V.nombresVisitante, V.numDocVisitante, VE.placaVehiculo FROM EstadoVisitante EV INNER JOIN Visitante V ON EV.idVisitanteFk = V.idVisitantePk INNER JOIN Vehiculo VE ON V.idVisitantePk = VE.idVisitanteFk;")
    myresult = cursor.fetchall()
    cursor.close()
    return render_template('/usuarios/eleccionUsu/ListaUsu/listaEstadovisitante.html',data = myresult)

#------log out--------------------->
def Logout():
    return render_template('/')




#Administrador----------------------------------------------------------------------------------------------------------------->

#Crud Usuarios -------------------------------------------------------------------------->

@app.route('/ListaUsuarios')
def listaUsuarios():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM usuario")
    myresult = cursor.fetchall()
    cursor.close()
    return render_template('Admin/eleccion/Listas/listaUsuarios.html', data = myresult)

@app.route('/delete/<string:idUsuarioPk>')
def delete (idUsuarioPk):
    cursor = mysql.connection.cursor()
    data = (idUsuarioPk ,)
    sql = "DELETE FROM usuario WHERE idUsuarioPk =%s"
    cursor.execute(sql, data)
    mysql.connection.commit()
    return redirect(url_for('listaUsuarios'))


@app.route('/edit/<string:idUsuarioPk>', methods=['POST'])
def edit(idUsuarioPk):
    correoUsuario = request.form['correoUsuario']
    passwordUsuario = request.form['passwordUsuario']

    if idUsuarioPk:
        cursor = mysql.connection.cursor()
        data = (correoUsuario,passwordUsuario,idUsuarioPk)
        sql = "UPDATE usuario SET correoUsuario = %s, passwordUsuario =%s WHERE idUsuarioPk = %s "
        cursor.execute(sql, data)
        mysql.connection.commit()
    return redirect(url_for('listaUsuarios'))

def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

@app.route('/RegistroUsuario', methods=['GET', 'POST'])
def Registro_Usuario():    
    if request.method == 'POST':
        nombres = request.form['nombres']
        Apellidos = request.form['apellidos']
        correoElectronico = request.form['correoElectronico']
        numeroDocumento = request.form['numDoc']
        password = generate_password(8)
        
        if nombres and correoElectronico and password and Apellidos and numeroDocumento:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM usuario WHERE correoUsuario = %s", (correoElectronico,))
            user = cursor.fetchone()
            if user:
                flash('El usuario ya está registrado', 'error')
            else:
                sql = "INSERT INTO usuario (nombresUsuario, apellidosUsuario, numDocUsuario, correoUsuario, passwordUsuario, idRolfk) VALUES (%s,%s,%s,%s,%s,2)"
                data = (nombres, Apellidos, numeroDocumento, correoElectronico, password)
                cursor.execute(sql, data)
                mysql.connection.commit()
                send_email(correoElectronico, password)

    return render_template("admin/eleccion/registrar/registroUsuarios.html")


#Crud Visitantes ----------------------------------------------->

@app.route('/ListaVisitantes')
def listaVisitantes():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM visitante")
    myresult = cursor.fetchall()
    cursor.close()
    return render_template('Admin/eleccion/Listas/listaVisitantes.html', data = myresult)



@app.route('/editVisitante/<string:idVisitantePk>', methods=['POST'])
def editVisitante(idVisitantePk):
    tipoVisitante = request.form['tipoVisitante']
    

    if idVisitantePk:
        cursor = mysql.connection.cursor()
        data = (tipoVisitante,idVisitantePk)
        sql = "UPDATE visitante SET tipoVisitante=%s WHERE idVisitantePk = %s "
        cursor.execute(sql, data)
        mysql.connection.commit()
        
    return redirect(url_for('listaVisitantes'))

@app.route('/RegistroVisitante', methods=['GET', 'POST'])
def Registro_Visitantes():
    if request.method == 'POST':
        nombresVisitante = request.form['nombresVisitante']
        apellidosVisitante = request.form['apellidosVisitante']
        numDocVisitante = request.form['numDocVisitante']
        tipoVisitante = request.form['tipoVisitante']

        if nombresVisitante  and apellidosVisitante and numDocVisitante and tipoVisitante:
            cursor = mysql.connection.cursor()
            sql = "INSERT INTO visitante (nombresVisitante, apellidosVisitante, numDocVisitante, tipoVisitante) VALUES (%s,%s,%s,%s)"
            data = (nombresVisitante,apellidosVisitante, numDocVisitante, tipoVisitante)
            cursor.execute(sql, data)
            mysql.connection.commit()
    
    return render_template("admin/eleccion/registrar/registroVisitantes.html")


#Crud Vehiculo ----------------------------------------------->
@app.route('/ListaVehiculo')
def listaVehiculo():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM vehiculo")
    myresult = cursor.fetchall()
    cursor.close()
    return render_template('Admin/eleccion/Listas/listaVehiculo.html', data = myresult)

@app.route('/deleteVehiculo/<string:idVehiculo>')
def deleteVehiculo (idVehiculo):
    cursor = mysql.connection.cursor()
    data = (idVehiculo,)
    sql = "DELETE FROM vehiculo WHERE idVehiculo =%s"
    cursor.execute(sql, data)
    mysql.connection.commit()
    return redirect(url_for('listaVehiculo'))

@app.route('/editVehiculo/<string:idVehiculo>', methods=['POST'])
def editVehiculo(idVehiculo):
    placaVehiculo = request.form['placaVehiculo']
    tipoVehiculo = request.form['tipoVehiculo']

    if idVehiculo:
        cursor = mysql.connection.cursor()
        data = (idVehiculo,placaVehiculo,tipoVehiculo)
        sql = "UPDATE vehiculo SET placaVehiculo=%s, tipoVehiculo = %s WHERE idVehiculo = %s "
        cursor.execute(sql, data)
        mysql.connection.commit()
        
    return redirect(url_for('listaVehiculo'))

@app.route('/RegistroVehiculo', methods=['GET', 'POST'])
def Registro_Vehiculo():
    if request.method == 'POST':
        placaVehiculo = request.form['placaVehiculo']
        tipoVehiculo = request.form['tipoVehiculo']

        if placaVehiculo and tipoVehiculo:
            cursor = mysql.connection.cursor()
            sql = "INSERT INTO vehiculo (placaVehiculo, tipoVehiculo, idVisitantefk) VALUES (%s,%s,1)"
            data = (placaVehiculo, tipoVehiculo)
            cursor.execute(sql, data)
            mysql.connection.commit()
    
    return render_template("admin/eleccion/registrar/registroVehiculo.html")


#Crud Estadovisitante----------------------------------->
@app.route('/listaEstadovisitante')
def listaEstadovisitante():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM estadovisitante")
    myresult = cursor.fetchall()
    cursor.close()
    return render_template('Admin/eleccion/Listas/listaEstadovisitante.html', data = myresult)

@app.route('/RegistroEstadovisitante', methods=['GET', 'POST'])
def Registro_Estado_Visitante():
    if request.method == 'POST':
        fechaEstado = request.form['fechaEstado']
        horaEstado = request.form['horaEstado']
        tipoEstado = request.form['tipoEstado']
        
        

        if fechaEstado  and horaEstado and tipoEstado:
            cursor = mysql.connection.cursor()
            sql = "INSERT INTO estadovisitante (fechaEstado,horaEstado,tipoEstado,idVisitanteFk) VALUES (%s,%s,%s,1)"
            data = (tipoEstado,horaEstado,tipoEstado)
            cursor.execute(sql, data)
            mysql.connection.commit()
    return render_template("Admin/eleccion/Registrar/RegistroEstadovisitante.html")

#Crud Artefactos-Externos----------------------------------->

@app.route('/ListaArtefactosExternos')
def ListaArtefactosExternos():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM artefactosexternos")
    myresult = cursor.fetchall()
    cursor.close()
    return render_template('Admin/eleccion/Listas/ListaArtefactosExternos.html', data = myresult)

@app.route('/deleteArtefactoExterno/<string:IdArtefactoPk>')
def deleteArtefactoExterno (IdArtefactoPk):
    cursor = mysql.connection.cursor()
    data = (IdArtefactoPk)
    sql = "DELETE FROM artefactosexternos WHERE IdArtefactoPk  =%s"
    cursor.execute(sql, data)
    mysql.connection.commit()
    return redirect(url_for('ListaArtefactosExternos'))

@app.route('/editArtefactosExternos/<string:IdArtefactoPk>', methods=['POST'])
def editArtefactosExternos(IdArtefactoPk):
    nombre_artefacto = request.form['nombreArtefacto']
    descripcion_artefacto = request.form['DescripcionArtefacto']

    if IdArtefactoPk:
        cursor = mysql.connection.cursor()
        data = (nombre_artefacto,descripcion_artefacto,IdArtefactoPk)
        sql = "UPDATE artefactosexternos SET nombreArtefacto=%s, descripcionArtefacto= %s WHERE IdArtefactoPk = %s "
        cursor.execute(sql, data)
        mysql.connection.commit()
        
    return redirect(url_for('ListaArtefactosExternos'))

@app.route('/RegistroArtefactoExterno', methods=['GET', 'POST'])
def Registro_ArtefactoExterno():
    if request.method == 'POST':
        nombre_artefacto = request.form['nombreArtefactosExternos']
        descripcion_artefacto = request.form['descripcionArtefactosExternos']

        if nombre_artefacto  and descripcion_artefacto:
            cursor = mysql.connection.cursor()
            sql = "INSERT INTO artefactosexternos (nombreArtefacto,descripcionArtefacto,idVisitantefk) VALUES (%s,%s,1)"
            data = (nombre_artefacto,descripcion_artefacto)
            cursor.execute(sql, data)
            mysql.connection.commit()
    return render_template("admin/eleccion/Registrar/registroArtefactoExterno.html")



#funcion de login-------------------------------------------->

@app.route('/acceso-login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        _correo = request.form.get('txtCorreo')
        _password = request.form.get('txtPassword')


        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuario WHERE correoUsuario = %s AND passwordUsuario = %s', (_correo, _password,))
        account = cur.fetchone()

        if account:
            session['logeado'] = True
            session['idUsuarioPk'] = account['idUsuarioPk']
            session['idRolfk'] = account['idRolfk']
            if session['idRolfk'] == 1:
                return render_template("/Admin/eleccion/eleccion.html")
            elif session['idRolfk'] == 2:
                return render_template("/usuarios/eleccionUsu/inicio.html")
        else:
            error_login = 'Correo electrónico o contraseña incorrectos.'
            return render_template("index.html", error_login=error_login)

    return render_template('index.html')

#----------------------recuperation password-------------->
@app.route('/RecuperarContra', methods=["GET", "POST"])
def recuperarContra():
    if request.method == 'POST':
        _correoR = request.form.get('txtCorreorecu')
        passwordR = generate_password(8)

        cur = mysql.connection.cursor()
        cur.execute('UPDATE usuario SET passwordUsuario = %s WHERE correoUsuario = %s', (passwordR, _correoR))
        send_email_recover(_correoR,passwordR)


    return render_template('recuperarContra.html')


#---------------------------------------------------------------------Reportess---------------------------------
@app.route('/reporteUsuarios')
def generar_reporte_usuarios():

    pdf = FPDF()
    pdf.add_page()


    pdf.set_font("Arial", size=8)


    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM usuario")
    resultados = cursor.fetchall()
    
    pdf.set_font("Arial", size=18, style='B') 
    pdf.cell(0, 10, "Reporte Usuarios", border=0, align='C') 
    pdf.ln(20)
    
    pdf.set_font("Arial", size=12, style='B') 
    
    pdf.cell(50, 10, "ID", border=1) 
    pdf.cell(50, 10, "Nombres", border=1) 
    pdf.cell(50, 10, "Apellidos", border=1) 
    pdf.cell(50, 10, "Num Doc", border=1) 
    pdf.cell(50, 10, "Correo", border=1) 
    pdf.cell(50, 10, "Contraseña", border=1) 
    pdf.ln()

    pdf.set_font("Arial", size=9) 
    
    for resultado in resultados:
        
        pdf.cell(50, 10, str(resultado['idUsuarioPk']), border=1)
        pdf.cell(50, 10, str(resultado['nombresUsuario']), border=1)
        pdf.cell(50, 10, str(resultado['apellidosUsuario']), border=1)
        pdf.cell(50, 10, str(resultado['numDocUsuario']), border=1)
        pdf.cell(50, 10, str(resultado['correoUsuario']), border=1)
        pdf.cell(50, 10, str(resultado['passwordUsuario']), border=1)
        pdf.ln()

    pdf_file_path = "reporte.pdf"
    pdf.output(pdf_file_path)
    
    
    print(f"El reporte ha sido guardado en: {pdf_file_path}")


    return send_file('reporte.pdf', as_attachment=True)


@app.route('/reporteArtefacto')
def generar_reporte_artefactos():

    pdf = FPDF()
    pdf.add_page()


    pdf.set_font("Arial", size=9)


    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM artefactosexternos")
    resultados = cursor.fetchall()
    
    pdf.set_font("Arial", size=18, style='B') 
    pdf.cell(0, 10, "Reporte artefactos externos", border=0, align='C') 
    pdf.ln(20)
    
    pdf.set_font("Arial", size=12, style='B') 
    
    pdf.cell(50, 10, "IdArtefactoPk", border=1) 
    pdf.cell(50, 10, "nombreArtefactosExternos", border=1) 
    pdf.cell(50, 10, "descripcionArtefactosExternos", border=1) 
    pdf.ln()

    pdf.set_font("Arial", size=9) 
    
    for resultado in resultados:
        
        pdf.cell(50, 10, str(resultado['IdArtefactoPk']), border=1)
        pdf.cell(50, 10, str(resultado['nombreArtefactosExternos']), border=1)
        pdf.cell(50, 10, str(resultado['descripcionArtefactosExternos']), border=1)
        pdf.ln()

    pdf_file_path = "reporte artefactos.pdf"
    pdf.output(pdf_file_path)
    
    
    print(f"El reporte ha sido guardado en: {pdf_file_path}")


    return send_file('reporte artefactos.pdf', as_attachment=True)


@app.route('/reporteEntrada')
def generar_reporte_Entrada():

    pdf = FPDF()
    pdf.add_page()


    pdf.set_font("Arial", size=9)


    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM estadovisitante")
    resultados = cursor.fetchall()
    
    pdf.set_font("Arial", size=18, style='B') 
    pdf.cell(0, 10, "Reporte Entrada de vehiculos", border=0, align='C') 
    pdf.ln(20)
    
    pdf.set_font("Arial", size=12, style='B') 
    
    pdf.cell(50, 10, "idEstadoPk ", border=1) 
    pdf.cell(50, 10, "placaVehiculo", border=1) 
    pdf.cell(50, 10, "tipoVehiculo", border=1) 
    pdf.cell(50, 10, "fechaEntrada", border=1) 
    
    pdf.ln()

    pdf.set_font("Arial", size=9) 
    
    for resultado in resultados:
        
        pdf.cell(50, 10, str(resultado['idEstadoPk']), border=1)
        pdf.cell(50, 10, str(resultado['placa']), border=1)
        pdf.cell(50, 10, str(resultado['horaEntrada']), border=1)
        pdf.cell(50, 10, str(resultado['fechaEntrada']), border=1)
        pdf.ln()

    pdf_file_path = "reporte Entrada.pdf"
    pdf.output(pdf_file_path)
    
    
    print(f"El reporte ha sido guardado en: {pdf_file_path}")


    return send_file('reporte Entrada.pdf', as_attachment=True)

@app.route('/reporteVehiculo')
def generar_reporte_Vehiculo():

    pdf = FPDF()
    pdf.add_page()


    pdf.set_font("Arial", size=9)


    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM vehiculo")
    resultados = cursor.fetchall()
    
    pdf.set_font("Arial", size=18, style='B') 
    pdf.cell(0, 10, "Reporte de vehiculos", border=0, align='C') 
    pdf.ln(20)
    
    pdf.set_font("Arial", size=12, style='B') 
    
    pdf.cell(50, 10, "idVehiculo", border=1) 
    pdf.cell(50, 10, "placaVehiculo", border=1) 
    pdf.cell(50, 10, "tipoVehiculo", border=1) 
    pdf.cell(50, 10, "idVisitantefk  ", border=1) 
    
    pdf.ln()

    pdf.set_font("Arial", size=9) 
    
    for resultado in resultados:
        
        pdf.cell(50, 10, str(resultado['idVehiculo']), border=1)
        pdf.cell(50, 10, str(resultado['placaVehiculo']), border=1)
        pdf.cell(50, 10, str(resultado['tipoVehiculo']), border=1)
        pdf.cell(50, 10, str(resultado['idVisitantefk']), border=1)
        pdf.ln()

    pdf_file_path = "reporte vehiculo.pdf"
    pdf.output(pdf_file_path)
    
    
    print(f"El reporte ha sido guardado en: {pdf_file_path}")


    return send_file('reporte vehiculo.pdf', as_attachment=True)


@app.route('/reporteVisitante')
def generar_reporte_Visitante():

    pdf = FPDF()
    pdf.add_page()


    pdf.set_font("Arial", size=9)


    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM visitante")
    resultados = cursor.fetchall()
    
    pdf.set_font("Arial", size=18, style='B') 
    pdf.cell(0, 10, "Reporte de visitantes", border=0, align='C') 
    pdf.ln(20)
    
    pdf.set_font("Arial", size=12, style='B') 
    
    pdf.cell(50, 10, "idVisitantePk   ", border=1) 
    pdf.cell(50, 10, "nombresVisitante", border=1) 
    pdf.cell(50, 10, "apellidosVisitante", border=1) 
    pdf.cell(50, 10, "cedula ", border=1) 
    pdf.ln()

    pdf.set_font("Arial", size=9) 
    
    for resultado in resultados:
        
        pdf.cell(50, 10, str(resultado['idVisitantePk']), border=1)
        pdf.cell(50, 10, str(resultado['nombresVisitante']), border=1)
        pdf.cell(50, 10, str(resultado['apellidosVisitante']), border=1)
        pdf.cell(50, 10, str(resultado['numDocVisitante']), border=1)
        pdf.ln()

    pdf_file_path = "reporte visitantes.pdf"
    pdf.output(pdf_file_path)
    
    
    print(f"El reporte ha sido guardado en: {pdf_file_path}")


    return send_file('reporte visitantes.pdf', as_attachment=True)

#-------------------------------correo enviar--------------------------

app.config['MAIL_SERVER'] = "smtp.googlemail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "parkingsenawaza@gmail.com"
app.config['MAIL_PASSWORD'] = "bksj oyhc cnjj tjza"
mail = Mail(app)



#---------Recuperation Password--------------------------------->
def send_email_recover(_correoR,passwordR):
    msg_title = "Contraseña Nueva"
    sender = app.config['MAIL_USERNAME']
    msg = Message(msg_title, sender=sender, recipients=[_correoR])
    msg.body = ""
    msg.html = render_template("recuperarContrase.html",correoRecibR = _correoR,ContraRe=passwordR) 

    try:
        mail.send(msg)
        return "Email sent..."
    except Exception as e:
        print(e)
        return f"the email was not sent {e}"
    

#------------correoRegistro---------------->
def send_email(correoElectronico,password):
    msg_title = "Bienvenido a nuestro sitio web"
    sender = app.config['MAIL_USERNAME']
    msg = Message(msg_title, sender=sender, recipients=[correoElectronico])
    msg_body = f"Gracias por registrarte en nuestro sitio web. Tu contraseña es: {password}"
    msg.body = ""
    msg.html = render_template("email.html",correoRecib = correoElectronico,Contraseña=password) 

    try:
        mail.send(msg)
        return "Email sent..."
    except Exception as e:
        print(e)
        return f"the email was not sent {e}"
    

@app.route('/reportPer')
def reportVisNOW():
    fecha_actual = datetime.now()
    fecha_actual_str = fecha_actual.strftime('%Y-%m-%d')
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT Visitante.nombresVisitante, Visitante.apellidosVisitante, EstadoVisitante.fechaEstado, EstadoVisitante.horaEstado, EstadoVisitante.tipoEstado, Vehiculo.placaVehiculo FROM Visitante JOIN EstadoVisitante ON Visitante.idVisitantePk = EstadoVisitante.idVisitanteFk JOIN Vehiculo ON Visitante.idVisitantePk = Vehiculo.idVisitanteFk WHERE EstadoVisitante.fechaEstado = %s ORDER BY EstadoVisitante.fechaEstado DESC;',[fecha_actual_str,])
    resultados= cursor.fetchall()
    cursor.close()
    # Crear un objeto FPDF
    # Crear un objeto FPDF
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()

    # Añadir título al reporte
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Reporte de Visitantes", 0, ln=True, align='C')


    pdf.set_font("Arial", size=12, style='B') 
    
    pdf.cell(50, 10, "nombresVisitante", border=1) 
    pdf.cell(50, 10, "apellidosVisitante", border=1) 
    pdf.cell(50, 10, "fechaEstado", border=1) 
    pdf.cell(50, 10, "horaEstado", border=1) 
    pdf.cell(50, 10, "tipoEstado", border=1) 
    pdf.cell(50, 10, "placaVehiculo", border=1) 
    pdf.ln()


    
    # Agregar datos al reporte
    for resultados in resultados:
        pdf.cell(50, 10, str(resultados['nombresVisitante']), border=1)
        pdf.cell(50, 10, str(resultados['apellidosVisitante']), border=1)
        pdf.cell(50, 10, str(resultados['fechaEstado']), border=1)
        pdf.cell(50, 10, str(resultados['horaEstado']), border=1)
        pdf.cell(50, 10, str(resultados['tipoEstado']), border=1)
        pdf.cell(50, 10, str(resultados['placaVehiculo']), border=1)
        pdf.ln()
    
    pdf_file_path = "report Visitant.pdf"
    pdf.output(pdf_file_path)
    
    
    print(f"El reporte ha sido guardado en: {pdf_file_path}")


    return send_file('report Visitant.pdf', as_attachment=True)

#Reportes Todos los meses----------------------------------------------->
#Report Enero
@app.route('/reportMhontEne')
def reportVisMonhtEne():
    fecha_actual = datetime.now()
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT  Visitante.nombresVisitante, Visitante.apellidosVisitante, EstadoVisitante.fechaEstado, EstadoVisitante.horaEstado, EstadoVisitante.tipoEstado, Vehiculo.placaVehiculo FROM Visitante JOIN EstadoVisitante ON Visitante.idVisitantePk = EstadoVisitante.idVisitanteFk JOIN Vehiculo ON Visitante.idVisitantePk = Vehiculo.idVisitanteFk WHERE MONTH(EstadoVisitante.fechaEstado) = 1 ORDER BY EstadoVisitante.fechaEstado DESC;')
    resultados= cursor.fetchall()
    cursor.close()
    # Crear un objeto FPDF
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()

    # Añadir título al reporte
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Reporte de Visitantes", 0, ln=True, align='C')


    pdf.set_font("Arial", size=12, style='B') 
    
    pdf.cell(50, 10, "nombresVisitante", border=1) 
    pdf.cell(50, 10, "apellidosVisitante", border=1) 
    pdf.cell(50, 10, "fechaEstado", border=1) 
    pdf.cell(50, 10, "horaEstado", border=1) 
    pdf.cell(50, 10, "tipoEstado", border=1) 
    pdf.cell(50, 10, "placaVehiculo", border=1) 
    pdf.ln()


    
    # Agregar datos al reporte
    for resultados in resultados:
        pdf.cell(50, 10, str(resultados['nombresVisitante']), border=1)
        pdf.cell(50, 10, str(resultados['apellidosVisitante']), border=1)
        pdf.cell(50, 10, str(resultados['fechaEstado']), border=1)
        pdf.cell(50, 10, str(resultados['horaEstado']), border=1)
        pdf.cell(50, 10, str(resultados['tipoEstado']), border=1)
        pdf.cell(50, 10, str(resultados['placaVehiculo']), border=1)
        pdf.ln()
    
    pdf_file_path = "report Visitant.pdf"
    pdf.output(pdf_file_path)
    
    
    print(f"El reporte ha sido guardado en: {pdf_file_path}")


    return send_file('report Visitant.pdf', as_attachment=True)

#report febrero
@app.route('/reportMhontFeb')
def reportVisMonhtFeb():
    fecha_actual = datetime.now()
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT  Visitante.nombresVisitante, Visitante.apellidosVisitante, EstadoVisitante.fechaEstado, EstadoVisitante.horaEstado, EstadoVisitante.tipoEstado, Vehiculo.placaVehiculo FROM Visitante JOIN EstadoVisitante ON Visitante.idVisitantePk = EstadoVisitante.idVisitanteFk JOIN Vehiculo ON Visitante.idVisitantePk = Vehiculo.idVisitanteFk WHERE MONTH(EstadoVisitante.fechaEstado) = 2 ORDER BY EstadoVisitante.fechaEstado DESC;')
    resultados= cursor.fetchall()
    cursor.close()
    # Crear un objeto FPDF
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()

    # Añadir título al reporte
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Reporte de Visitantes", 0, ln=True, align='C')


    pdf.set_font("Arial", size=12, style='B') 
    
    pdf.cell(50, 10, "nombresVisitante", border=1) 
    pdf.cell(50, 10, "apellidosVisitante", border=1) 
    pdf.cell(50, 10, "fechaEstado", border=1) 
    pdf.cell(50, 10, "horaEstado", border=1) 
    pdf.cell(50, 10, "tipoEstado", border=1) 
    pdf.cell(50, 10, "placaVehiculo", border=1) 
    pdf.ln()


    
    # Agregar datos al reporte
    for resultados in resultados:
        pdf.cell(50, 10, str(resultados['nombresVisitante']), border=1)
        pdf.cell(50, 10, str(resultados['apellidosVisitante']), border=1)
        pdf.cell(50, 10, str(resultados['fechaEstado']), border=1)
        pdf.cell(50, 10, str(resultados['horaEstado']), border=1)
        pdf.cell(50, 10, str(resultados['tipoEstado']), border=1)
        pdf.cell(50, 10, str(resultados['placaVehiculo']), border=1)
        pdf.ln()
    
    pdf_file_path = "report Visitant.pdf"
    pdf.output(pdf_file_path)
    
    
    print(f"El reporte ha sido guardado en: {pdf_file_path}")


    return send_file('report Visitant.pdf', as_attachment=True)
#report marzo
@app.route('/reportMhontMar')
def reportVisMonhtMar():
    fecha_actual = datetime.now()
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT  Visitante.nombresVisitante, Visitante.apellidosVisitante, EstadoVisitante.fechaEstado, EstadoVisitante.horaEstado, EstadoVisitante.tipoEstado, Vehiculo.placaVehiculo FROM Visitante JOIN EstadoVisitante ON Visitante.idVisitantePk = EstadoVisitante.idVisitanteFk JOIN Vehiculo ON Visitante.idVisitantePk = Vehiculo.idVisitanteFk WHERE MONTH(EstadoVisitante.fechaEstado) = 3 ORDER BY EstadoVisitante.fechaEstado DESC;')
    resultados= cursor.fetchall()
    cursor.close()
    # Crear un objeto FPDF
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()

    # Añadir título al reporte
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Reporte de Visitantes", 0, ln=True, align='C')


    pdf.set_font("Arial", size=12, style='B') 
    
    pdf.cell(50, 10, "nombresVisitante", border=1) 
    pdf.cell(50, 10, "apellidosVisitante", border=1) 
    pdf.cell(50, 10, "fechaEstado", border=1) 
    pdf.cell(50, 10, "horaEstado", border=1) 
    pdf.cell(50, 10, "tipoEstado", border=1) 
    pdf.cell(50, 10, "placaVehiculo", border=1) 
    pdf.ln()


    
    # Agregar datos al reporte
    for resultados in resultados:
        pdf.cell(50, 10, str(resultados['nombresVisitante']), border=1)
        pdf.cell(50, 10, str(resultados['apellidosVisitante']), border=1)
        pdf.cell(50, 10, str(resultados['fechaEstado']), border=1)
        pdf.cell(50, 10, str(resultados['horaEstado']), border=1)
        pdf.cell(50, 10, str(resultados['tipoEstado']), border=1)
        pdf.cell(50, 10, str(resultados['placaVehiculo']), border=1)
        pdf.ln()
    
    pdf_file_path = "report Visitant.pdf"
    pdf.output(pdf_file_path)
    
    
    print(f"El reporte ha sido guardado en: {pdf_file_path}")


    return send_file('report Visitant.pdf', as_attachment=True)
#report Abril
@app.route('/reportMhontAbr')
def reportVisMonhtAbr():
    fecha_actual = datetime.now()
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT  Visitante.nombresVisitante, Visitante.apellidosVisitante, EstadoVisitante.fechaEstado, EstadoVisitante.horaEstado, EstadoVisitante.tipoEstado, Vehiculo.placaVehiculo FROM Visitante JOIN EstadoVisitante ON Visitante.idVisitantePk = EstadoVisitante.idVisitanteFk JOIN Vehiculo ON Visitante.idVisitantePk = Vehiculo.idVisitanteFk WHERE MONTH(EstadoVisitante.fechaEstado) = 4 ORDER BY EstadoVisitante.fechaEstado DESC;')
    resultados= cursor.fetchall()
    cursor.close()
    # Crear un objeto FPDF
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()

    # Añadir título al reporte
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Reporte de Visitantes", 0, ln=True, align='C')


    pdf.set_font("Arial", size=12, style='B') 
    
    pdf.cell(50, 10, "nombresVisitante", border=1) 
    pdf.cell(50, 10, "apellidosVisitante", border=1) 
    pdf.cell(50, 10, "fechaEstado", border=1) 
    pdf.cell(50, 10, "horaEstado", border=1) 
    pdf.cell(50, 10, "tipoEstado", border=1) 
    pdf.cell(50, 10, "placaVehiculo", border=1) 
    pdf.ln()


    
    # Agregar datos al reporte
    for resultados in resultados:
        pdf.cell(50, 10, str(resultados['nombresVisitante']), border=1)
        pdf.cell(50, 10, str(resultados['apellidosVisitante']), border=1)
        pdf.cell(50, 10, str(resultados['fechaEstado']), border=1)
        pdf.cell(50, 10, str(resultados['horaEstado']), border=1)
        pdf.cell(50, 10, str(resultados['tipoEstado']), border=1)
        pdf.cell(50, 10, str(resultados['placaVehiculo']), border=1)
        pdf.ln()
    
    pdf_file_path = "report Visitant.pdf"
    pdf.output(pdf_file_path)
    
    
    print(f"El reporte ha sido guardado en: {pdf_file_path}")


    return send_file('report Visitant.pdf', as_attachment=True)
#report mayo
@app.route('/reportMhonMay')
def reportVisMonhtMay():
    fecha_actual = datetime.now()
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT  Visitante.nombresVisitante, Visitante.apellidosVisitante, EstadoVisitante.fechaEstado, EstadoVisitante.horaEstado, EstadoVisitante.tipoEstado, Vehiculo.placaVehiculo FROM Visitante JOIN EstadoVisitante ON Visitante.idVisitantePk = EstadoVisitante.idVisitanteFk JOIN Vehiculo ON Visitante.idVisitantePk = Vehiculo.idVisitanteFk WHERE MONTH(EstadoVisitante.fechaEstado) = 5 ORDER BY EstadoVisitante.fechaEstado DESC;')
    resultados= cursor.fetchall()
    cursor.close()
    # Crear un objeto FPDF
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()

    # Añadir título al reporte
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Reporte de Visitantes", 0, ln=True, align='C')


    pdf.set_font("Arial", size=12, style='B') 
    
    pdf.cell(50, 10, "nombresVisitante", border=1) 
    pdf.cell(50, 10, "apellidosVisitante", border=1) 
    pdf.cell(50, 10, "fechaEstado", border=1) 
    pdf.cell(50, 10, "horaEstado", border=1) 
    pdf.cell(50, 10, "tipoEstado", border=1) 
    pdf.cell(50, 10, "placaVehiculo", border=1) 
    pdf.ln()


    
    # Agregar datos al reporte
    for resultados in resultados:
        pdf.cell(50, 10, str(resultados['nombresVisitante']), border=1)
        pdf.cell(50, 10, str(resultados['apellidosVisitante']), border=1)
        pdf.cell(50, 10, str(resultados['fechaEstado']), border=1)
        pdf.cell(50, 10, str(resultados['horaEstado']), border=1)
        pdf.cell(50, 10, str(resultados['tipoEstado']), border=1)
        pdf.cell(50, 10, str(resultados['placaVehiculo']), border=1)
        pdf.ln()
    
    pdf_file_path = "report Visitant.pdf"
    pdf.output(pdf_file_path)
    
    
    print(f"El reporte ha sido guardado en: {pdf_file_path}")


    return send_file('report Visitant.pdf', as_attachment=True)
#report junio
@app.route('/reportMhonJun')
def reportVisMonhtJun():
    fecha_actual = datetime.now()
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT  Visitante.nombresVisitante, Visitante.apellidosVisitante, EstadoVisitante.fechaEstado, EstadoVisitante.horaEstado, EstadoVisitante.tipoEstado, Vehiculo.placaVehiculo FROM Visitante JOIN EstadoVisitante ON Visitante.idVisitantePk = EstadoVisitante.idVisitanteFk JOIN Vehiculo ON Visitante.idVisitantePk = Vehiculo.idVisitanteFk WHERE MONTH(EstadoVisitante.fechaEstado) = 6 ORDER BY EstadoVisitante.fechaEstado DESC;')
    resultados= cursor.fetchall()
    cursor.close()
    # Crear un objeto FPDF
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()

    # Añadir título al reporte
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Reporte de Visitantes", 0, ln=True, align='C')


    pdf.set_font("Arial", size=12, style='B') 
    
    pdf.cell(50, 10, "nombresVisitante", border=1) 
    pdf.cell(50, 10, "apellidosVisitante", border=1) 
    pdf.cell(50, 10, "fechaEstado", border=1) 
    pdf.cell(50, 10, "horaEstado", border=1) 
    pdf.cell(50, 10, "tipoEstado", border=1) 
    pdf.cell(50, 10, "placaVehiculo", border=1) 
    pdf.ln()


    
    # Agregar datos al reporte
    for resultados in resultados:
        pdf.cell(50, 10, str(resultados['nombresVisitante']), border=1)
        pdf.cell(50, 10, str(resultados['apellidosVisitante']), border=1)
        pdf.cell(50, 10, str(resultados['fechaEstado']), border=1)
        pdf.cell(50, 10, str(resultados['horaEstado']), border=1)
        pdf.cell(50, 10, str(resultados['tipoEstado']), border=1)
        pdf.cell(50, 10, str(resultados['placaVehiculo']), border=1)
        pdf.ln()
    
    pdf_file_path = "report Visitant.pdf"
    pdf.output(pdf_file_path)
    
    
    print(f"El reporte ha sido guardado en: {pdf_file_path}")


    return send_file('report Visitant.pdf', as_attachment=True)
#report julio
@app.route('/reportMhonJul')
def reportVisMonhtJul():
    fecha_actual = datetime.now()
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT  Visitante.nombresVisitante, Visitante.apellidosVisitante, EstadoVisitante.fechaEstado, EstadoVisitante.horaEstado, EstadoVisitante.tipoEstado, Vehiculo.placaVehiculo FROM Visitante JOIN EstadoVisitante ON Visitante.idVisitantePk = EstadoVisitante.idVisitanteFk JOIN Vehiculo ON Visitante.idVisitantePk = Vehiculo.idVisitanteFk WHERE MONTH(EstadoVisitante.fechaEstado) = 7 ORDER BY EstadoVisitante.fechaEstado DESC;')
    resultados= cursor.fetchall()
    cursor.close()
    # Crear un objeto FPDF
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()

    # Añadir título al reporte
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Reporte de Visitantes", 0, ln=True, align='C')


    pdf.set_font("Arial", size=12, style='B') 
    
    pdf.cell(50, 10, "nombresVisitante", border=1) 
    pdf.cell(50, 10, "apellidosVisitante", border=1) 
    pdf.cell(50, 10, "fechaEstado", border=1) 
    pdf.cell(50, 10, "horaEstado", border=1) 
    pdf.cell(50, 10, "tipoEstado", border=1) 
    pdf.cell(50, 10, "placaVehiculo", border=1) 
    pdf.ln()


    
    # Agregar datos al reporte
    for resultados in resultados:
        pdf.cell(50, 10, str(resultados['nombresVisitante']), border=1)
        pdf.cell(50, 10, str(resultados['apellidosVisitante']), border=1)
        pdf.cell(50, 10, str(resultados['fechaEstado']), border=1)
        pdf.cell(50, 10, str(resultados['horaEstado']), border=1)
        pdf.cell(50, 10, str(resultados['tipoEstado']), border=1)
        pdf.cell(50, 10, str(resultados['placaVehiculo']), border=1)
        pdf.ln()
    
    pdf_file_path = "report Visitant.pdf"
    pdf.output(pdf_file_path)
    
    
    print(f"El reporte ha sido guardado en: {pdf_file_path}")


    return send_file('report Visitant.pdf', as_attachment=True)
#report agosto
@app.route('/reportMhonAgo')
def reportVisMonhtAgo():
    fecha_actual = datetime.now()
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT  Visitante.nombresVisitante, Visitante.apellidosVisitante, EstadoVisitante.fechaEstado, EstadoVisitante.horaEstado, EstadoVisitante.tipoEstado, Vehiculo.placaVehiculo FROM Visitante JOIN EstadoVisitante ON Visitante.idVisitantePk = EstadoVisitante.idVisitanteFk JOIN Vehiculo ON Visitante.idVisitantePk = Vehiculo.idVisitanteFk WHERE MONTH(EstadoVisitante.fechaEstado) = 8 ORDER BY EstadoVisitante.fechaEstado DESC;')
    resultados= cursor.fetchall()
    cursor.close()
    # Crear un objeto FPDF
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()

    # Añadir título al reporte
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Reporte de Visitantes", 0, ln=True, align='C')


    pdf.set_font("Arial", size=12, style='B') 
    
    pdf.cell(50, 10, "nombresVisitante", border=1) 
    pdf.cell(50, 10, "apellidosVisitante", border=1) 
    pdf.cell(50, 10, "fechaEstado", border=1) 
    pdf.cell(50, 10, "horaEstado", border=1) 
    pdf.cell(50, 10, "tipoEstado", border=1) 
    pdf.cell(50, 10, "placaVehiculo", border=1) 
    pdf.ln()


    
    # Agregar datos al reporte
    for resultados in resultados:
        pdf.cell(50, 10, str(resultados['nombresVisitante']), border=1)
        pdf.cell(50, 10, str(resultados['apellidosVisitante']), border=1)
        pdf.cell(50, 10, str(resultados['fechaEstado']), border=1)
        pdf.cell(50, 10, str(resultados['horaEstado']), border=1)
        pdf.cell(50, 10, str(resultados['tipoEstado']), border=1)
        pdf.cell(50, 10, str(resultados['placaVehiculo']), border=1)
        pdf.ln()
    
    pdf_file_path = "report Visitant.pdf"
    pdf.output(pdf_file_path)
    
    
    print(f"El reporte ha sido guardado en: {pdf_file_path}")


    return send_file('report Visitant.pdf', as_attachment=True)
#report septiembre
@app.route('/reportMhonSep')
def reportVisMonhtSep():
    fecha_actual = datetime.now()
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT  Visitante.nombresVisitante, Visitante.apellidosVisitante, EstadoVisitante.fechaEstado, EstadoVisitante.horaEstado, EstadoVisitante.tipoEstado, Vehiculo.placaVehiculo FROM Visitante JOIN EstadoVisitante ON Visitante.idVisitantePk = EstadoVisitante.idVisitanteFk JOIN Vehiculo ON Visitante.idVisitantePk = Vehiculo.idVisitanteFk WHERE MONTH(EstadoVisitante.fechaEstado) = 9 ORDER BY EstadoVisitante.fechaEstado DESC;')
    resultados= cursor.fetchall()
    cursor.close()
    # Crear un objeto FPDF
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()

    # Añadir título al reporte
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Reporte de Visitantes", 0, ln=True, align='C')


    pdf.set_font("Arial", size=12, style='B') 
    
    pdf.cell(50, 10, "nombresVisitante", border=1) 
    pdf.cell(50, 10, "apellidosVisitante", border=1) 
    pdf.cell(50, 10, "fechaEstado", border=1) 
    pdf.cell(50, 10, "horaEstado", border=1) 
    pdf.cell(50, 10, "tipoEstado", border=1) 
    pdf.cell(50, 10, "placaVehiculo", border=1) 
    pdf.ln()


    
    # Agregar datos al reporte
    for resultados in resultados:
        pdf.cell(50, 10, str(resultados['nombresVisitante']), border=1)
        pdf.cell(50, 10, str(resultados['apellidosVisitante']), border=1)
        pdf.cell(50, 10, str(resultados['fechaEstado']), border=1)
        pdf.cell(50, 10, str(resultados['horaEstado']), border=1)
        pdf.cell(50, 10, str(resultados['tipoEstado']), border=1)
        pdf.cell(50, 10, str(resultados['placaVehiculo']), border=1)
        pdf.ln()
    
    pdf_file_path = "report Visitant.pdf"
    pdf.output(pdf_file_path)
    
    
    print(f"El reporte ha sido guardado en: {pdf_file_path}")


    return send_file('report Visitant.pdf', as_attachment=True)
#report octubre
@app.route('/reportMhonOct')
def reportVisMonhtOct():
    fecha_actual = datetime.now()
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT  Visitante.nombresVisitante, Visitante.apellidosVisitante, EstadoVisitante.fechaEstado, EstadoVisitante.horaEstado, EstadoVisitante.tipoEstado, Vehiculo.placaVehiculo FROM Visitante JOIN EstadoVisitante ON Visitante.idVisitantePk = EstadoVisitante.idVisitanteFk JOIN Vehiculo ON Visitante.idVisitantePk = Vehiculo.idVisitanteFk WHERE MONTH(EstadoVisitante.fechaEstado) = 10 ORDER BY EstadoVisitante.fechaEstado DESC;')
    resultados= cursor.fetchall()
    cursor.close()
    # Crear un objeto FPDF
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()

    # Añadir título al reporte
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Reporte de Visitantes", 0, ln=True, align='C')


    pdf.set_font("Arial", size=12, style='B') 
    
    pdf.cell(50, 10, "nombresVisitante", border=1) 
    pdf.cell(50, 10, "apellidosVisitante", border=1) 
    pdf.cell(50, 10, "fechaEstado", border=1) 
    pdf.cell(50, 10, "horaEstado", border=1) 
    pdf.cell(50, 10, "tipoEstado", border=1) 
    pdf.cell(50, 10, "placaVehiculo", border=1) 
    pdf.ln()


    
    # Agregar datos al reporte
    for resultados in resultados:
        pdf.cell(50, 10, str(resultados['nombresVisitante']), border=1)
        pdf.cell(50, 10, str(resultados['apellidosVisitante']), border=1)
        pdf.cell(50, 10, str(resultados['fechaEstado']), border=1)
        pdf.cell(50, 10, str(resultados['horaEstado']), border=1)
        pdf.cell(50, 10, str(resultados['tipoEstado']), border=1)
        pdf.cell(50, 10, str(resultados['placaVehiculo']), border=1)
        pdf.ln()
    
    pdf_file_path = "report Visitant.pdf"
    pdf.output(pdf_file_path)
    
    
    print(f"El reporte ha sido guardado en: {pdf_file_path}")


    return send_file('report Visitant.pdf', as_attachment=True)
#report Noviembre
@app.route('/reportMhontNov')
def reportVisMonhtNov():
    fecha_actual = datetime.now()
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT  Visitante.nombresVisitante, Visitante.apellidosVisitante, EstadoVisitante.fechaEstado, EstadoVisitante.horaEstado, EstadoVisitante.tipoEstado, Vehiculo.placaVehiculo FROM Visitante JOIN EstadoVisitante ON Visitante.idVisitantePk = EstadoVisitante.idVisitanteFk JOIN Vehiculo ON Visitante.idVisitantePk = Vehiculo.idVisitanteFk WHERE MONTH(EstadoVisitante.fechaEstado) = 11 ORDER BY EstadoVisitante.fechaEstado DESC;')
    resultados= cursor.fetchall()
    cursor.close()
    # Crear un objeto FPDF
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()

    # Añadir título al reporte
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Reporte de Visitantes", 0, ln=True, align='C')


    pdf.set_font("Arial", size=12, style='B') 
    
    pdf.cell(50, 10, "nombresVisitante", border=1) 
    pdf.cell(50, 10, "apellidosVisitante", border=1) 
    pdf.cell(50, 10, "fechaEstado", border=1) 
    pdf.cell(50, 10, "horaEstado", border=1) 
    pdf.cell(50, 10, "tipoEstado", border=1) 
    pdf.cell(50, 10, "placaVehiculo", border=1) 
    pdf.ln()


    
    # Agregar datos al reporte
    for resultados in resultados:
        pdf.cell(50, 10, str(resultados['nombresVisitante']), border=1)
        pdf.cell(50, 10, str(resultados['apellidosVisitante']), border=1)
        pdf.cell(50, 10, str(resultados['fechaEstado']), border=1)
        pdf.cell(50, 10, str(resultados['horaEstado']), border=1)
        pdf.cell(50, 10, str(resultados['tipoEstado']), border=1)
        pdf.cell(50, 10, str(resultados['placaVehiculo']), border=1)
        pdf.ln()
    
    pdf_file_path = "report Visitant.pdf"
    pdf.output(pdf_file_path)
    
    
    print(f"El reporte ha sido guardado en: {pdf_file_path}")


    return send_file('report Visitant.pdf', as_attachment=True)

#report Diciembre
@app.route('/reportMhontDic')
def reportVisMonhtDic():
    fecha_actual = datetime.now()
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT  Visitante.nombresVisitante, Visitante.apellidosVisitante, EstadoVisitante.fechaEstado, EstadoVisitante.horaEstado, EstadoVisitante.tipoEstado, Vehiculo.placaVehiculo FROM Visitante JOIN EstadoVisitante ON Visitante.idVisitantePk = EstadoVisitante.idVisitanteFk JOIN Vehiculo ON Visitante.idVisitantePk = Vehiculo.idVisitanteFk WHERE MONTH(EstadoVisitante.fechaEstado) = 12 ORDER BY EstadoVisitante.fechaEstado DESC;')
    resultados= cursor.fetchall()
    cursor.close()
    # Crear un objeto FPDF
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()

    # Añadir título al reporte
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Reporte de Visitantes", 0, ln=True, align='C')


    pdf.set_font("Arial", size=12, style='B') 
    
    pdf.cell(50, 10, "nombresVisitante", border=1) 
    pdf.cell(50, 10, "apellidosVisitante", border=1) 
    pdf.cell(50, 10, "fechaEstado", border=1) 
    pdf.cell(50, 10, "horaEstado", border=1) 
    pdf.cell(50, 10, "tipoEstado", border=1) 
    pdf.cell(50, 10, "placaVehiculo", border=1) 
    pdf.ln()


    
    # Agregar datos al reporte
    for resultados in resultados:
        pdf.cell(50, 10, str(resultados['nombresVisitante']), border=1)
        pdf.cell(50, 10, str(resultados['apellidosVisitante']), border=1)
        pdf.cell(50, 10, str(resultados['fechaEstado']), border=1)
        pdf.cell(50, 10, str(resultados['horaEstado']), border=1)
        pdf.cell(50, 10, str(resultados['tipoEstado']), border=1)
        pdf.cell(50, 10, str(resultados['placaVehiculo']), border=1)
        pdf.ln()
    
    pdf_file_path = "report Visitant.pdf"
    pdf.output(pdf_file_path)
    
    
    print(f"El reporte ha sido guardado en: {pdf_file_path}")


    return send_file('report Visitant.pdf', as_attachment=True)


#Fin report visit ------------------------------------------------------------------------------------------------------------------>


@app.route('/ListaVisitantes')
def listaVisitantes():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM visitante")
    myresult = cursor.fetchall()
    cursor.close()
    return render_template('index.html', data = myresult)


@app.route('/reporteVisitante')
def generar_reporte_Visitant():

    pdf = FPDF()
    pdf.add_page()


    pdf.set_font("Arial", size=9)


    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM visitante")
    resultadoss = cursor.fetchall()
    
    pdf.set_font("Arial", size=18, style='B') 
    pdf.cell(0, 10, "Reporte de visitantes", border=0, align='C') 
    pdf.ln(20)
    
    pdf.set_font("Arial", size=12, style='B') 
    
    pdf.cell(50, 10, "idVisitantePk", border=1) 
    pdf.cell(50, 10, "nombresVisitante", border=1) 
    pdf.cell(50, 10, "apellidosVisitante", border=1) 
    pdf.cell(50, 10, "numDocVisitante", border=1) 
    pdf.cell(50, 10, "tipoVisitante", border=1) 
    pdf.ln()

    pdf.set_font("Arial", size=9) 
    
    for resultadoss in resultadoss:
        
        pdf.cell(50, 10, str(resultadoss['idVisitantePk']), border=1)
        pdf.cell(50, 10, str(resultadoss['nombresVisitante']), border=1)
        pdf.cell(50, 10, str(resultadoss['apellidosVisitante']), border=1)
        pdf.cell(50, 10, str(resultadoss['numDocVisitante']), border=1)
        pdf.cell(50, 10, str(resultadoss['tipoVisitante']), border=1)
        pdf.ln()

    pdf_file_path = "reporte visitantes.pdf"
    pdf.output(pdf_file_path)
    
    
    print(f"El reporte ha sido guardado en: {pdf_file_path}")


    return send_file('reporte visitantes.pdf', as_attachment=True)

if __name__ == '__main__':
    app.secret_key="contraseñamela"
    app.run(debug=True, host='0.0.0.0',port=5000,threaded=True)