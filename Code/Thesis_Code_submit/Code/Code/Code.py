# -*- coding:utf-8 -*- 
#图片隐写工程
#@platform: python+pyqt5
#pip install Sip 
#pip install PyQt5-tools
#pip install numpy 
#pip install random
#pip install opencv-python

"""
Module implementing mainWin.
"""
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox,QLineEdit,QInputDialog
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *

from Ui_windows import Ui_MainWindow
import PIL  #pip install Pillow
from PIL import Image,ImageFont,ImageDraw,ImageGrab
import pytesseract #3rdparty install,default in C:\Program Files (x86)\Tesseract-OCR 
#import selenium # pip install selenium
#from selenium import webdriver #if you want to use python OCR install these 

from arithmetic import *
from steganography import *
import numpy
class mainWin(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(mainWin, self).__init__(parent)
        self.setupUi(self)
        
        # 初始化用于隐写的对象
        self.LSB = LSB()
        self.Jsteg = Jsteg()
        self.F3 = F3()
        self.F5 = F5()
        self.EzSteg = EzSteg()
        self.BWM = BlindWaterMark()
        self.attachFile = attachFile()
    
    @pyqtSlot()
    def on_LSB_pushButton_clicked(self):
        """
        ‘LSB隐写’按钮点击事件响应函数
        """
        filename, _ = QFileDialog.getOpenFileName(self, '请选择BMP文件', '../../../../DemoImage/Input', 'BMP文件(*.bmp)')
        imgs = QtGui.QPixmap(filename).scaled(self.label.width(), self.label.height())
        Ui_MainWindow.show(self,imgs)
        text, okPressed = QInputDialog.getText(self, "LSB","Input Data:", QLineEdit.Normal, "")
        QMessageBox.information(self,"LSB写入内容", text)
        filename1, _ = QFileDialog.getSaveFileName(self, '请选择保存路径', '../../../../DemoImage/Output', 'BMP文件(*.bmp)')
        self.LSB.new_write(filename,filename1,text)
        QMessageBox.information(self,"Success","写入成功")
    @pyqtSlot()
    def on_JsteG_pushButton_clicked(self):
        """
        ‘JsteG隐写’按钮点击事件响应函数
        """
        filename, _ = QFileDialog.getOpenFileName(self, '请选择JPG文件', '../../../../DemoImage/Input', 'JPG文件(*.jpg)')
        imgs = QtGui.QPixmap(filename).scaled(self.label.width(), self.label.height())
        Ui_MainWindow.show(self,imgs)
        text, okPressed = QInputDialog.getText(self, "JsteG","Input Data:", QLineEdit.Normal, "")
        filename1, _ = QFileDialog.getSaveFileName(self, '请选择保存路径', '../../../../DemoImage/Output', 'JPG文件(*.jpg)')
        write_new(filename,filename1,text)
        QMessageBox.information(self,"Success","写入成功")
    @pyqtSlot()
    def on_F3_pushButton_clicked(self):
        """
        ‘F3隐写’按钮点击事件响应函数
        """
        filename, _ = QFileDialog.getOpenFileName(self, '请选择JPG文件', '../../../../DemoImage/Input', 'JPG文件(*.jpg)')
        imgs = QtGui.QPixmap(filename).scaled(self.label.width(), self.label.height())
        Ui_MainWindow.show(self,imgs)
        text, okPressed = QInputDialog.getText(self, "F3","Input Data:", QLineEdit.Normal, "")
        QMessageBox.information(self,"F3写入内容", text)
        filename1, _ = QFileDialog.getSaveFileName(self, '请选择保存路径', '../../../../DemoImage/Output', 'JPG文件(*.jpg)')
        self.F3.new_write(filename,filename1,text)
        QMessageBox.information(self,"Success","写入成功")
    
    @pyqtSlot()
    def on_F5_pushButton_clicked(self):
        """
        ‘F5隐写’按钮点击事件响应函数
        """
        filename, _ = QFileDialog.getOpenFileName(self, '请选择JPG文件', '../../../../DemoImage/Input', 'JPG文件(*.jpg)')
        imgs = QtGui.QPixmap(filename).scaled(self.label.width(), self.label.height())
        Ui_MainWindow.show(self,imgs)
        text, okPressed = QInputDialog.getText(self, "F5","Input Data:", QLineEdit.Normal, "")
        QMessageBox.information(self,"F5写入内容", text)
        filename1, _ = QFileDialog.getSaveFileName(self, '请选择保存路径', '../../../../DemoImage/Output', 'JPG文件(*.jpg)')
        self.F5.new_write(filename,filename1,text)
        QMessageBox.information(self,"Success","写入成功")
    
    @pyqtSlot()
    def on_Ezsetgo_pushButton_clicked(self):
        """
        EzSteg 按钮响应函数
        """
        
        filename, _ = QFileDialog.getOpenFileName(self, '请选择文件', '../../../../DemoImage/Input', '图片文件(*.png)')
        imgs = QtGui.QPixmap(filename).scaled(self.label.width(), self.label.height()) #show images in suitable scales 
        Ui_MainWindow.show(self,imgs)
        text, okPressed = QInputDialog.getText(self, "Get text","Input Data:", QLineEdit.Normal, "")
        #print("text is ",text)
        QMessageBox.information(self,"EzSteg写入内容", text)
        new_img = self.EzSteg.new_write(filename,text)
        filename, _ = QFileDialog.getSaveFileName(self, '请选择保存路径', '../../../../DemoImage/Output', '图片文件(*.png)')
        new_img.save(filename)
        QMessageBox.information(self,"Success","写入成功")
       
    @pyqtSlot()
    def on_imgfile_pushButton_clicked(self):
        """
        文件隐藏  按钮响应函数
        """
        
        filename, _ = QFileDialog.getOpenFileName(self, '请选择PNG文件', '../../../../DemoImage/Input', 'PNG文件(*.png)')
        img = Image.open(filename)
        imgs = QtGui.QPixmap(filename).scaled(self.label.width(), self.label.height())
        Ui_MainWindow.show(self,imgs)

        QMessageBox.information(self,"Open file","请打开需要写入的文件") 
        filename1, _ = QFileDialog.getOpenFileName(self, '请选择文件', '../../../../DemoImage/Input', 'Dat文件(*.dat)')
        #text = np.loadtxt(filename1, dtype=bytes).astype(str).tolist()
        text = open(filename1).read()
        #print(text)
        attachimg = self.attachFile.write(img,text)
        filename2, _ = QFileDialog.getSaveFileName(self, '选择保存的路径', '../../../../DemoImage/Output', 'PNG文件(*.png)')
        attachimg.save(filename2,'PNG')
        QMessageBox.information(self,"Success","保存成功")
         
    @pyqtSlot()
    def on_watermark_pushButton_clicked(self):
        """
        watermark 按钮响应函数
        """
        filename, _ = QFileDialog.getOpenFileName(self, '请选择PNG文件', '../../../../DemoImage/Input', 'PNG文件(*.png)')
        imgs = QtGui.QPixmap(filename).scaled(self.label.width(), self.label.height())
        Ui_MainWindow.show(self,imgs)  
        #write
        img = Image.open(filename)
        #self.BWM.load_img(filename)    
        QMessageBox.information(self,"watermark","请选择水印图片")
        filename, _ = QFileDialog.getOpenFileName(self, '请选择水印文件', '../../../../DemoImage/Input',  'PNG文件(*.png)')
        #self.BWM.load_wm(filename)
        mark = Image.open(filename)
        newimg = self.BWM.new_write(img,mark)
        #imgs = self.BWM.write()
        filename, _ = QFileDialog.getSaveFileName(self, '请选择保存路径', '../../../../DemoImage/Output',  'PNG文件(*.png)')
        newimg.save(filename)
        #cv2.imwrite(filename, imgs)
        QMessageBox.information(self,"Success","水印写入成功")
    
    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        LSB解析按钮响应函数
        """
        filename, _ = QFileDialog.getOpenFileName(self, '请选择BMP文件', '../../../../DemoImage/Output', 'BMP文件(*.bmp)')
        #movie = QtGui.QMovie(filename) #load Gif file
        #self.EzSteg.load_gif(filename)
        #Ui_MainWindow.showGif(self,movie)
        text = self.LSB.new_read(filename) 
        QMessageBox.information(self,"解析内容", text)
     
    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        ‘JsteG解析’按钮点击事件响应函数
        """
        filename, _ = QFileDialog.getOpenFileName(self, '请选择JPG文件', '../../../../DemoImage/Output', 'JPG文件(*.jpg)')
        #imgs = QtGui.QPixmap(filename).scaled(self.label.width(), self.label.height())
        #Ui_MainWindow.show(self,imgs)
        text = read_new(filename)        
        QMessageBox.information(self,"解析内容", text)
 
        
    
    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        """
        ‘F3解析’按钮点击事件响应函数
        """
        filename, _ = QFileDialog.getOpenFileName(self, '请选择JPG文件', '../../../../DemoImage/Output', 'JPG文件(*.jpg)')
        text = self.F3.new_read(filename) 
        QMessageBox.information(self,"F3解析内容", text)
    
    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        """
        ‘F5解析’按钮点击事件响应函数
        """
        filename, _ = QFileDialog.getOpenFileName(self, '请选择JPG文件', '../../../../DemoImage/Output', 'JPG文件(*.jpg)')
        text = self.F5.new_read(filename) 
        QMessageBox.information(self,"F5解析内容", text)
    
    @pyqtSlot()
    def on_pushButton_5_clicked(self):
        """
        ‘EzSteg解析’  按钮点击事件响应函数
        """
        filename, _ = QFileDialog.getOpenFileName(self, '请选择PNG文件', '../../../../DemoImage/Output', 'PNG文件(*.png)')
        img = Image.open(filename)
        #movie = QtGui.QMovie(filename) #load Gif file
        #self.EzSteg.load_gif(filename)
        #Ui_MainWindow.showGif(self,movie)
        text = self.EzSteg.new_read(img) 
        print(text)
        QMessageBox.information(self,"解析内容", text)
       
    @pyqtSlot()
    def on_pushButton_6_clicked(self):
        """
       ‘水印解析’  按钮点击事件响应函数
        """
        filename, _ = QFileDialog.getOpenFileName(self, '请选择PNG文件', '../../../../DemoImage/Output', 'PNG文件(*.png)')
        imgs = QtGui.QPixmap(filename).scaled(self.label.width(), self.label.height())
        Ui_MainWindow.show(self,imgs)
        img = Image.open(filename)
        img_wave = self.BWM.new_read(img)
        QMessageBox.information(self,"Success", "解析成功")
        Ui_MainWindow.show(self,img_wave)
    @pyqtSlot()

    def on_pushButton_7_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    

    @pyqtSlot()
    def on_pushButton_8_clicked(self):
        """
       ‘关键字检索’  按钮点击事件响应函数
        """
        filename, _ = QFileDialog.getOpenFileName(self, '请选择解析文件', '../../../../DemoImage/Output', '文件(*)')
        #imgs = QtGui.QPixmap(filename).scaled(self.label.width(), self.label.height())
        #Ui_MainWindow.show(self,imgs)
        #
        text, okPressed = QInputDialog.getText(self, "Key Word","输入检索字:", QLineEdit.Normal, "")
        #img = Image.open(filename)
        formate = filename.split('.')
        print(formate[1])
        if(formate[1]=='bmp'):
            QMessageBox.information(self,"BMP","LSB解析")
            #imgs = QtGui.QPixmap(filename).scaled(self.label.width(), self.label.height()) #show images in suitable scales 
            #Ui_MainWindow.show(self,imgs)
            info_ = self.LSB.new_read(filename) 
            #info_ = self.LSB.read(img)
            QMessageBox.information(self,"解析内容", info_)
            if(info_ == text):
               QMessageBox.warning(self,"Attention", "敏感")
            else:
               QMessageBox.information(self,"Common", "无敏感")
        elif(formate[1]=='jpg'):
            QMessageBox.information(self,"JPEG","JsteG解析")
            #imgs = QtGui.QPixmap(filename).scaled(self.label.width(), self.label.height()) #show images in suitable scales 
            #Ui_MainWindow.show(self,imgs)
            #info_ = self.LSB.read(img)
            info_ = read_new(filename)
            QMessageBox.information(self,"解析内容", info_)
            if(info_ == text):
                QMessageBox.warning(self,"Attention", "敏感")
            else:
                QMessageBox.information(self,"Common", "无敏感")
        elif(formate[1]=='png'):
            QMessageBox.information(self,"PNG","EzSteg解析")
            #imgs = QtGui.QPixmap(filename).scaled(self.label.width(), self.label.height()) #show images in suitable scales 
            #Ui_MainWindow.show(self,imgs)
            #info_ = self.LSB.read(img)
            img = Image.open(filename)
            info_ = self.EzSteg.new_read(img)
            QMessageBox.information(self,"解析内容", info_)
            if(info_ == text):
                QMessageBox.warning(self,"Attention", "敏感")
            else:
                QMessageBox.information(self,"Common", "无敏感")
        else:
            QMessageBox.warning(self,"Attention", "未识别")
        #if you want use this demo, open these code and close code above it.
        #text=pytesseract.image_to_string(Image.open(filename),lang='chi_sim')
        #text=text.replace(" ","") #remove backspace 
        #QMessageBox.information(self,"解析内容", text)
        #url = 'https://www.baidu.com/s?wd=%s' % text #baidu Search 
        #driver = webdriver.Firefox() #Your FireFox  Broswer Dir
        #driver.maximize_window()
        #driver.get(url)
    @pyqtSlot()
    def on_pushButton_9_clicked(self):
        """
       ‘文件隐藏解析’  按钮点击事件响应函数
        """
        filename, _ = QFileDialog.getOpenFileName(self, '请选择PNG文件', '../../../../DemoImage/Output', 'PNG文件(*.png)')
        img = Image.open(filename)
        imgs = QtGui.QPixmap(filename).scaled(self.label.width(), self.label.height())
        Ui_MainWindow.show(self,imgs)
        QMessageBox.information(self,"decode","点击开始解析")
        decodeimg = self.attachFile.read(img).scaled(self.label.width(), self.label.height())
        Ui_MainWindow.show(self,decodeimg)
        QMessageBox.information(self,"Success","检测成功")
   
if __name__ == "__main__":
    import sys
    print("\t\t\t图片隐写解析系统\n运行中...")
    app = QApplication(sys.argv)
    ui = mainWin()
    ui.show()
    sys.exit(app.exec_())

