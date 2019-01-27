from visual import *
import gravityFieldBall
import math
import wx
import wx.grid as gridlib

#window size
L = 660
W = 635

w = window(width=L, height=W,
           menus=False, title='Ball motion in gravity field - 2D simulation',
           style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)

#create scene in VPython inside window:
scene = display(window=w, x=10, y=105, width=600, height=500, center=(40,28,0), background=(0,0,0), autoscale=True)
hV_label = label(pos=(45, 55, 0), text='h=\nV=', xoffset=1, line=0, box=True, opacity=0)

p = w.panel

showVelcheck=wx.CheckBox(p, label="Show velocity vector", pos=(505,68), style=0, name="showVel")

#RADIO BUTTONS:
radio1=wx.RadioButton(p, label=" Free fall:", pos=(30, 4), size=(110, 25), style=wx.RB_GROUP, name="radio1")
radio2=wx.RadioButton(p, label=" Horizontal motion:", pos=(30, 33), size=(130, 25), style=0, name="radio2")
radio3=wx.RadioButton(p, label=" Angular motion:", pos=(30, 62), size=(110, 25), style=0, name="radio3")

#LABELS:
labelOfInitialH1=wx.StaticText(p, label="h_0", pos=(170, 9))
labelOfInitialH2=wx.StaticText(p, label="h_0", pos=(170, 38))
labelOfInitialH3=wx.StaticText(p, label="h_0", pos=(170, 67))

labelUnitM1=wx.StaticText(p,label="[m]", pos=(242,9))
labelUnitM2=wx.StaticText(p,label="[m]", pos=(242,38))
labelUnitM3=wx.StaticText(p,label="[m]", pos=(242,67))

labelOfInitialVx0_1=wx.StaticText(p, label="Vx0", pos=(275, 9))
labelOfInitialVx0_2=wx.StaticText(p, label="Vx0", pos=(275, 38))
labelOfInitialVx0_3=wx.StaticText(p, label="Vx0", pos=(275, 67))

labelUnitVx0_1=wx.StaticText(p,label="[m/s]", pos=(331,9))
labelUnitVx0_2=wx.StaticText(p,label="[m/s]", pos=(347,38))
labelUnitVx0_3=wx.StaticText(p,label="[m/s]", pos=(347,67))


labelOfInitialVy0_1=wx.StaticText(p, label="Vy0", pos=(390, 9))
labelOfInitialVy0_2=wx.StaticText(p, label="Vy0", pos=(390, 38))
labelOfInitialVy0_3=wx.StaticText(p, label="Vy0", pos=(390, 67))

labelUnitVy0_1=wx.StaticText(p,label="[m/s]", pos=(463,9))
labelUnitVy0_2=wx.StaticText(p,label="[m/s]", pos=(446,38))
labelUnitVy0_3=wx.StaticText(p,label="[m/s]", pos=(463,67))

labelDt=wx.StaticText(p, label="dt", pos=(505, 38))

#INPUT FIELDS:
inputH0_1 = wx.SpinCtrl(p, value="50", min=1, max=50, pos=(195, 7), size=(45, -1))
inputH0_2 = wx.SpinCtrl(p, value="50", min=1, max=50, pos=(195, 36), size=(45, -1))
inputH0_2.Enable(False)
inputH0_3 = wx.SpinCtrl(p, value="0", min=0, max=50, pos=(195, 65), size=(45, -1))
inputH0_3.Enable(False)

inputVx0_1 = wx.TextCtrl(p, value="0", pos=(300, 7), size=(27, -1))
inputVx0_1.Enable(True)
inputVx0_1.SetEditable(False)
inputVx0_2 = wx.SpinCtrl(p, value="10", max=10, min=1, pos=(300, 36), size=(45, -1))
inputVx0_2.Enable(False)
inputVx0_3 = wx.SpinCtrl(p, value="10", max=10, min=1, pos=(300, 65), size=(45, -1))
inputVx0_3.Enable(False)

inputVy0_1 = wx.SpinCtrl(p, value="0", max=10, pos=(415, 7), size=(45, -1))
inputVy0_2 = wx.TextCtrl(p, value="0", pos=(415, 36), size=(27, -1))
inputVy0_2.Enable(False)
inputVy0_3 = wx.SpinCtrl(p, value="30", max=30, min=1, pos=(415, 65), size=(45, -1))
inputVy0_3.Enable(False)

inputDt = wx.TextCtrl(p, value="0.1", pos=(522, 36), size=(35, -1))


def enablerDisabler(event):

    if radio1.GetValue() == True:
        inputH0_1.Enable(True)
        inputH0_2.Enable(False)
        inputH0_3.Enable(False)
        inputVx0_1.Enable(True)
        inputVx0_1.SetEditable(False)
        inputVx0_2.Enable(False)
        inputVx0_3.Enable(False)
        inputVy0_1.Enable(True)
        inputVy0_2.Enable(False)
        inputVy0_3.Enable(False)
    if radio2.GetValue() == True:
        inputH0_1.Enable(False)
        inputH0_2.Enable(True)
        inputH0_3.Enable(False)
        inputVx0_1.Enable(False)
        inputVx0_2.Enable(True)
        inputVx0_3.Enable(False)
        inputVy0_1.Enable(False)
        inputVy0_2.Enable(True)
        inputVy0_2.SetEditable(False)
        inputVy0_3.Enable(False)
    if radio3.GetValue() == True:
        inputH0_1.Enable(False)
        inputH0_2.Enable(False)
        inputH0_3.Enable(True)
        inputVx0_1.Enable(False)
        inputVx0_2.Enable(False)
        inputVx0_3.Enable(True)
        inputVy0_1.Enable(False)
        inputVy0_2.Enable(False)
        inputVy0_3.Enable(True)

p.Bind(wx.EVT_RADIOBUTTON,enablerDisabler)

#small button for re-sizing window and panel for making red outline around it, when results are calculated
pan = wx.Panel(parent=p, size=(36, 29), pos=(612, 337))
buttonResize = wx.Button(pan, label=">>", pos=(3, 3), size=(30, 23))


def resizeWindow(event):

    if buttonResize.GetLabel() == ">>":
        buttonResize.SetLabel("<<")
        pan.SetBackgroundColour("Default")
        pan.Refresh()
        w.win.SetSize(wx.Size(985, W))
        return

    if buttonResize.GetLabel() == "<<":
        buttonResize.SetLabel(">>")
        pan.SetBackgroundColour("Default")
        pan.Refresh()
        w.win.SetSize(wx.Size(L, W))
        return

buttonResize.Bind(wx.EVT_BUTTON, resizeWindow)


class Simulation(object):
    g = -gravityFieldBall.Ball.g

    def __init__(self):

        self.ifSimulationWorks=False
        self.simulationCalculatedParameters={'hmax':-1,'vxend':-1,'vyend':-1,'Vend':-1,'d':-1,'hmin':1000000, 'tend':-1}

        #BUTTONS:
        buttonStart = wx.Button(p, label="Start simulation", pos=(505, 5), size=(100,23))
        buttonStart.Enable(false)
        buttonStop = wx.Button(p, label="Stop", pos=(565, 36), size=(40,23))
        buttonStart.Bind(wx.EVT_BUTTON, self.runSimulation)
        buttonStop.Bind(wx.EVT_BUTTON, self.stopSimulation)
        buttonSave = wx.Button(p, label="Save", pos=(785, 210), size=(50,23))
        buttonClear = wx.Button(p, label="Clear", pos=(785, 453), size=(50,23))
        buttonSave.Bind(wx.EVT_BUTTON, self.saveResults)
        buttonClear.Bind(wx.EVT_BUTTON, self.clearSavedTable)

        showVelcheck.Bind(wx.EVT_CHECKBOX, self.showHideVelocityVector)

        #GRIDS:
        self.resultGrid=gridlib.Grid(p, pos=(657, 73), size=(400, 130))
        self.resultGrid=self.initiateGrid(self.resultGrid)
        self.backupGrid=gridlib.Grid(p, pos=(657, 316), size=(400, 130))
        self.backupGrid=self.initiateGrid(self.backupGrid)

        #LABELS:
        self.labelCurrentResults = wx.StaticText(p, label="CURRENT RESULTS: ", pos=(657, 9))
        self.labelSavedResults = wx.StaticText(p, label="SAVED RESULTS: ", pos=(657, 255))
        self.labelInitialValues1=wx.StaticText(p, label="For initial values: ", pos=(657, 37))
        self.labelInitialValues2=wx.StaticText(p, label="For initial values: ", pos=(657, 280))
        self.labelNotice=wx.StaticText(p, label="NOTICE: To improve accuracy of calculations reduce\n time step (dt)", pos=(657, 485))

        self.drawXYaxis()
        wx.Yield()#to freeze Start button until Vpython scene with axis is loaded
        buttonStart.Enable(true)

        self.initialData={}

    def initiateGrid(self, grid):

        grid.CreateGrid(5, 3)
        grid.SetDefaultCellBackgroundColour(self.resultGrid.GetLabelBackgroundColour())
        grid.EnableEditing(False)
        grid.SetCellHighlightPenWidth(0)
        grid.DisableDragRowSize()
        grid.DisableDragColSize()
        grid.SetRowLabelSize(70)
        grid.SetRowLabelValue(0, "hmax [m]")
        grid.SetRowLabelValue(1, "tmax [s]")
        grid.SetRowLabelValue(2, "Vend [m/s]")
        grid.SetRowLabelValue(3, "tend [s]")
        grid.SetRowLabelValue(4, "d [m]")
        grid.SetColLabelValue(0, "Simulated\n value")
        grid.SetColLabelValue(1, "Theoretical\n value")
        grid.SetColLabelValue(2, "Delta")

        return grid


    def clearResultTable(self):
        self.resultGrid.ClearGrid()
        self.labelInitialValues1.SetLabel("For initial values:")

    def clearSavedTable(self, event=None):
        self.backupGrid.ClearGrid()
        self.labelInitialValues2.SetLabel("For initial values:")


    def saveResults(self, event=None):

        for i in range(0,self.resultGrid.GetNumberRows()):
            for j in range(0, self.resultGrid.GetNumberCols()):
                self.backupGrid.SetCellValue(i,j,self.resultGrid.GetCellValue(i,j))
        self.labelInitialValues2.SetLabel(self.labelInitialValues1.GetLabel())


    def initEntryData(self):
        if radio1.GetValue():  #if radio button nr 1 is selected (is true)
            self.initialData={'x0':0,'y0':int(inputH0_1.GetValue()), 'vx0':int(inputVx0_1.GetValue()), 'vy0':int(inputVy0_1.GetValue()), 'dt':float(inputDt.GetValue())}
        if radio2.GetValue():
            self.initialData={'x0':0,'y0':int(inputH0_2.GetValue()), 'vx0':int(inputVx0_2.GetValue()), 'vy0':int(inputVy0_2.GetValue()), 'dt':float(inputDt.GetValue())}
        if radio3.GetValue():
            self.initialData={'x0':0,'y0':int(inputH0_3.GetValue()), 'vx0':int(inputVx0_3.GetValue()), 'vy0':int(inputVy0_3.GetValue()), 'dt':float(inputDt.GetValue())}

    def showHandV(self):
        h="h="+str(round(self.ourBall.y,2))+" m"
        hV_label.text = h+"\nV="+str(round(math.sqrt(self.ourBall.vx**2+self.ourBall.vy**2),2))+" m/s"

    def calculateEndParameters(self):
        if self.ourBall.y>self.simulationCalculatedParameters['hmax']:
            self.simulationCalculatedParameters['hmax']=self.ourBall.y
            self.simulationCalculatedParameters['tmax']=self.ourBall.t

        if self.ourBall.y>0 and self.ourBall.y<self.simulationCalculatedParameters['hmin'] and self.ourBall.vy<0:
            self.simulationCalculatedParameters['hmin']=self.ourBall.y
            self.simulationCalculatedParameters['d']=self.ourBall.x
            self.simulationCalculatedParameters['vxend']=self.ourBall.vx
            self.simulationCalculatedParameters['vyend']=self.ourBall.vy
            self.simulationCalculatedParameters['Vend']=math.sqrt(self.ourBall.vx**2+self.ourBall.vy**2)
            self.simulationCalculatedParameters['tend']=self.ourBall.t


    def drawXYaxis(self):
        xmin = 0.
        xmax = 50.
        ymin = 0.
        ymax = 55.

        # tick marks
        tic_dx = 5
        tic_h = 1

        self.xaxis = arrow(pos=(xmin, 0, 0), axis=(xmax+tic_dx, 0, 0), shaftwidth=0.2)# axes
        self.yaxis = arrow(pos=(0, ymin, 0), axis=(0, ymax+tic_dx, 0), shaftwidth=0.2)

        labelY = text(text='y [m]', depth=0.4, color=color.white, height=1.5, pos=[-6 * tic_h, ymax+tic_dx])
        labelX = text(text='x [m]', depth=0.4, color=color.white, height=1.5, pos=[ymax, -3 * tic_h], font='serif')

        self.gravityVector = arrow(pos=(70, 55, 0), axis=(0, -5, 0), shaftwidth=0.5, color=color.blue)
        self.gravityVectorLabel = text(text='g',pos=(72, 53, 0), axis=(1, 0, 0), color=color.blue, height=2)

        for i in arange(xmin,xmax+tic_dx,tic_dx):
         tic = curve(pos=[(i,-0.5*tic_h),(i,0.5*tic_h)])
         label = text(text=str(int(i)), depth=0.4, color=color.white, height=1.5, pos=[i,-3*tic_h], font='serif')

        for i in arange(ymin,ymax+tic_dx,tic_dx):
         tic = curve(pos=[(-0.5*tic_h,i),(0.5*tic_h,i)])
         label = text(text=str(int(i)), depth=0.4, color=color.white, height=1.5, pos=[-3*tic_h,i], font='serif')

        return "done"

    def presentResults(self, teo, sim):
        if teo['hmax']!=None:
         self.resultGrid.SetCellValue(0, 0, str(round(sim['hmax'],2)))
         self.resultGrid.SetCellValue(0, 1, str(round(teo['hmax'],2)))
         self.resultGrid.SetCellValue(0,2, str(round(math.fabs(sim['hmax']-teo['hmax']),2)))

        if teo['tmax']!=None:
         self.resultGrid.SetCellValue(1, 0, str(round(sim['tmax'],2)))
         self.resultGrid.SetCellValue(1, 1, str(round(teo['tmax'],2)))
         self.resultGrid.SetCellValue(1,2, str(round(math.fabs(sim['tmax']-teo['tmax']),2)))

        if teo['Vend']!=None:
         self.resultGrid.SetCellValue(2, 0, str(round(sim['Vend'],2)))
         self.resultGrid.SetCellValue(2, 1, str(round(teo['Vend'],2)))
         self.resultGrid.SetCellValue(2,2, str(round(math.fabs(sim['Vend']-teo['Vend']),2)))

        if teo['tend']!=None:
         self.resultGrid.SetCellValue(3, 0, str(round(sim['tend'],2)))
         self.resultGrid.SetCellValue(3, 1, str(round(teo['tend'],2)))
         self.resultGrid.SetCellValue(3,2, str(round(math.fabs(sim['tend']-teo['tend']),2)))

        if teo['d']!=None:
         self.resultGrid.SetCellValue(4, 0, str(round(sim['d'],2)))
         self.resultGrid.SetCellValue(4, 1, str(round(teo['d'],2)))
         self.resultGrid.SetCellValue(4, 2, str(round(math.fabs(sim['d']-teo['d']),2)))

        if buttonResize.GetLabel()==">>":
          pan.SetBackgroundColour("Red")
          pan.Refresh()
          pan.Show()

        self.labelInitialValues1.SetLabel("For initial values: h_0="+str(self.initialData['y0'])+" m, Vx0="+str(self.initialData['vx0'])+" m/s, Vy0="+str(self.initialData['vy0'])+" m/s,\ndt="+str(self.initialData['dt'])+" s")

    def showHideVelocityVector(self, event=None):
        try:# if ball object yet exists
         if showVelcheck.GetValue()==True:
            self.ourBall.velocityVector.visible=True
         else:
            self.ourBall.velocityVector.visible=False
        except:
            pass


    def runSimulation(self, event=None):

        pan.SetBackgroundColour("Default")
        pan.Refresh()

        self.simulationCalculatedParameters={'hmax':-1, 'vxend':-1, 'vyend':-1, 'Vend':-1, 'd':-1, 'tend':-1, 'hmin':1000000}
        self.stopSimulation()
        self.initEntryData()
        self.ourBall=gravityFieldBall.Ball(self.initialData, float(inputDt.GetValue()))


        if self.ifSimulationWorks == False:
            self.ifSimulationWorks = True
            status=True
            self.showHideVelocityVector()
            self.showHandV()#show initial values

            while self.ifSimulationWorks and status:
                self.calculateEndParameters()
                scene.autoscale = False
                rate(30)
                status=self.ourBall.nextStep()
                if self.ifSimulationWorks:
                 self.showHandV()

        if self.ifSimulationWorks:#is False when user clicks 'Stop' button
         self.presentResults(self.getTheoreticalResults(self.initialData), self.simulationCalculatedParameters)

        self.ifSimulationWorks=False
        return

    def stopSimulation(self, event=None):

        self.ifSimulationWorks=False
        pan.SetBackgroundColour("Default")
        pan.Refresh()
        hV_label.text="h=\nV="
        self.clearResultTable()
        try:
         self.ourBall.mysphere.visible=False
         self.ourBall.velocityVector.visible=False
        except:
            pass

    def getTheoreticalResults(self, data):

        tend=None
        Vend=None
        tmax=None
        hmax=None
        d=None

        if data['y0']>0 and data['vx0']==0 and data['vy0']==0:#free fall motion only
            tend=math.sqrt(2*data['y0']/(-self.g))
            Vend=math.sqrt(2*(-self.g)*data['y0'])

        if data['vx0']==0 and data['vy0']>0:#free fall with upward motion at start
            hmax=data['y0']+data['vy0']**2/(2*(-self.g))
            tmax=data['vy0']/(-self.g)
            tend=math.sqrt(2*hmax/(-self.g))+tmax
            Vend=math.sqrt(2*(-self.g)*(data['y0']+(data['vy0']**2/(-2*self.g))))

        if data['vx0']>0 and data['vy0']==0:#horizontal projection
            tend=math.sqrt(2*data['y0']/(-self.g))
            Vend=math.sqrt(data['vx0']**2+2*(-self.g)*data['y0'])
            d=data['vx0']*math.sqrt((2*data['y0'])/(-self.g))

        if data['vx0']>0 and data['vy0']>0 and data['y0']==0:#angular projection from h0=0
            tend=2*data['vy0']/(-self.g)
            d=data['vx0']*tend
            hmax=data['vy0']**2/(2*-self.g)
            Vend=math.sqrt(data['vx0']**2+data['vy0']**2)
            tmax=data['vy0']/(-self.g)

        if data['vx0']>0 and data['vy0']>0 and data['y0']>0:#angular projection from h0>0
            tend=(data['vy0']+math.sqrt(data['vy0']**2+2*data['y0']*(-self.g)))/(-self.g)
            d=data['vx0']*tend
            hmax=data['vy0']**2/(2*-self.g)+data['y0']
            Vend=math.sqrt(data['vx0']**2+data['vy0']**2+2*(-self.g)*data['y0'])
            tmax=data['vy0']/(-self.g)

        return {"tend":tend, "Vend":Vend, "tmax":tmax, "hmax":hmax, "d":d}


sym = Simulation()

