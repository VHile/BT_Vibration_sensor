from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice
import pandas as pd
from datetime import datetime
import numpy as np
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys
import pyqtgraph.opengl as gl

app = QtWidgets.QApplication([])
ui = uic.loadUi("design.ui")
ui.setWindowTitle("Serial")

serial = QSerialPort()
serial.setBaudRate(115200)
portlist = []
ports = QSerialPortInfo().availablePorts()
for port in ports:
    portlist.append(port.portName())
ui.comL.addItems(portlist)
print(portlist)

bufferX = np.zeros(1000000, float)
bufferY = np.zeros(1000000, float)
bufferZ = np.zeros(1000000, float)

listX = []
listY = []
listZ = []
list_t = []

t = 0
x = 0
i = 0
flag_update = False
flag_StartEXP = False
flag_is_start = False

listXYZ = {'X': [], 'Y': [], 'Z': [], 'T': []}

ui.graph.addLegend()
ui.graph.showGrid(x=True, y=True, alpha=0.8)
ui.graph.setLabel('left', 'Amplitude (16bit Signed)')

curve1 = ui.graph.plot(pen="r", name="Accel X")
curve2 = ui.graph.plot(pen="g", name="Accel Y")
curve3 = ui.graph.plot(pen="b", name="Accel Z")
curve4 = ui.graph.plot()

#for i in range(len(listX)):
#    listXYZ['X'].append(listX[i])
#for i in range(len(listY)):
#    listXYZ['Y'].append(listY[i])
#for i in range(len(listZ)):
#    listXYZ['Z'].append(listZ[i])

data = [None]*5

def onRead():
    global listX, list_t, t, data, listXYZ
    rx = serial.readLine()
    rxs = str(rx, 'utf-8').strip()
    data = rxs.split('+')
    try:
        ui.lcdX.display(float(data[0]))
        ui.lcdY.display(float(data[1]))
        ui.lcdZ.display(float(data[2]))
        ui.lcdT.display(float(data[3]))
    except IndentationError:
        print('?')

def update():
    global t, x, listX, listY, listZ,  list_t, flag_StartEXP, data, listXYZ, curve1, curve2, curve3, i, bufferX, bufferY, bufferZ
    if flag_StartEXP:
        t += 1
        x += 1
        listX.append(float(data[0]))
        listY.append(float(data[1]))
        listZ.append(float(data[2]))
        list_t.append(t)
        bufferX[i] = data[0]
        bufferY[i] = data[1]
        bufferZ[i] = data[2]
        listXYZ['X'].append(float(data[0]))
        listXYZ['Y'].append(float(data[1]))
        listXYZ['Z'].append(float(data[2]))
        listXYZ['T'].append(float(data[3]))

#        ui.graph.clear()
#        curve1.setData(list_t, listX)
        curve1.setData(bufferX[0:i])
        curve1.setPos(0, 0)

        curve2.setData(bufferY[0:i])
        curve2.setPos(0, 0)

        curve3.setData(bufferZ[0:i])
        curve3.setPos(0, 0)
        i += 1
        app.processEvents()

def StartEXP():
    global flag_StartEXP, flag_is_start
    flag_StartEXP = True
    flag_is_start = True
    print("on")

#    serial.write(txs.encode())

def StopEXP():
    global listXYZ, listX, listY, listZ, flag_StartEXP, n_file, flag_is_start
    if flag_is_start:
        df = pd.DataFrame(data=listXYZ)

        new_name_file = str('./Accel/Accel' + str(datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p")) + '.xlsx')

        print(new_name_file)
        df.to_excel(new_name_file)
        print("off")
        flag_StartEXP = False
        listX.clear()
        listY.clear()
        listZ.clear()
        list_t.clear()

        listXYZ['X'].clear()
        listXYZ['Y'].clear()
        listXYZ['Z'].clear()
        listXYZ['T'].clear()

#        ui.graph.clear()
        flag_is_start = False
#    serial.write(txs.encode())

def onOpen():
   serial.setPortName(ui.comL.currentText())
   serial.open(QIODevice.ReadWrite)

def onClose():
    serial.close()

serial.readyRead.connect(onRead)
ui.openB.clicked.connect(onOpen)
ui.closeB.clicked.connect(onClose)

ui.onB.clicked.connect(StartEXP)
ui.offB.clicked.connect(StopEXP)

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(10)
#timer.setInterval(dt)

ui.show()
app.exec()