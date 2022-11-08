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
after_picture_path = []
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
            self.comboBox_chk.currentTextChanged.connect(self.comb)
            self.pushButton_trans.clicked.connect(self.trans)
        except Exception as e:
            messagebox.showinfo("예외가 발생했습니다", e)
    
    def comb(self):
        if self.comboBox_chk.currentText()=="산술 및 논리 연산":
            self.pushButton_histogram.setText("픽셀 AND")
            self.pushButton_gaussianBlur.setText("픽셀 OR")
            self.pushButton_smooth.setText("픽셀 반전")
            self.pushButton_unsharp.setText("픽셀 마스크")
            self.pushButton_PixelBlending.setText("픽셀 결합")
        
        elif self.comboBox_chk.currentText()=="화질 향상 기법":
            self.pushButton_histogram.setText("히스토그램 평활화")
            self.pushButton_gaussianBlur.setText("가우시안 필터링")
            self.pushButton_smooth.setText("보존 스무딩")
            self.pushButton_unsharp.setText("언샤프 필터링")
            self.pushButton_PixelBlending.setText("중간값 필터링")

        elif self.comboBox_chk.currentText()=="영상 특징 검출":
            self.pushButton_histogram.setText("로버트 크로스 에지")
            self.pushButton_gaussianBlur.setText("소벨 에지")
            self.pushButton_smooth.setText("프르윗 에지")
            self.pushButton_unsharp.setText("캐니 에지")
            self.pushButton_PixelBlending.setText("가우시안-라플라시안")
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
            self.lineEdit_fin_path.setText(after_picture_path)
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
    def trans(self):
        try:
            global after_picture_path
            img = cv.imread(after_picture_path)
            rows,cols = img.shape[:2]
            # 회전점을 영상 모서리 -> 영상의 중심으로 변경
            W=self.doubleSpinBox_trans.value()   #가중치 설정
            M = cv.getRotationMatrix2D(((cols-1)/2.0,(rows-1)/2.0),W,1)
            output_img = cv.warpAffine(img,M,(cols*1,rows*1),flags = cv.INTER_LINEAR)
            output_img= cv.cvtColor(output_img,cv.COLOR_RGB2BGR)
            self.filesave(output_img) # 파일 저장 및 출력
        except Exception as e:
            messagebox.showinfo("예외가 발생했습니다", e)
    def histogram(self): # 히스토그램 평활화
        try:
            global pre_picture_path
            global add_picture_path
            if self.comboBox_chk.currentText()=="산술 및 논리 연산": # AND연산
                img1 = cv.imread(pre_picture_path[0])
                img2 = cv.imread(add_picture_path[0])
                # BGR채널순서를 RGB채널로 변경
                RGB_img1 = cv.cvtColor(img1, cv.COLOR_BGR2RGB) 
                RGB_img2 = cv.cvtColor(img2, cv.COLOR_BGR2RGB)
                output_img = cv.cvtColor(img1,cv.COLOR_BGR2RGB) 
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

                #영상 이진화 하기
                for h in range(RGB_img1.shape[0]):
                    for w in range(RGB_img1.shape[1]):
                        if(np.int32(R_img1[h,w])>180):
                            R_img1[h,w]=G_img1[h,w]=B_img1[h,w]=255
                        else:
                            R_img1[h,w]=G_img1[h,w]=B_img1[h,w]=0
                        if(np.int32(G_img2[h,w])>50):
                            R_img2[h,w]=G_img2[h,w]=B_img2[h,w]=255
                        else:
                            R_img2[h,w]=G_img2[h,w]=B_img2[h,w]=0 

                #for문을 돌며 픽셀 비트 AND 연산 하기
                for h in range(RGB_img1.shape[0]):
                    for w in range(RGB_img1.shape[1]):
                        R_plus[h,w] = saturation(np.int32(R_img1[h,w])& np.int32(R_img2[h,w])) 
                        G_plus[h,w] = saturation(np.int32(G_img1[h,w])& np.int32(G_img2[h,w])) 
                        B_plus[h,w] = saturation(np.int32(B_img1[h,w])& np.int32(B_img2[h,w]))
                output_img[:,:,0]=R_plus
                output_img[:,:,1]=G_plus
                output_img[:,:,2]=B_plus
                self.filesave(output_img) # 파일 저장 및 출력

            elif self.comboBox_chk.currentText()=="화질 향상 기법":
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
            elif self.comboBox_chk.currentText()=="영상 특징 검출":
                print(pre_picture_path[0])
                img=cv.imread(pre_picture_path[0])
                # color영상을 gray영상으로 만들기
                gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

                # 로버트 크로스 필터
                gx = np.array([[-1, 0], [0, 1]], dtype=int)
                gy = np.array([[0, -1], [1, 0]], dtype=int)

                # 로버트 크로스 컨벌루션
                x = cv.filter2D(gray_img, -1, gx)
                y = cv.filter2D(gray_img, -1, gy)

                # 절대값 취하기
                absX = cv.convertScaleAbs(x)
                absY = cv.convertScaleAbs(y)
                output_img = cv.addWeighted(absX, 0.5, absY, 0.5, 0)
                self.filesave(output_img) # 파일 저장 및 출력
        except Exception as e:
            messagebox.showinfo("예외가 발생했습니다", e)

    def gaussianBlur(self): # 가우시안 필터링 버튼 구동 하는 부분
        try:
            global pre_picture_path
            global add_picture_path
            if self.comboBox_chk.currentText()=="산술 및 논리 연산": # OR연산
                img1 = cv.imread(pre_picture_path[0])
                img2 = cv.imread(add_picture_path[0])
                # BGR채널순서를 RGB채널로 변경
                RGB_img1 = cv.cvtColor(img1, cv.COLOR_BGR2RGB) 
                RGB_img2 = cv.cvtColor(img2, cv.COLOR_BGR2RGB)
                output_img = cv.cvtColor(img1,cv.COLOR_BGR2RGB) 
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

                #영상 이진화 하기
                for h in range(RGB_img1.shape[0]):
                    for w in range(RGB_img1.shape[1]):
                        if(np.int32(R_img1[h,w])>180):
                            R_img1[h,w]=G_img1[h,w]=B_img1[h,w]=255
                        else:
                            R_img1[h,w]=G_img1[h,w]=B_img1[h,w]=0
                        if(np.int32(G_img2[h,w])>50):
                            R_img2[h,w]=G_img2[h,w]=B_img2[h,w]=255
                        else:
                            R_img2[h,w]=G_img2[h,w]=B_img2[h,w]=0 

                #for문을 돌며 픽셀 비트 OR 연산 하기
                for h in range(RGB_img1.shape[0]):
                    for w in range(RGB_img1.shape[1]):
                        R_plus[h,w] = saturation(np.int32(R_img1[h,w])| np.int32(R_img2[h,w])) 
                        G_plus[h,w] = saturation(np.int32(G_img1[h,w])| np.int32(G_img2[h,w])) 
                        B_plus[h,w] = saturation(np.int32(B_img1[h,w])| np.int32(B_img2[h,w]))
                output_img[:,:,0]=R_plus
                output_img[:,:,1]=G_plus
                output_img[:,:,2]=B_plus
                self.filesave(output_img) # 파일 저장 및 출력

            elif self.comboBox_chk.currentText()=="화질 향상 기법":
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

            elif self.comboBox_chk.currentText()=="영상 특징 검출":
                print(pre_picture_path[0])
                img=cv.imread(pre_picture_path[0])
                # color영상을 gray영상으로 만들기
                gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

                # Sobel operator
                x = cv.Sobel(gray_img, -1, 1, 0)
                y = cv.Sobel(gray_img, -1, 0, 1)

                # Turn uint8, image fusion
                absX = cv.convertScaleAbs(x)
                absY = cv.convertScaleAbs(y)
                output_img = cv.addWeighted(absX, 0.5, absY, 0.5, 0)
                self.filesave(output_img) # 파일 저장 및 출력
        except Exception as e:
            messagebox.showinfo("예외가 발생했습니다", e)
    
    def smooth(self): # 보존 스무딩
        try:
            global pre_picture_path
            global add_picture_path
            if self.comboBox_chk.currentText()=="산술 및 논리 연산": # 픽셀 반전 연산
                img1 = cv.imread(pre_picture_path[0])
                # BGR채널순서를 RGB채널로 변경
                RGB_img1 = cv.cvtColor(img1, cv.COLOR_BGR2RGB) 
                output_img = cv.cvtColor(img1,cv.COLOR_BGR2RGB) 
                # RGB 채널 나누기
                R_img1,G_img1,B_img1=cv.split(RGB_img1)
                # 출력 array 생성하고 0으로 초기화, unsigned byte (0~255)로 설정
                R_plus=np.zeros((RGB_img1.shape[0],RGB_img1.shape[1]),dtype=np.ubyte)
                G_plus=np.zeros((RGB_img1.shape[0],RGB_img1.shape[1]),dtype=np.ubyte)
                B_plus=np.zeros((RGB_img1.shape[0],RGB_img1.shape[1]),dtype=np.ubyte)
                def saturation(value): #saturation함수로 정의하기
                    if(value>255):
                        value = 255
                    return value 
                #for문을 돌며 픽셀 반전 연산 하기
                for h in range(RGB_img1.shape[0]):
                    for w in range(RGB_img1.shape[1]):
                        R_plus[h,w] = saturation(255-np.int32(R_img1[h,w])) 
                        G_plus[h,w] = saturation(255-np.int32(G_img1[h,w])) 
                        B_plus[h,w] = saturation(255-np.int32(B_img1[h,w]))
                #영상 다시 넣어주기  
                RGB_img1[:,:,0] = R_img1
                RGB_img1[:,:,1] = G_img1
                RGB_img1[:,:,2] = B_img1  
                output_img[:,:,0]=R_plus
                output_img[:,:,1]=G_plus
                output_img[:,:,2]=B_plus
                self.filesave(output_img) # 파일 저장 및 출력
            
            elif self.comboBox_chk.currentText()=="화질 향상 기법":
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
            elif self.comboBox_chk.currentText()=="영상 특징 검출":
                print(pre_picture_path[0])
                img=cv.imread(pre_picture_path[0])
                # color영상을 gray영상으로 만들기
                gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

                # 프르윗 필터
                gx = np.array([[-1,0,1],[-1,0,1],[-1,0,1]],dtype=int)
                gy = np.array([[1,1,1],[0,0,0],[-1,-1,-1]],dtype=int)
                # 프르윗 필터 컨벌루션
                x = cv.filter2D(gray_img, -1, gx)
                y = cv.filter2D(gray_img, -1, gy)
                # uint8 타입(0~255)로 변경하고 영상 합하기
                absX = cv.convertScaleAbs(x)
                absY = cv.convertScaleAbs(y)
                output_img = cv.addWeighted(absX, 0.5, absY, 0.5, 0)
                self.filesave(output_img) # 파일 저장 및 출력
        except Exception as e:
            messagebox.showinfo("예외가 발생했습니다", e)

    def unsharp(self): # 언샤프 필터링
        try:
            global pre_picture_path
            global add_picture_path
            if self.comboBox_chk.currentText()=="산술 및 논리 연산": # 산술 연산의 응용(MASK)
                img1 = cv.imread(pre_picture_path[0])
                img2 = cv.imread(add_picture_path[0])
                # BGR채널순서를 RGB채널로 변경
                RGB_img1 = cv.cvtColor(img1, cv.COLOR_BGR2RGB) 
                RGB_img2 = cv.cvtColor(img2, cv.COLOR_BGR2RGB)
                output_img = cv.cvtColor(img1,cv.COLOR_BGR2RGB) 
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

                #1) 영상 임계값 적용 하기
                for h in range(RGB_img2.shape[0]):
                    for w in range(RGB_img2.shape[1]):
                        if(np.int32(R_img2[h,w])<=0):
                            R_img2[h,w]=G_img2[h,w]=B_img2[h,w]=255
                        else:
                            R_img2[h,w]=G_img2[h,w]=B_img2[h,w]=0

                #2) 원 영상과 AND 비트 연산하기
                for h in range(RGB_img1.shape[0]):
                    for w in range(RGB_img1.shape[1]):
                        R_plus[h,w] = saturation(np.int32(R_img1[h,w]) & np.int32(R_img2[h,w])) 
                        G_plus[h,w] = saturation(np.int32(G_img1[h,w]) & np.int32(G_img2[h,w])) 
                        B_plus[h,w] = saturation(np.int32(B_img1[h,w]) & np.int32(B_img2[h,w]))
                W=self.doubleSpinBox_W.value()   #가중치 설정
                #for문을 돌며 픽셀 블렌딩 연산 하기
                for h in range(RGB_img1.shape[0]):
                    for w in range(RGB_img1.shape[1]):
                        R_plus[h,w] = saturation(W*np.float32(R_img1[h,w]) +(1-W)*np.float32(R_plus[h,w])) 
                        G_plus[h,w] = saturation(W*np.float32(G_img1[h,w]) +(1-W)*np.float32(G_plus[h,w])) 
                        B_plus[h,w] = saturation(W*np.float32(B_img1[h,w]) +(1-W)*np.float32(B_plus[h,w])) 

                output_img[:,:,0]=R_plus
                output_img[:,:,1]=G_plus
                output_img[:,:,2]=B_plus
                self.filesave(output_img) # 파일 저장 및 출력

            elif self.comboBox_chk.currentText()=="화질 향상 기법":
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
            elif self.comboBox_chk.currentText()=="영상 특징 검출":
                print(pre_picture_path[0])
                img=cv.imread(pre_picture_path[0])
                # color영상을 gray영상으로 만들기
                gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

                # 케니 에지 컨벌루션 연산하기
                output_img = cv.Canny(gray_img,100,250)
                self.filesave(output_img) # 파일 저장 및 출력
        except Exception as e:
            messagebox.showinfo("예외가 발생했습니다", e)


    def combination(self): # 픽셀 결합
        try:
            global pre_picture_path
            global add_picture_path
            if self.comboBox_chk.currentText()=="산술 및 논리 연산":
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

            elif self.comboBox_chk.currentText()=="화질 향상 기법":
                print(pre_picture_path[0])
                img=cv.imread(pre_picture_path[0])
                img_ycrcb= cv.cvtColor(img, cv.COLOR_BGR2RGB)
                # YCrCb 컬러 형태로 변환합니다.
                yCrCb = cv.cvtColor(img_ycrcb, cv.COLOR_BGR2YCrCb)
                # y, Cr, Cb로 컬러 영상을 분리 합니다.
                y, Cr, Cb = cv.split(yCrCb)
                # y값을 보존 스무딩를 합니다.
                mean_img=cv.medianBlur(y,5)
                edge_img=cv.addWeighted(y, 1.0, mean_img,-1.0, 0)
                equalizedY=cv.addWeighted(y, 1.0, edge_img, 3.0, 0)
                # equalizedY, Cr, Cb를 합쳐서 새로운 yCrCb 이미지를 만듭니다.
                yCrCb2 = cv.merge([equalizedY, Cr, Cb])
                # 마지막으로 yCrCb2를 다시 BGR 형태로 변경합니다.
                yCrCbDst = cv.cvtColor(yCrCb2, cv.COLOR_YCrCb2BGR)
                self.filesave(yCrCbDst) # 파일 저장 및 출력

            elif self.comboBox_chk.currentText()=="영상 특징 검출":
                print(pre_picture_path[0])
                img=cv.imread(pre_picture_path[0])
                # color영상을 gray영상으로 만들기
                gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

                # Apply Gaussian Blur
                blur = cv.GaussianBlur(gray_img,(3,3),1)

                # 라플라시안 에지 컨벌루션 연산하기
                laplacian = cv.Laplacian(blur,-1,1)
                self.filesave(laplacian) # 파일 저장 및 출력
        except Exception as e:
            messagebox.showinfo("예외가 발생했습니다", e)
    def logout(self): # 종료버튼 동작 구동 하는 부분
        exit()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    widget = QtWidgets.QStackedWidget()
    widget.setFixedWidth(1620)
    widget.setFixedHeight(1040)
    # widget.setFixedWidth(940) small version
    # widget.setFixedHeight(530)
    widget.addWidget(win)
    widget.show()
    app.exec_()
