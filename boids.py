
import threading
from random import randint
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QFrame, QDialog, QWidget, QLabel,QVBoxLayout, QHBoxLayout, QLineEdit, QGridLayout, QPushButton,QTextEdit,QTabWidget,QComboBox,QScrollArea,QPlainTextEdit, QSizePolicy,QCheckBox,QSpacerItem,QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QTimer, QThread
from configparser import ConfigParser
import time
from re import findall
import concurrent.futures
import numpy as np
import math as maths
#https://www.red3d.com/cwr/boids/
def calcAvePos(boidsList):
	averageFlockPosX = 0
	averageFlockPosY = 0
	for i in boidsList:
		averageFlockPosX = averageFlockPosX + i.coord.x
		averageFlockPosY = averageFlockPosY + i.coord.y
	averageFlockPosX = averageFlockPosX/len(	boidsList)
	averageFlockPosY = averageFlockPosY/len(boidsList)
	averageFlockCoord = Vector(averageFlockPosX,averageFlockPosY)
	return averageFlockCoord
	print(averageFlockPosY)
class BoidsWindow(QDialog):
	windowSizeX = 600
	windowSizeY = 600
	boidViewingDistance = 100
	numBoids = 100
	def __init__(self):
		super().__init__()
		self.averageFlockPosX = 0
		self.averageFlockPosY = 0
		self.dotImg = QPixmap('boidDot.png') # setup dot img
		self.dotImgSmall = self.dotImg.scaled(5,5, Qt.IgnoreAspectRatio) #then scale it
		self.dotLabel = QLabel(self)
		self.dotLabel.setPixmap(self.dotImgSmall)
		self.boidsList = []
		self.resize(BoidsWindow.windowSizeX,BoidsWindow.windowSizeY)
		#self.dotLabel.move(20,20)
		self.setupUpdateTimer()
		self.makeBoids()
		#print(np.arctan2(-4,4))

	def makeBoids(self):
		
		for i in range(0, BoidsWindow.numBoids):
			randX = randint(0,BoidsWindow.windowSizeX)
			randY = randint(0,BoidsWindow.windowSizeY)
			self.boidsList.append(Boid(Vector(randX,randY),self))



	def setupUpdateTimer(self):
		timer = QTimer(self)
		timer.timeout.connect(self.update)
		timer.start(100)
	def update(self):
		for i in self.boidsList:
			i.update(self.boidsList)


class Boid():
	def __init__(self,coord,parentWindow):
		self.coord = coord
		
		self.dotLabel = QLabel(parentWindow)
		self.dotLabel.setPixmap(parentWindow.dotImgSmall)
		
		self.viewableBoidsList = []
	def move(self,x,y):
		if self.coord.x > BoidsWindow.windowSizeX:
			self.coord.x = self.coord.x - 1000
		if self.coord.y > BoidsWindow.windowSizeY:
			self.coord.y = self.coord.y - 1000
		self.dotLabel.move(x,y)
	def update(self, boidsList):
		
		self.boidsList = boidsList
		self.getViewableBoids(self.boidsList)
		self.aveNeibourhoodPos = calcAvePos(self.viewableBoidsList)
		self.calcSeperation()
		self.calcAlignment()
			
		self.calcCohesion()
		self.addRand()
		self.move(self.coord.x,self.coord.y)
	def calcSeperation(self):
		aveNeibourhoodPos = calcAvePos(self.viewableBoidsList)
		angleAwayFromNeighbourhood = self.calcAngleToNeighbours() +maths.pi
		self.coord.x = self.coord.x + (1*np.cos(angleAwayFromNeighbourhood))
		self.coord.y = self.coord.y + (1*np.sin(angleAwayFromNeighbourhood))
		print("angle away is " + str(angleAwayFromNeighbourhood))
	def addRand(self):
		self.coord.x = self.coord.x + randint(-10 ,10)/10
		self.coord.y = self.coord.y + randint(-10 ,10)/10
	def calcAlignment(self):
		angle = 0
		for i in self.viewableBoidsList:
			angle = angle +i.coord.getDir()
		self.aveDirAngle = angle

		self.coord.x = self.coord.x + (1*np.cos(self.aveDirAngle))
		self.coord.y = self.coord.y + (1*np.sin(self.aveDirAngle))
	def calcAngleToNeighbours(self):
		angleToNeighbourhood = maths.atan2(self.aveNeibourhoodPos.y - self.coord.y, self.aveNeibourhoodPos.x - self.coord.x)
		return angleToNeighbourhood
	def calcCohesion(self):
		angleToNeighbourhood = self.calcAngleToNeighbours()
		self.coord.x = self.coord.x + (2*np.cos(angleToNeighbourhood))
		self.coord.y = self.coord.y + (2*np.sin(angleToNeighbourhood))
		print("angle to is " + str(angleToNeighbourhood))
	def getViewableBoids(self, boidsList):
		for i in boidsList:
			xDiff = self.coord.x - i.coord.x
			yDiff = self.coord.y - i.coord.y
			dist = maths.hypot(xDiff, yDiff)
			if dist < BoidsWindow.boidViewingDistance:
				self.viewableBoidsList.append(i)

class Vector():
	def __init__(self, x,y):
		self.x = x
		self.y = y
	def getDir(self):
		return np.arctan(self.x/self.y)
	def getMag(self):
		return sqrt(self.x**2 + self.y**2)









if __name__ == '__main__':
	app = QApplication(sys.argv)
	appWindow = BoidsWindow()
	appWindow.show()
	app.exec()


