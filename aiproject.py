import sys
import os
import cv2 as cv
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from tkinter import messagebox
from tkinter import Tk
from PIL import Image as im
root= Tk()
root.withdraw()

pre_picture_path = []
add_picture_path = []
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(
        os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form1 = resource_path('Main.ui')
form1, base1 = uic.loadUiType(form1)

class MainWindow(base1, form1):
    def __init__(self): # 버튼 인식하는 부분
        try:
            super(base1, self).__init__()
            # loadUi("Main.ui",self)
            self.setupUi(self)
            self.radioButton_color.setChecked(True)
            self.pushButton_filepath.clicked.connect(self.filepath)
            self.pushButton_filepath_add.clicked.connect(self.filepath_add)
            self.pushButton_exit.clicked.connect(self.logout)
            self.pushButton_histogram.clicked.connect(self.histogram)
            self.pushButton_gaussianBlur.clicked.connect(self.gaussianBlur)
            self.pushButton_smooth.clicked.connect(self.smooth)
            self.pushButton_unsharp.clicked.connect(self.unsharp)
            self.pushButton_PixelBlending.clicked.connect(self.combination)
        except Exception as e:
            messagebox.showinfo("예외가 발생했습니다", e)
    def filesave(self,output_img):
        try:
            global after_picture_path
            if self.radioButton_gray.isChecked()==True:
                output_img = cv.cvtColor(output_img, cv.COLOR_BGR2GRAY)
            data = im.fromarray(output_img)
            newfilename=pre_picture_path[0].split('.')
            newfilename[1]
            data.save(newfilename[0]+"_change."+newfilename[1])
            self.picture_after.setPixmap(QPixmap(newfilename[0]+"_change."+newfilename[1]))
            after_picture_path=newfilename[0]+"_change."+newfilename[1]
            print(after_picture_path)
        except Exception as e:
            messagebox.showinfo("예외가 발생했습니다", e)

    def filepath(self): # 파일 경로 지정하는 부분(파일 탐색기)
        try:
            global pre_picture_path
            pre_picture_path=QFileDialog.getOpenFileName(self,'','','Picture(*.png *.jpg *.jpeg);;All File(*)')        
            self.lineEdit_filepath.setText(pre_picture_path[0])
            self.picture_pre.setPixmap(QPixmap(pre_picture_path[0]))
        except Exception as e:
            messagebox.showinfo("예외가 발생했습니다", e)
    
    def filepath_add(self): # 파일 경로 지정하는 부분(파일 탐색기)
        try:
            global add_picture_path
            add_picture_path=QFileDialog.getOpenFileName(self,'','','Picture(*.png *.jpg *.jpeg);;All File(*)')        
            self.lineEdit_filepath_add.setText(add_picture_path[0])
            self.picture_add.setPixmap(QPixmap(add_picture_path[0]))
        except Exception as e:
            messagebox.showinfo("예외가 발생했습니다", e)
    def histogram(self):
        try:
            global pre_picture_path
            print(pre_picture_path[0])
            img=cv.imread(pre_picture_path[0])
            img_ycrcb= cv.cvtColor(img, cv.COLOR_BGR2RGB)
            # YCrCb 컬러 형태로 변환합니다.
            yCrCb = cv.cvtColor(img_ycrcb, cv.COLOR_BGR2YCrCb)
            # y, Cr, Cb로 컬러 영상을 분리 합니다.
            y, Cr, Cb = cv.split(yCrCb)
            # y값을 히스토그램 평활화를 합니다.
            equalizedY = cv.equalizeHist(y)
            # equalizedY, Cr, Cb를 합쳐서 새로운 yCrCb 이미지를 만듭니다.
            yCrCb2 = cv.merge([equalizedY, Cr, Cb])
            # 마지막으로 yCrCb2를 다시 BGR 형태로 변경합니다.
            yCrCbDst = cv.cvtColor(yCrCb2, cv.COLOR_YCrCb2BGR)
            self.filesave(yCrCbDst) # 파일 저장 및 출력
        except Exception as e:
            messagebox.showinfo("예외가 발생했습니다", e)

    def gaussianBlur(self): # 가우시안 필터링 버튼 구동 하는 부분
        try:
            global pre_picture_path
            print(pre_picture_path[0])
            img=cv.imread(pre_picture_path[0])
            img_ycrcb= cv.cvtColor(img, cv.COLOR_BGR2RGB)
            # YCrCb 컬러 형태로 변환합니다.
            yCrCb = cv.cvtColor(img_ycrcb, cv.COLOR_BGR2YCrCb)
            # y, Cr, Cb로 컬러 영상을 분리 합니다.
            y, Cr, Cb = cv.split(yCrCb)
            # y값을 가우시안 필터링을 합니다.
            equalizedY = cv.GaussianBlur(y,(5,5),0)
            # equalizedY, Cr, Cb를 합쳐서 새로운 yCrCb 이미지를 만듭니다.
            yCrCb2 = cv.merge([equalizedY, Cr, Cb])
            # 마지막으로 yCrCb2를 다시 BGR 형태로 변경합니다.
            yCrCbDst = cv.cvtColor(yCrCb2, cv.COLOR_YCrCb2BGR)
            self.filesave(yCrCbDst) # 파일 저장 및 출력
        
        except Exception as e:
            messagebox.showinfo("예외가 발생했습니다", e)
    
    def smooth(self):
        try:
            global pre_picture_path
            print(pre_picture_path[0])
            img=cv.imread(pre_picture_path[0])
            img_ycrcb= cv.cvtColor(img, cv.COLOR_BGR2RGB)
            # YCrCb 컬러 형태로 변환합니다.
            yCrCb = cv.cvtColor(img_ycrcb, cv.COLOR_BGR2YCrCb)
            # y, Cr, Cb로 컬러 영상을 분리 합니다.
            y, Cr, Cb = cv.split(yCrCb)
            # y값을 보존 스무딩를 합니다.
            smoothing_mask = np.array([[1/16, 1/8, 1/16], [1/8, 1/4, 1/8], [1/16, 1/8, 1/16]])
            smoothing_out = cv.filter2D(y, -1, smoothing_mask)

            # equalizedY, Cr, Cb를 합쳐서 새로운 yCrCb 이미지를 만듭니다.
            yCrCb2 = cv.merge([smoothing_out, Cr, Cb])
            # 마지막으로 yCrCb2를 다시 BGR 형태로 변경합니다.
            yCrCbDst = cv.cvtColor(yCrCb2, cv.COLOR_YCrCb2BGR)
            self.filesave(yCrCbDst) # 파일 저장 및 출력
        except Exception as e:
            messagebox.showinfo("예외가 발생했습니다", e)

    def unsharp(self):
        try:
            global pre_picture_path
            print(pre_picture_path[0])
            img=cv.imread(pre_picture_path[0])
            img_ycrcb= cv.cvtColor(img, cv.COLOR_BGR2RGB)
            # YCrCb 컬러 형태로 변환합니다.
            yCrCb = cv.cvtColor(img_ycrcb, cv.COLOR_BGR2YCrCb)
            # y, Cr, Cb로 컬러 영상을 분리 합니다.
            y, Cr, Cb = cv.split(yCrCb)
            # y값을 보존 스무딩를 합니다.
            mean_img=cv.blur(y,(5,5))
            edge_img=cv.addWeighted(y, 1.0, mean_img,-1.0, 0)
            equalizedY=cv.addWeighted(y, 1.0, edge_img, 3.0, 0)
            # equalizedY, Cr, Cb를 합쳐서 새로운 yCrCb 이미지를 만듭니다.
            yCrCb2 = cv.merge([equalizedY, Cr, Cb])
            # 마지막으로 yCrCb2를 다시 BGR 형태로 변경합니다.
            yCrCbDst = cv.cvtColor(yCrCb2, cv.COLOR_YCrCb2BGR)
            self.filesave(yCrCbDst) # 파일 저장 및 출력
        except Exception as e:
            messagebox.showinfo("예외가 발생했습니다", e)


    def combination(self):
        try:
            global pre_picture_path
            global add_picture_path
            img1 = cv.imread(pre_picture_path[0])
            img2 = cv.imread(add_picture_path[0])
            # BGR채널순서를 RGB채널로 변경
            RGB_img1 = cv.cvtColor(img1, cv.COLOR_BGR2RGB) 
            RGB_img2 = cv.cvtColor(img2, cv.COLOR_BGR2RGB)
            output_img = cv.cvtColor(img1,cv.COLOR_BGR2RGB) 
            # RGB 채널 나누기
            R_img1,G_img1,B_img1=cv.split(RGB_img1)
            R_img2,G_img2,B_img2=cv.split(RGB_img2)
            # 출력 array 생성하고 0으로 초기화, unsigned byte (0~255)로 설정
            R_plus=np.zeros((RGB_img1.shape[0],RGB_img1.shape[1]),dtype=np.ubyte)
            G_plus=np.zeros((RGB_img1.shape[0],RGB_img1.shape[1]),dtype=np.ubyte)
            B_plus=np.zeros((RGB_img1.shape[0],RGB_img1.shape[1]),dtype=np.ubyte)
            def saturation(value): #saturation함수로 정의하기
                if(value>255):
                    value = 255
                return value 
            W=self.doubleSpinBox_W.value()   #가중치 설정
            #for문을 돌며 픽셀 블렌딩 연산 하기
            for h in range(RGB_img1.shape[0]):
                for w in range(RGB_img1.shape[1]):
                    R_plus[h,w] = saturation(np.fabs(W*np.float32(R_img1[h,w])+(1-W)*np.float32(R_img2[h,w]))) 
                    G_plus[h,w] = saturation(np.fabs(W*np.float32(G_img1[h,w])+(1-W)*np.float32(G_img2[h,w]))) 
                    B_plus[h,w] = saturation(np.fabs(W*np.float32(B_img1[h,w])+(1-W)*np.float32(B_img2[h,w]))) 
            output_img[:,:,0]=R_plus
            output_img[:,:,1]=G_plus
            output_img[:,:,2]=B_plus
            self.filesave(output_img) # 파일 저장 및 출력
        except Exception as e:
            messagebox.showinfo("예외가 발생했습니다", e)
    def logout(self): # 종료버튼 동작 구동 하는 부분
        exit()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    widget = QtWidgets.QStackedWidget()
    widget.setFixedWidth(800)
    widget.setFixedHeight(455)
    widget.addWidget(win)
    widget.show()
    app.exec_()
