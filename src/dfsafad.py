from PyQt5 import QtGui, QtCore, QtWidgets
from mathgl import *
import sys

app = QtWidgets.QApplication(sys.argv)
qpointf=QtCore.QPointF()

class hfQtPlot(QtWidgets):
    def __init__(self, parent=None):
        QtWidgets.__init__(self, parent)
        self.img=(QtGui.QImage())
    def setgraph(self,gr):
        self.buffer='\t'
        self.buffer=self.buffer.expandtabs(4*gr.GetWidth()*gr.GetHeight())
        gr.GetBGRN(self.buffer,len(self.buffer))
        self.img=QtGui.QImage(self.buffer, gr.GetWidth(),gr.GetHeight(),QtGui.QImage.Format_ARGB32)
        self.update()
    def paintEvent(self, event):
        paint = QtGui.QPainter()
        paint.begin(self)
        paint.drawImage(qpointf,self.img)
        paint.end()

BackgroundColor=[1.0,1.0,1.0]
size=100
gr=mglGraph()
y=mglData(size)
#y.Modify("((0.7*cos(2*pi*(x+.2)*500)+0.3)*(rnd*0.5+0.5)+362.135+10000.)")
y.Modify("(cos(2*pi*x*10)+1.1)*1000.*rnd-501")
x=mglData(size)
x.Modify("x^2");

def plotpanel(gr,x,y,n):
    gr.SubPlot(2,2,n)
    gr.SetXRange(x)
    gr.SetYRange(y)
    gr.AdjustTicks()
    gr.Axis()
    gr.Box()
    gr.Label("x","x-Axis",1)
    gr.Label("y","y-Axis",1)
    gr.ClearLegend()
    gr.AddLegend("Legend: "+str(n),"k")
    gr.Legend()
    gr.Plot(x,y)


gr.Clf(BackgroundColor[0],BackgroundColor[1],BackgroundColor[2])
gr.SetPlotFactor(1.5)
plotpanel(gr,x,y,0)
y.Modify("(cos(2*pi*x*10)+1.1)*1000.*rnd-501")
plotpanel(gr,x,y,1)
y.Modify("(cos(2*pi*x*10)+1.1)*1000.*rnd-501")
plotpanel(gr,x,y,2)
y.Modify("(cos(2*pi*x*10)+1.1)*1000.*rnd-501")
plotpanel(gr,x,y,3)

gr.WritePNG("test.png","Test Plot")

qw = hfQtPlot()
qw.show()
qw.setgraph(gr)
qw.raise_()