# -*- coding: utf-8 -*-

"""
Module implementing mainWin.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox

from Ui_windows import Ui_MainWindow
from Ui_newWin import Ui_Dialog
from arithmetic import *


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
        self.EzSteg = EzSteg()
        self.BWM = BlindWaterMark()
        self.attachFile = attachFile()
    
    @pyqtSlot()
    def on_LSB_pushButton_clicked(self):
        """
        ‘LSB隐写’按钮点击事件响应函数
        """
        filename, _ = QFileDialog.getOpenFileName(self, '请选择BMP文件', '', 'BMP文件(*.bmp)')
        info_ = [0,1,0,1,1,0,1,0]
        self.LSB.load_bmp(filename)
        self.LSB.write(info_)
        filename, _ = QFileDialog.getSaveFileName(self, '请选择保存路径', '', 'BMP文件(*.bmp)')
        self.LSB.save(filename)
        
    
    @pyqtSlot()
    def on_JsteG_pushButton_clicked(self):
        """
        ‘JsteG隐写’按钮点击事件响应函数
        """
        filename, _ = QFileDialog.getOpenFileName(self, '请选择JPG文件', '', 'JPG文件(*.jpg)')
        dctInt, img = self.Jsteg.get_dct(filename)
        dctShape = dctInt.shape
        dctInt = dctInt.reshape((-1))
        self.Jsteg.set_sequence_after_dct(dctInt)
        info_ = [0,1,0,1,1,0,1,0]
        self.Jsteg.write(info_)
        
        dctInfo = self.Jsteg.get_sequence_after_dct()
        dctInfo = np.float32(dctInfo.reshape(dctShape))
        img[:, :, 0] = cv2.idct(dctInfo)
        
        filename, _ = QFileDialog.getSaveFileName(self, '请选择保存路径', '', 'JPG文件(*.jpg)')
        cv2.imwrite(filename, img)
        
        
    
    @pyqtSlot()
    def on_F3_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_F5_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_Ezsetgo_pushButton_clicked(self):
        """
        EzSteg 按钮响应函数
        """
        filename, _ = QFileDialog.getOpenFileName(self, '请选择BMP文件', '', 'BMP文件(*.bmp)')
        info_ = [0,1,0,1,1,0,1,0]
        self.EzSteg = EzSteg()
        
        
    
    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        LSB解析按钮响应函数
        """
        filename, _ = QFileDialog.getOpenFileName(self, '请选择BMP文件', '', 'BMP文件(*.bmp)')
        self.LSB.load_bmp(filename)
        info_ = self.LSB.read()
        info_ = [str(i) for i in info_]
        QMessageBox.information(self,"Information", str(info_))
    
    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        ‘JsteG解析’按钮点击事件响应函数
        """
        filename, _ = QFileDialog.getOpenFileName(self, '请选择JPG文件', '', 'JPG文件(*.jpg)')
        dctInt, _ = self.Jsteg.get_dct(filename)
        dctInt = dctInt.reshape((-1))
        self.Jsteg.set_sequence_after_dct(dctInt)
        info_ = self.Jsteg.read()
        info_ = [str(i) for i in info_]
        QMessageBox.information(self,"Information", str(info_))
    
    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_pushButton_5_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_pushButton_6_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
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
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_pushButton_9_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError


if __name__ == "__main__":
    import sys
   # print('hello')
    app = QApplication(sys.argv)
    ui = mainWin()
    ui.show()
    sys.exit(app.exec_())

