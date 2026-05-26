import pyqtgraph as pg
pg.plot(data)

pw = pg.plot(xVals, yVals, pen='r')
pw.plot(xVals, yVals, pen='b')

win = pg.GraphicsLayoutWidget()
win.addPlot(data1, row=0, col=0)
win.addPlot(data2, row=0, col=1)
win.addPlot(data3, row=1, col=0, colspan=0)
pg.show(imageData)
