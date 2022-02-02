
# coding: utf-8

# In[ ]:


from PyQt5.QtCore import*
from PyQt5.QtGui import*
from PyQt5.QtWidgets import*
import functools
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import*
import sys
import os
import numpy as np
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import csv
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas,NavigationToolbar2QT as NavigationToolbar
import re

from mpl_toolkits.mplot3d import Axes3D
class DockDialog(QMainWindow):
    def __init__(self,parents,folder):
        super().__init__()
        
        self.createDockWidget(parents,folder)
    
    def createDockWidget(self,parents,folder):
        parents.dock = QDockWidget("FOLDER", parents)
        parents.l1 = QTreeWidgetItem(["TE/TM REFLECTION (MAGNITUDE)"])
        parents.l2 = QTreeWidgetItem(["TE/TM REFLECTION (PHASE)"])
        parents.l3 = QTreeWidgetItem(["TE/TM TRANSMISSION (MAGNITUDE)"])
        parents.l4 = QTreeWidgetItem(["TE/TM TRANSMISSION (PHASE)"])
        parents.l5= QTreeWidgetItem(["FAR FIELD PATTERN"])
        parents.l6= QTreeWidgetItem(["3d SURFACE"])
        parents.l7= QTreeWidgetItem(["GA DATA"])
        
        
        w = QWidget()
        parents.tw = QTreeWidget(w)
        parents.tw.setHeaderLabel(folder)
        parents.tw.addTopLevelItem(parents.l1)
        parents.tw.addTopLevelItem(parents.l2)
        parents.tw.addTopLevelItem(parents.l3)
        parents.tw.addTopLevelItem(parents.l4)
        parents.tw.addTopLevelItem(parents.l5)
        parents.tw.addTopLevelItem(parents.l6)
        parents.tw.addTopLevelItem(parents.l7)
        self.update_docket(parents,folder)
        parents.addDockWidget(Qt.LeftDockWidgetArea, parents.dock)
        
    #FOR UPDATING DOCKET IN CASE OF NEW FOLDER
    def update_docket(self,parents,folder):
        
        
       
      
        try:
            list_files=os.listdir(folder)
            self.folder=folder
        except:
            
            list_files=os.getcwd()
            
            self.folder=os.getcwd()
        parents.tw.setHeaderLabel(self.folder)
        parents.central_widget()
        parents.file_status=[False]*3    
        item = parents.tw.invisibleRootItem() 
        for i in range(item.childCount()):
            item.child(i).setSelected(False)
        if(list_files):
            item = parents.tw.invisibleRootItem()
            for f in list_files:
                if(f[-5:]=='.RTEF' and parents.file_status[0]==False):
                    try:
                        parents.load_file_data(folder+"\\"+f,'.RTEF')
                        parents.file_status[0]=True
                    except:
                         parents.file_status[0]=False
                             
                            
                    if(parents.file_status[0]==True):
                        child = item.child(0)
                        child.setSelected(True)
                        child = item.child(1)
                        child.setSelected(True)
                   
                elif(f[-5:]=='.TTEF' and parents.file_status[1]==False):
                    try:
                        parents.load_file_data(folder+"\\"+f,'.TTEF')
                        parents.file_status[1]=True
                    except:
                         parents.file_status[1]=False
                    if(parents.file_status[1]==True):
                        child = item.child(2)
                        child.setSelected(True)
                        child = item.child(3)
                        child.setSelected(True)
                 

                  
                elif(f[-6:]=='.3DCTE' and parents.file_status[2]==False):
                    try:
                        parents.load_file_data(folder+"\\"+f,'.3DCTE')
                        parents.file_status[2]=True
                    except:
                        parents.file_status[2]=False
                    if(parents.file_status[2]==True):
                        #child = item.child(4)
                        #child.setSelected(True)
                        child = item.child(5)
                        child.setSelected(True)
                        #child = item.child(6)
                        #child.setSelected(True)
                       
        if(True in parents.file_status):
            f = open(os.getcwd()+"\\AA.info\\folder.txt", "r+")
            f.read()
            f.seek(0)
            f.write(folder)
            f.truncate()
            f.close()

                    
        parents.tw.itemClicked.connect(parents.plot_file)
       
        parents.dock.setWidget(parents.tw)
        
        
        
class Canvas(FigureCanvas):
    def __init__(self,parent=None,width=5,height=4,dpi=100,pro=None):
       
        if(pro==None):
            self.fig=Figure(figsize=(width,height),dpi=dpi)
            self.axes=self.fig.add_subplot(111)
      
            self.fig.tight_layout()
        elif(pro=='3d'):
            plt.close('all')
            self.fig=plt.figure(figsize=(14,8),dpi=dpi)
            left, bottom, width, height = 0.2, 0.1, 0.6, 0.8
            self.axes = self.fig.add_axes([left, bottom, width, height]) 

        super().__init__(self.fig)


    

       
class Example(QMainWindow,QObject):
   
    
    def __init__(self):
        super().__init__()
        
     
        
        self.initUI()
    def exitapp(self): 
        sys.exit() 
   

    #LOADS DATA FROM FILE AND STORES IT
    def load_file_data(self,filename,ext):
        x = []
        y = []
        z=  []
        f=  []
        g=  []
        if(ext!=".3DCTE"):
            with open(filename,'r') as csvfile:
                lines=csvfile.readlines()
                for line in lines:
                    row=list(line.split())
                    x.append(float(row[0]))
                    y.append(float(row[1]))
                    z.append(float(row[2]))
                
                if(ext==".RTEF"):
                    self.file_status[0]=True
                    self.x1=x
                    self.y1=y
                    self.z1=z
                elif(ext==".TTEF"):
                    self.file_status[1]=True
                    self.x2=x
                    self.y2=y
                    self.z2=z
            
        else:
            with open(filename,'r') as csvfile:
                lines=csvfile.readlines()
                for line in lines:
                    row=list(line.split())
                    f.append(float(row[0]))
                    g.append(float(row[1]))
                    x.append(float(row[2]))
                    y.append(float(row[3]))
                    z.append(float(row[4]))    
                self.file_status[2]=True
                self.f3=f
                self.g3=g
                self.x3=x
                self.y3=y
                self.z3=z
        
        
     
     
           
        
        
    #SLOT FOR ITEMS IN DOCKET, PLOTS DATA
    def plot_file(self,item=None):
        if(item!=None and item.parent()==None):
            if(item==self.l1 and self.file_status[0]==True):
                self.mag_2dplot("*.RTEF")
            elif(item==self.l2 and self.file_status[0]==True):
                self.phase_2dplot("*.RTEF")
            elif(item==self.l3 and self.file_status[1]==True):
                self.mag_2dplot("*.TTEF")
            elif(item==self.l4 and self.file_status[1]==True):
                self.phase_2dplot("*.TTEF")
            elif(item==self.l6 and self.file_status[2]==True):
                self.plot_3d()
            else:
                
                self.central_widget()
                item.setSelected(False)
                self.No_data(item)
                item.setSelected(False)
                
                
                
   
    
    #FUNCTION FOR PLOTTING MAGNITUDE PLOT OF .TTEF AND .RTEF FILES
    def mag_2dplot(self,ext):
        if(ext=="*.RTEF"):
            x=self.x1
            y=self.y1
        else:
            x=self.x2
            y=self.y2
        ex=Canvas()
        ex.axes.plot(x,y)
        ex.axes.set_xlabel('Frequency')
        ex.axes.set_ylabel('Magnitude')
        if(ext=="*.RTEF"):
            ex.axes.set_title('TE REFLECTION')
        elif(ext=="*.TTEF"):
            ex.axes.set_title('TE TRANSMISSION')
        toolbar = NavigationToolbar(ex,self)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(ex)
        layout.addWidget(toolbar)
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
            
   
     #FUNCTION FOR PLOTTING PHASE PLOT OF .TTEF AND .RTEF FILES 
    def phase_2dplot(self,ext):
        if(ext=="*.RTEF"):
            x=self.x1
            z=self.z1
        else:
            x=self.x2
            z=self.z2
        ex=Canvas()
        ex.axes.plot(x,z)
        ex.axes.set_xlabel('Frequency')
        ex.axes.set_ylabel('Phase')
        if(ext=="*.RTEF"):
            ex.axes.set_title('TE REFLECTION')
        elif(ext=="*.TTEF"):
            ex.axes.set_title('TE TRANSMISSION')
        toolbar = NavigationToolbar(ex,self)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(ex)
        layout.addWidget(toolbar)
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
     
    #FUNCTION FOR PLOTTING 3D PLOT OF .3DCTE FILE
    def plot_3d(self):
     
                
        if(True):

            self.f1=list(set(self.f3))
            self.g1=list(set(self.g3))
            self.f1.sort()
            self.g1.sort()
            self.frequency=self.f1[0]
            self.gz=self.g1[0]
            self.frq = QComboBox(self)
            self.frq.resize(30,30)
            for f in self.f1:
                self.frq.addItem(str(f))
            self.gg = QComboBox(self)
            self.gg.resize(30,30)
            for g_v in self.g1:
                self.gg.addItem(str(g_v))
            self.push=QPushButton("PLOT")
            self.frq.currentIndexChanged.connect(self.indexChanged1)
            self.gg.currentIndexChanged.connect(self.indexChanged2)
            layout=QHBoxLayout()
            layout.setSpacing(40)
            layout.addStretch(2)
            layout.addWidget(QLabel('Frequency:'))
            layout.addWidget(self.frq)
            layout.addWidget(QLabel('Value of Z:'))
            layout.addWidget(self.gg)
            layout.addWidget(self.push)
            layout.setContentsMargins(300,0,300,0)
            widget = QtWidgets.QWidget()
            widget.setLayout(layout)
            widget.setContentsMargins(0,0,0,0)
           
            #self.setCentralWidget(widget)
           
          

            
                # Create a placeholder widget to hold our toolbar and canvas.
           
            self.push.clicked.connect(lambda:self.update_3d(widget))
            self.update_3d(widget)
            
    def central_widget(self):
        self.centralwidget = QtWidgets.QWidget(self) 
        self.centralwidget.setObjectName("centralwidget") 
        self.setCentralWidget(self.centralwidget) 
            
    
     
    #UPDATES FREQUENCY USING FREQUENCY COMBOBOX
    def indexChanged1(self, index):
        
        data=self.f1[index]
    
        if(data is not None):
            self.frequency = float(data)
            
    #UPDATES Z-VALUE USING Z COMBOBOX
    def indexChanged2(self, index):
        print(index)
        data = self.g1[index]
        print(data)
        if(data is not None):
            self.gz=float(data)
            
            
    #UPDATES THE 3D PLOT 
    def update_3d(self,widget):
        layout=QVBoxLayout()
        layout.setSpacing(0)
        layout.addStretch(0)
        layout.addWidget(widget)
        st=-1
        en=-1
        
        for j in range(0,len(self.f3)):
            if(self.f3[j]==self.frequency and st==-1 and self.g3[j]==self.gz):
                st=j
            elif(st!=-1 and (self.f3[j]!=self.frequency or self.g3[j]!=self.gz)):
                en=j-1
                break
        if(en==-1):
            en=j
     
        x1 = np.asarray(self.x3[st:en+1])# value at x from t6.3DCTE
        y1 = np.asarray(self.y3[st:en+1])# value at y from t6.3DCTE
        fnp=np.asarray(self.z3[st:en+1])# value at x and y from t6.3DCTE
        xx=x1.reshape(64,64)
        yy=y1.reshape(64,64)
        fnp=fnp.reshape(64,64)
        self.ex=Canvas(None,6,4,100,'3d')

        self.ex.axes.set_xlabel('X')
        self.ex.axes.set_ylabel('Y')
        self.ex.axes.set_title('Contour Plot')
        cp=self.ex.axes.contourf(xx,yy,fnp,cmap='viridis')
        cb=plt.colorbar(cp,orientation='vertical')
        
        toolbar = NavigationToolbar(self.ex, self)
        
        layout.addWidget(toolbar)
        layout.addWidget(self.ex)
        layout.setContentsMargins(0,10,0,10)
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        widget.setContentsMargins(0,0,0,20)
        self.setCentralWidget(widget)     
        #plt.show()
    # OPENS FOLDER DIALOG
    def open_folder(self):
       
        dir_ = QFileDialog.getExistingDirectory(None, 'Select a folder:', self.folder, QFileDialog.ShowDirsOnly)
    
        if(dir_!=''):
            self.folder=dir_
            self.d.update_docket(self,dir_)
            
    def info(self):
        msg=QMessageBox()
        msg.about(self,"ABOUT DISPLAY","ABOUT AADISPLAY\n\nDEVELOPED BY: Akash Goyal(NIT DELHI)\n\nGUIDED BY:Dr.Ravi Kumar Arya")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        
    def No_data(self,item):
        item.setSelected(False)
        msg=QMessageBox()
        msg.about(self,"NO DATA","There is no data available for this function.")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.buttonClicked.connect(lambda:self.popup_button(item))
        
        
    def popup_button(self,item):
        item.setSelected(False)
        
       
        
    def helps(self):
        msg=QMessageBox()
        msg.about(self, "Information", "How to use:\n1.Click on the File button on Menubar and choose Open."
                  "\n\n2.Choose the folder having .TTEF , .RTEF and .3DCTE files.\n\n3.Choose the required plot from left side of the window.")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Ok)
        
        
    def initUI(self):               
        self.folder=os.getcwd()
        lis=False
        try:
            lis=os.listdir(os.getcwd()+"\\AA.info")
        except:
            os.mkdir(os.getcwd()+"\\AA.info")
        
        
        try:
            f=open(os.getcwd()+"\\AA.info\\folder.txt",'r')
            self.folder=f.readlines()[0]
            f.close()
        except:
            f=open(os.getcwd()+"\\AA.info\\folder.txt",'a')
            f.write(os.getcwd())
            f.close()
                    
                
        
        
        
        
        
        
        
     
        self.centralwidget = QtWidgets.QWidget(self) 
        #Functions for Menubar
        exitAct = QAction('Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(self.exitapp)
        exitAct.setIcon(QIcon('icons\\Exit.png'))
        
        openAct=QAction('Open',self)
        openAct.triggered.connect(self.open_folder)
        openAct.setStatusTip('Open Folder')
        openAct.setShortcut('Ctrl+N')
        openAct.setIcon(QIcon('icons\\Folder.png'))
        
        helpAct=QAction('Help',self)
        helpAct.setStatusTip('Get Help')
        helpAct.setIcon(QIcon('icons\\Help.png'))
        helpAct.triggered.connect(self.helps)
        
        aboutAct=QAction('About',self)
        aboutAct.setStatusTip('About AADISPLAY')
        aboutAct.setIcon(QIcon('icons\\info.png'))
        aboutAct.triggered.connect(self.info)
        #Menubar for window
        menubar = self.menuBar()
    
        file = menubar.addMenu('&File')
        file.addAction(openAct)
        file.addAction(exitAct)
        
        help1=menubar.addMenu('&Help')
        help1.addAction(helpAct)
        help1.addAction(aboutAct)
        self.statusBar()
        
        
        toolbar=QToolBar()
        self.addToolBar(toolbar)
        
        layout = QHBoxLayout()
        layout.setSpacing(10)
        
        #toolbar button 1
        self.toolButton = QtWidgets.QToolButton(self.centralwidget) 

        icon = QIcon() 
        self.toolButton.setIconSize(QSize(15,15))
        icon.addPixmap(QtGui.QPixmap("icons\\Folder.png"),QtGui.QIcon.Normal, QtGui.QIcon.Off) 
        self.toolButton.setIcon(icon) 
        self.toolButton.setStatusTip("Open Folder")
        self.toolButton.clicked.connect(self.open_folder) 
        
        layout.addWidget(self.toolButton)
        
          #toolbar button 2
        self.toolButton = QtWidgets.QToolButton(self.centralwidget) 

        icon = QIcon() 
        self.toolButton.setIconSize(QSize(15,15))
        icon.addPixmap(QtGui.QPixmap("icons\\Help.png"),QtGui.QIcon.Normal, QtGui.QIcon.Off) 
        self.toolButton.setIcon(icon) 
        self.toolButton.setStatusTip("Help")
        self.toolButton.clicked.connect(self.helps) 
        
        layout.addWidget(self.toolButton)
       
        #toolbar button 3
        self.toolButton = QtWidgets.QToolButton(self.centralwidget) 

        icon = QIcon() 
        self.toolButton.setIconSize(QSize(15,15))
        icon.addPixmap(QtGui.QPixmap("icons\\info.png"),QtGui.QIcon.Normal, QtGui.QIcon.Off) 
        self.toolButton.setIcon(icon) 
        self.toolButton.setStatusTip("Information")
        self.toolButton.clicked.connect(self.info) 
        
        layout.addWidget(self.toolButton)
        
        
      
        
        #adding the toolbuttons to toolbar
        widget = QWidget()
        widget.setLayout(layout)
        widget.setContentsMargins(5,0,5,0)
        toolbar.addWidget(widget)
    
        
       
        self.central_widget()
        
        
        QtCore.QMetaObject.connectSlotsByName(self) 
        self.file_status=[False]*3
        
        self.setGeometry(600, 600, 350, 250)
        self.setWindowTitle('AADISPLAY')
        self.setWindowIcon(QIcon('icons\\eye.png'))
        self.d=DockDialog(self,self.folder)
        
        self.show()

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    print(width,height)
    ex = Example()
    sys.exit(app.exec_())

