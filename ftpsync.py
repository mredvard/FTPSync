#!/usr/bin/python
# -*- coding: utf-8 -*-

#	Nombre: FTPSync
#	Creado por: Ing. Edgar Contreras
# 	ADVERTENCIA: Ha sido solo probado en maquinas Linux, no posee compatibilidad con maquinas windows por convencion de nombres 
#	de Carpetas.
#	OJO: Ftp es lento por naturaleza para mayor velocidad usar rsync

from struct import *
from mainwindow import *
import ftputil
import threading
import os
from Queue import Queue

class vPrincipal(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.uiPrincipal = Ui_MainWindow()
		self.uiPrincipal.setupUi(self)
		
		self.status = False
		self.raiz = '/'
		self.directorios = []			# Almacena los directorios del usuario con un PATH completo
		self.archivos = []			# Almacena los archivos del usuario con PATH completo
		self.archivos_total = 0			# Total de archivos contados
		self.directorios_total = 0		# Total de directorios contados
		self.tamano_total = 0			# Tamano total a descargar expresado en bytes
		self.porcentaje = 0			# Almacena el porcentaje de descarga durante el proceso
		self.byte = 0				# Usada para debugging
		self.ftp = None				# Almacena el objeto ftputil
		self.host = ''				# Almacena el host a conectar
		
		# Declaracion de eventos
		self.connect(self.uiPrincipal.btnConectar, QtCore.SIGNAL('clicked()'), self.conectar)	#Evento de hacer click en btnConectar
		self.connect(self.uiPrincipal.btnTransferir, QtCore.SIGNAL('clicked()'), self.transferir) #Evento de hacer click en btnTransferir
		self.connect(self, QtCore.SIGNAL("actualizarBarra"), self.actualizarBarra) #Evento para actualizar la barra desde el thread
		self.connect(self, QtCore.SIGNAL("error"), self.mostrarError)	# Evento para mostrar una ventana de error desde un thread
		
	# conectar: Va ligado al evento de hacer click en btnConectar	
	def conectar(self):
		# Inicializacion de variables para la conexion FTP
		self.host = str(self.uiPrincipal.txtHost.text())
		login = str(self.uiPrincipal.txtLogin.text())
		password =  str(self.uiPrincipal.txtPassword.text())
		self.raiz = str(self.uiPrincipal.txtRaiz.text())
		if (self.raiz == ''):
			self.raiz = '/'
		
		if (self.host == ''): 
			self.mostrarError("Campo de host no puede esar vacio")
		else:
			try:
				self.uiPrincipal.statusbar.showMessage("Conectando ...")
				print "Conectando ..."
				self.ftp = ftputil.FTPHost(self.host, login, password)
				self.ftp.chdir(self.raiz)
				self.uiPrincipal.statusbar.showMessage("Conectado")
				print "Conectado"
				self.status = True
				
				# Activa los controles que estaban desactivados antes de conectar 
				self.uiPrincipal.btnTransferir.setEnabled(True)
				self.uiPrincipal.barProgreso.setEnabled(True)

			# Captar error en caso de algun problema conectando
			except OSError:					
				self.mostrarError("Error al conectar")
				print "Error al Conectar"
				self.uiPrincipal.statusbar.showMessage("Error al conectar")

	# Realiza un scan recursivo a los archivos bajo la carpeta raiz especificada por el usuario y da detalles
	# sobre tamano, cantidad de directorios y archivos

	def obtenerDatos(self, raiz):
		print "Calculando..."
		for path, directorio, archivo in self.ftp.walk(raiz):
			self.directorios.append(path)
			for nombre in archivo:
				archivo_dir = os.path.join(path, nombre)
				self.archivos.append(archivo_dir)
				self.tamano_total += self.ftp.path.getsize(archivo_dir)

		self.archivos_total = len(self.archivos)
		self.directorios_total = len(self.directorios)
		self.uiPrincipal.statusbar.showMessage("Directorios: " + repr(self.directorios_total) +\
						       " Archivos: " + repr(self.archivos_total) +\
						       " Size: " + repr(self.tamano_total/1024) + " Kbytes")
		
	# Metodo que dispara el evento de hacer click en el boton transferir
	def transferir(self):
		self.uiPrincipal.statusbar.showMessage("Calculando archivos a descargar...")
		self.obtenerDatos(self.raiz)
		texto = "Directorios: " + repr(self.directorios_total) +\
			"\nArchivos: " + repr(self.archivos_total) +\
			"\nSize: " + repr(self.tamano_total/1024) + " Kbytes\n" +\
			"Desea continuar con la descarga?"
		
		msgPregunta = QtGui.QMessageBox.question(self, 'Pregunta',\
							 texto, QtGui.QMessageBox.Ok,\
							 QtGui.QMessageBox.Cancel)
		# Ejecutar solo si el usuario hace click en OK
		# No entiendo todavia por que sale Cancel primero que OK 
		if msgPregunta ==  QtGui.QMessageBox.Ok:
			self.uiPrincipal.btnTransferir.setEnabled(False)
			
			thread = threading.Thread(target = self.descargar) 	# Llama a la funcion descargar en un nuevo thread
			thread.start()						# Arranca la descarga

	# Metodo para descargar los archivos de la carpeta raiz, debe ser llamado desde un thread
	def descargar(self):
		try:
			raiz_local = './' + self.host
			for dir_nombre in self.directorios:
				os.makedirs(raiz_local + dir_nombre)
				print "Creando " + raiz_local + dir_nombre
                except:
                        self.mostrarError("No se pudo crear el directorio local, es posible que ya exista o no tenga permiso de escritura")			
		try:
			for f_nombre in self.archivos:
				print "Descargando " + f_nombre + " S: " + repr(self.ftp.path.getsize(f_nombre))
                       		self.ftp.download(f_nombre, raiz_local + f_nombre, 'b', self.actualizarProgreso)
			print "Finalizada la descarga"
		except:
			self.emit(QtCore.SIGNAL("error"), "No se pudo completar la descarga ...")

	# Metodo para mostrar una ventana de error
	def mostrarError(self, texto):
		print texto # Para debuggin en consola
		msgBox = QtGui.QMessageBox.critical(self, "Error", texto, QtGui.QMessageBox.Ok)
	

	def actualizarProgreso(self, byte_chunk):
		
		self.byte += len(byte_chunk)
		self.porcentaje += float(len(byte_chunk) * 100) / float(self.tamano_total) # Realiza el calculo de porcentaje descargado 
		print repr(self.porcentaje) + " " + repr(self.byte) 	                   # Salidas por pantalla para debuggin
		
		# Emite la senal para disparar el evento que actualiza la barra de progreso
		self.emit(QtCore.SIGNAL("actualizarBarra"), self.porcentaje)		   
	
	# Metodo para actualizar la barra de progreso de la ventana
	def actualizarBarra(self, porcentaje):
		self.uiPrincipal.barProgreso.setValue(porcentaje)


if __name__ == "__main__":
	import sys
	app = QtGui.QApplication(sys.argv)
    	oPrincipal = vPrincipal()
	oPrincipal.show()
	sys.exit(app.exec_())

