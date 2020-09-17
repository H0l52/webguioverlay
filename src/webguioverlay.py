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
#import Queue

"""
web = QWebView()
		web.load(QtCore.QUrl("https://pythonspot.com"))
		web.show()
"""

running = True

class linkchanger(QtCore.QThread):
	
	link_change = QtCore.pyqtSignal(object)
	
	def __init__(self):
		QtCore.QThread.__init__(self)
		self.url = input("Enter new link(will not be added to file): ")
	
	def run(self):
		self.link_change.emit(str(self.url))

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
	global running
	while True:
		print('')
		commands = input('> ')
		nextcommand = commands.lower()
		print()
		if nextcommand == 'close':
			running = False
			QApplication.exit()
			quit()
		elif nextcommand == 'changelink':
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
			print('Reloading...')
			QApplication.exit()
			
		elif nextcommand == 'help':
			print('---------')
			print('changelink > changes the link of a gui element')
			print('addelement > adds an element to file and loads element')
			print('removeelement > removes an element and deletes the file')
			print('reload > reloads all elements from files') 
			print('close > quits the program')
			print('help > shows this message')
			print('---------')
		elif nextcommand == 'damn':
			print('daniel')
		else:
			print('Unknown command. Do \"help\" if you need assistance.')
if __name__ == '__main__':
	print()
	print("Running ---- Web Gui Overlay by H0l52 v 0.0.3 ----")

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
		
	
