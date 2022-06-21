from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice
import pandas as pd
from datetime import datetime
from collections import deque
from itertools import islice
import numpy as np
from scipy.fft import rfft, rfftfreq


app = QtWidgets.QApplication([])
ui = uic.loadUi("design.ui")
ui.setWindowTitle("PyGraph")

serial = QSerialPort()
serial.setBaudRate(115200)
port_list = []
ports = QSerialPortInfo().availablePorts()
for port in ports:
    port_list.append(port.portName())
ui.comL.addItems(port_list)

size = 512
i = size

bufferX = deque([0]*size, maxlen=size)
bufferY = deque([0]*size, maxlen=size)
bufferZ = deque([0]*size, maxlen=size)
bufferTi = deque([0]*size, maxlen=size)

data = []
dictXYZ = {'X': [], 'Y': [], 'Z': [], 'Time': []}

flag_update = False
flag_StartEXP = False
flag_is_start = False


ui.graph.addLegend()
ui.graph.showGrid(x=True, y=True, alpha=0.8)
ui.graph.setLabel('left', 'Amplitude')
ui.graph.setLabel('bottom', 'Time (ms)')

curve1 = ui.graph.plot(pen="r", name="Accel X")
curve2 = ui.graph.plot(pen="g", name="Accel Y")
curve3 = ui.graph.plot(pen="b", name="Accel Z")
curve4 = ui.graph.plot()


ui.graph_2.addLegend()
ui.graph_2.showGrid(x=True, y=True, alpha=0.8)
ui.graph_2.setLabel('left', 'Amplitude')
ui.graph_2.setLabel('bottom', 'frq (Hz)')

curve5 = ui.graph_2.plot(pen="r", name="Accel X")
curve6 = ui.graph_2.plot(pen="g", name="Accel Y")
curve7 = ui.graph_2.plot(pen="b", name="Accel Z")
curve8 = ui.graph_2.plot()


def on_read():
    global data
    rx = serial.readLine()
    rxs = str(rx, 'utf-8').strip()
    data = rxs.split('+')
    try:
        ui.lcdX.display(float(data[0]))
        ui.lcdY.display(float(data[1]))
        ui.lcdZ.display(float(data[2]))
        ui.lcdT.display(float(data[4]))
    except IndexError:
        pass


def update():
    global flag_StartEXP, data, dictXYZ, curve1, curve2, curve3, i, bufferX, bufferY, bufferZ
    if flag_StartEXP:

        dictXYZ['X'].append(float(data[0]))
        dictXYZ['Y'].append(float(data[1]))
        dictXYZ['Z'].append(float(data[2]))
        dictXYZ['Time'].append(float(data[4]))

        if i > 0:
            i -= 1

        bufferX.append(float(data[0]))
        bufferY.append(float(data[1]))
        bufferZ.append(float(data[2]))
        bufferTi.append(float(data[4]))

        curve1.setData(list(islice(bufferTi, i, size)), list(islice(bufferX, i, size)))
        curve1.setPos(0, 0)

        curve2.setData(list(islice(bufferTi, i, size)), list(islice(bufferY, i, size)))
        curve2.setPos(0, 0)

        curve3.setData(list(islice(bufferTi, i, size)), list(islice(bufferZ, i, size)))
        curve3.setPos(0, 0)

        spec_x = rfft(list(islice(bufferX, 0, size)))
        abs_spec_x = np.abs(spec_x)

        xf = rfftfreq(size, 1. / 100)

        curve5.setData(xf, abs_spec_x)
        curve5.setPos(0, 0)

        spec_y = rfft(list(islice(bufferY, 0, size)))
        abs_spec_y = np.abs(spec_y)

        curve6.setData(xf, abs_spec_y)
        curve6.setPos(0, 0)

        spec_z = rfft(list(islice(bufferZ, 0, size)))
        abs_spec_z = np.abs(spec_z)

        curve7.setData(xf, abs_spec_z)
        curve7.setPos(0, 0)

        app.processEvents()


def start_exp():
    global flag_StartEXP, flag_is_start
    flag_StartEXP = True
    flag_is_start = True
    print("on")


def stop_exp():
    global flag_StartEXP, flag_is_start, dictXYZ, i, bufferX, bufferY, bufferZ,bufferTi, data
    if flag_is_start:
        df = pd.DataFrame(data=dictXYZ)
        new_name_file = str(f'./Accel/Accel{str(datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p"))}.xlsx')
        print(new_name_file)
        df.to_excel(new_name_file)
        print("off")

        flag_StartEXP = False

        bufferX = deque([0] * size, maxlen=size)
        bufferY = deque([0] * size, maxlen=size)
        bufferZ = deque([0] * size, maxlen=size)
        bufferTi = deque([0] * size, maxlen=size)

        data.clear()

        dictXYZ['X'].clear()
        dictXYZ['Y'].clear()
        dictXYZ['Z'].clear()
        dictXYZ['Time'].clear()

        i = size

        flag_is_start = False


def on_open():
    serial.setPortName(ui.comL.currentText())
    serial.open(QIODevice.ReadWrite)


def on_close():
    serial.close()


serial.readyRead.connect(on_read)
ui.openB.clicked.connect(on_open)
ui.closeB.clicked.connect(on_close)

ui.onB.clicked.connect(start_exp)
ui.offB.clicked.connect(stop_exp)

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(10)
ui.show()
app.exec()
