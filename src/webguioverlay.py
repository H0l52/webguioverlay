import sys
import win32api, win32con, win32gui, win32ui
import os
from PyQt5 import QtGui, QtCore, uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView,QWebEnginePage as QWebPage
from PyQt5.QtWebEngineWidgets import QWebEngineSettings as QWebSettings
import threading
import signal
import time
from tkinter import Tk
from tkinter.filedialog import askopenfilename
#import Queue

"""
web = QWebView()
		web.load(QtCore.QUrl("https://pythonspot.com"))
		web.show()
"""

running = True

class filerunner(QtCore.QThread):
	
	file_run = QtCore.pyqtSignal(object)
	
	def __init__(self, filename):
		QtCore.QThread.__init__(self)
		self.filename = filename
	
	def run(self):
		filename = self.filename
		os.system("copy \"" + filename + "\"")
		files = filename.split('/')
		filenamer = files[-1].split(".")[0]
		self.file_run.emit([str("import {0}".format(filenamer)), filenamer])
		

class linkchanger(QtCore.QThread):
	
	link_change = QtCore.pyqtSignal(object)
	
	def __init__(self):
		QtCore.QThread.__init__(self)
		self.url = input("Enter new link(will not be added to file): ")
	
	def run(self):
		self.link_change.emit(str(self.url))

class closer(QtCore.QThread):
	
	close_change = QtCore.pyqtSignal(object)
	
	def __init__(self):
		QtCore.QThread.__init__(self)
		
	
	def run(self):
		self.close_change.emit('quit')
		
class MainWindow(QWebView):
	def __init__(self, loc, sizex, sizey):
		QMainWindow.__init__(self)
		#QWebView.__init__(self)
		self.setWindowFlags(
			QtCore.Qt.WindowStaysOnTopHint |
			QtCore.Qt.FramelessWindowHint |
			QtCore.Qt.X11BypassWindowManagerHint
		)
		self.setGeometry(
			QtWidgets.QStyle.alignedRect(
				QtCore.Qt.LeftToRight, QtCore.Qt.AlignCenter,
				#QtCore.QSize(312, 600),
				QtCore.QSize(sizex, sizey),
				QtWidgets.qApp.desktop().availableGeometry()
		))
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		#self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
		self.center(loc)
		
		
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent, False)
		page = self.page()
		page.setBackgroundColor(QtCore.Qt.transparent)
		#page.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.setStyleSheet("background:transparent;")
		#self.page().setBackgroundColor(QtCore.Qt.transparent)
		#palette = page.palette()
		#palette.setBrush(QtGui.QPalette.Base, Qt.transparent)
		#page.setPalette(palette)
		#self.setWindowOpacity(0.6)
		#hwnd = win32gui.FindWindow(None, "Demo")
		hwnd = int(self.winId())
		posX, posY, width, height = win32gui.GetWindowPlacement(hwnd)[4]
		
		windowStyles = win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
		win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, windowStyles)
		win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, posX,posY, 0,0, win32con.SWP_NOSIZE)

		windowAlpha = 180
		win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0,0,0),
		windowAlpha, win32con.LWA_ALPHA)
		self.threads = []
		"""
		layout = QVBoxLayout()
		self.setLayout(layout)
 
		# Create and fill a QWebView
		view = QWebView()
		view.load(QtCore.QUrl("http://www.www.pythoncentral.io"))
		layout.addWidget(view)
		button = QtWidgets.QPushButton('Set Full Name')
		layout.addWidget(button)
		"""
	def runfile(self, filename):
		filerholder = filerunner(filename)
		filerholder.file_run.connect(self.on_runf)
		self.threads.append(filerholder)
		filerholder.start()
	def on_runf(self, datalist):
		exec(datalist[0])
		os.system("del " + datalist[1] + ".py")
		
	def vishide(self):
		vischange = closer()
		vischange.close_change.connect(self.on_visread)
		self.threads.append(vischange)
		vischange.start()
	def on_visread(self, data):
		self.close()
	def newlink(self):
		linker = linkchanger()
		linker.link_change.connect(self.on_linkready)
		self.threads.append(linker)
		linker.start()
	def on_linkready(self, data):
		self.setUrl(QtCore.QUrl(data))
		
		
	def load(self,url):
		self.setUrl(QtCore.QUrl(url))
		
	def center(self, loc):
	
		if loc == "topleft":
			#print('topleft')
			qr = self.frameGeometry()
			cp = QDesktopWidget().availableGeometry().topLeft()
			qr.moveTopLeft(cp)
			self.move(qr.topLeft())
		if loc == "bottomleft":
			#print('bottomleft')
			qr = self.frameGeometry()
			cp = QDesktopWidget().availableGeometry().bottomLeft()
			qr.moveBottomLeft(cp)
			self.move(qr.topLeft())
		if loc == "topright":
			#print('topright')
			qr = self.frameGeometry()
			cp = QDesktopWidget().availableGeometry().topRight()
			qr.moveTopRight(cp)
			self.move(qr.topLeft())
		if loc == "bottomright":
			#print('bottomright')
			qr = self.frameGeometry()
			cp = QDesktopWidget().availableGeometry().bottomRight()
			qr.moveBottomRight(cp)
			self.move(qr.topLeft())
	
	#def mousePressEvent(self, event):
		#self.setMask(region)
		#print('hi')
		#QtWidgets.qApp.quit()
	#def mousePressEvent(self, event):
	#	QtWidgets.qApp.quit()
	#def mouseMoveEvent(self, event):
	 #   print('moved')
	  #  self.setMask(region)

	
	
def commandloop():
	time.sleep(2)
	Tk().withdraw()
	global running
	#print()
	while True:
		try:
			print()
			commands = input('> ')
			nextcommand = commands.lower()
			
			if nextcommand == 'close':
				running = False
				QApplication.exit()
				sys.exit()
			elif nextcommand == 'changelink':
				print()
				a = 1
				for file in os.listdir("./gui"):
					print(str(a) + ":" + str(file))
					a = a + 1
				chosen = input('Select file to change: ')
				print()
				dirlist = os.listdir("./gui")
				
				chose = dirlist[int(chosen)-1]
				print("Chose: " + str(chose))
				
				print()
				cs = str(chose).split(".")
				#print("global obj{0}\nobj{0}.newlink".format(cs[0]))
				exec("global obj{0}\nobj{0}.newlink()".format(cs[0]))
			elif nextcommand == 'addelement':
				print()
				position = input('Position[topleft, bottomleft, topright, bottomright]: ')
				link = input('Link: ')
				sizex = input('SizeX: ')
				sizey = input('SizeY: ')
				filename = input('WidgetName (include .txt): ')
				filewrite = open(str("./gui/" + filename), 'w')
				filewrite.write(position + "\n" + link + "\n" + sizex + "\n" + sizey)
				
				
				filewrite.close()
				
				QApplication.exit()
				#exec("global obj{0}\nobj{0} = MainWindow(flist[0], int(flist[2]), int(flist[3]))".format(fsplit[0]))
				#exec("global obj{0}\nobj{0}.show()".format(fsplit[0]))
				#exec("global obj{0}\nobj{0}.load(flist[1])".format(fsplit[0]))
				
				
			elif nextcommand == 'removeelement':
				print()
				op = input('Are you sure you want to do this? (will remove file) [Y/N]: ')
				if op.lower() == 'y':
					print()
					a = 1
					dirlist = os.listdir("./gui")
					for file in os.listdir("./gui"):
						print(str(a) + ":" + str(file))
						a = a + 1
					chosen = input('Select file to remove: ')
					
					
					os.system('cd gui')
					os.system('del ' + dirlist[int(chosen)-1])
					os.system('cd ..')
					
					print('Deleted')
					print()
					print('Reloading Elements')
					
					QApplication.exit()
			elif nextcommand == 'reload':
				print()
				print('Reloading...')
				QApplication.exit()
			elif nextcommand == 'closeelement':
				print()
				a = 1
				dirlist = os.listdir("./gui")
				for file in os.listdir("./gui"):
					print(str(a) + ":" + str(file))
					a = a + 1
				chosen = input('Select widget to close: ')
				chose = dirlist[int(chosen)-1]
				print("Chose: " + str(chose))
				
				
				cs = str(chose).split(".")
				#print("global obj{0}\nobj{0}.newlink".format(cs[0]))
				exec("global obj{0}\nobj{0}.vishide()".format(cs[0]))
			elif nextcommand == 'run':
				print()
				chosen = input('Run from thread, or from window? [T,W]: ')
				if chosen.lower() == 't':
					filename = askopenfilename(initialdir = "/",title = "Select file",filetypes = (("python files","*.py"),("all files","*.*")))
					os.system("copy \"" + filename + "\"")
					files = filename.split('/')
					filenamer = files[-1].split(".")[0]
					exec("import {0}".format(filenamer))
					os.system("del " + filenamer + ".py")
					#print(filename)
				if chosen.lower() == 'w':
					print()
					a = 1
					dirlist = os.listdir("./gui")
					for file in os.listdir("./gui"):
						print(str(a) + ":" + str(file))
						a = a + 1
					chosen = input('Select widget to run program from: ')
					chose = dirlist[int(chosen)-1]
					print("Chose: " + str(chose))
					cs = str(chose).split(".")
					filename = askopenfilename(initialdir = "/",title = "Select file",filetypes = (("python files","*.py"),("all files","*.*")))
					exec("global obj{0}\nobj{0}.runfile(filename)".format(cs[0]))
					
					#cs = str(chose).split(".")
				
			elif nextcommand == 'help':
				print()
				print('---------')
				print('changelink > changes the link of a gui element')
				print('addelement > adds an element to file and loads element')
				print('removeelement > removes an element and deletes the file')
				print('closeelement > closes an element on screen')
				print('reload > reloads all elements from files') 
				print('close > quits the program')
				print('help > shows this message')
				print('run > developer only, runs a python program from loop thread, or an element.')
				print('---------')
			elif nextcommand == 'damn':
				print()
				print('daniel')
			elif nextcommand == '':
				continue
			else:
				print('Unknown command. Do \"help\" if you need assistance.')
		except Exception as error:
			print("Error: " + str(error))
if __name__ == '__main__':
	
	print()
	print("Running ---- Web Gui Overlay by H0l52 v 0.0.4 ----")

	x = threading.Thread(target=commandloop)
	x.start()
	app = QApplication(sys.argv)
	
	while running == True:
		
		for file in os.listdir("./gui"):
			try:
				if file.endswith(".txt"):
					fileloc = './gui/' + str(file)
					f = open(fileloc, 'r')
					flist = str(f.read()).split('\n')
					fsplit = str(file).split('.')
					exec("global obj{0}\nobj{0} = MainWindow(flist[0], int(flist[2]), int(flist[3]))".format(fsplit[0]))
					exec("global obj{0}\nobj{0}.show()".format(fsplit[0]))
					exec("global obj{0}\nobj{0}.load(flist[1])".format(fsplit[0]))
					f.close()
			except:
				print('ERROR: File ' + file + " not formatted correctly.")
				
				#file = MainWindow(flist[0], int(flist[2]), int(flist[3]))
				#file.show()
		
				#file.load(flist[1])
	
	
		app.exec_()
		
	
