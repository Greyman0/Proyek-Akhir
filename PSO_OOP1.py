# Inisialisasi Library
import numpy as np
import matplotlib.pyplot as plt
from skimage.color import colorconv
from skimage.io import imread, imshow
from skimage.color import rgb2gray, rgb2hsv
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
import cv2
from math import *

class PSO():
    def __init__(self):
        self.dimensi = 2

    def input_gambar(self, image_path):
        self.image_path = image_path 
        self.img = cv2.imread(self.image_path)
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        # self.img = cv2.resize(self.img, (640,640))
        fig, ax = plt.subplots(figsize=(3,3))
        ax.imshow(self.img)
        return self.img

    def input_partikel(self,partikel=160,ratio_size=np.array([25])):
         # ambil path gambar dan jumlah partikel yang diinginkan
        print('tes threading')
        self.partikel = partikel
        self.ratio_size = ratio_size
# konversi ke integer 
        self.x_pos = np.zeros((self.dimensi, self.partikel), dtype='int32')
        self.x = np.random.randint(0,self.img.shape[1],(self.partikel), dtype='int32')
        self.y = np.random.randint(0,self.img.shape[0],(self.partikel), dtype='int32')

        self.x_pos[0] = self.x
        self.x_pos[1] = self.y


        # inisiasi region 1-4
        self.regX1Y1 = self.x_pos[:,(self.x_pos[0]<self.img.shape[1]/4) * (self.x_pos[1] < self.img.shape[0]/4)] 
        self.regX2Y1 = self.x_pos[:,(self.x_pos[0]>self.img.shape[1]/4) * (self.x_pos[0]<self.img.shape[1]/2) * (self.x_pos[1] < self.img.shape[0]/4)] 
        self.regX3Y1 = self.x_pos[:,(self.x_pos[0]>self.img.shape[1]/2) * (self.x_pos[0]<self.img.shape[1]*3/4) * (self.x_pos[1] < self.img.shape[0]/4)] 
        self.regX4Y1 = self.x_pos[:,(self.x_pos[0]>self.img.shape[1]*3/4) *(self.x_pos[0]<self.img.shape[1]/1) * (self.x_pos[1] < self.img.shape[0]/4)]

        # inisiasi region 5-8
        self.regX1Y2 = self.x_pos[:,(self.x_pos[0]<self.img.shape[1]/4) * (self.x_pos[1] > self.img.shape[0]/4) * (self.x_pos[1] < self.img.shape[0]/2)] 
        self.regX2Y2 = self.x_pos[:,(self.x_pos[0]>self.img.shape[1]/4) * (self.x_pos[0]<self.img.shape[1]/2) * (self.x_pos[1] > self.img.shape[0]/4) * (self.x_pos[1] < self.img.shape[0]/2)] 
        self.regX3Y2 = self.x_pos[:,(self.x_pos[0]>self.img.shape[1]/2) * (self.x_pos[0]<self.img.shape[1]*3/4) * (self.x_pos[1] > self.img.shape[0]/4) * (self.x_pos[1] < self.img.shape[0]/2)] 
        self.regX4Y2 = self.x_pos[:,(self.x_pos[0]>self.img.shape[1]*3/4) *(self.x_pos[0]<self.img.shape[1]/1) * (self.x_pos[1] > self.img.shape[0]/4) * (self.x_pos[1] < self.img.shape[0]/2)]

        # inisiasi region 9-12
        self.regX1Y3 = self.x_pos[:,(self.x_pos[0]<self.img.shape[1]/4) * (self.x_pos[1] > self.img.shape[0]/2) * (self.x_pos[1] < self.img.shape[0]*3/4)] 
        self.regX2Y3 = self.x_pos[:,(self.x_pos[0]>self.img.shape[1]/4) * (self.x_pos[0]<self.img.shape[1]/2) * (self.x_pos[1] > self.img.shape[0]/2) * (self.x_pos[1] < self.img.shape[0]*3/4)] 
        self.regX3Y3 = self.x_pos[:,(self.x_pos[0]>self.img.shape[1]/2) * (self.x_pos[0]<self.img.shape[1]*3/4) * (self.x_pos[1] > self.img.shape[0]/2) * (self.x_pos[1] < self.img.shape[0]*3/4)] 
        self.regX4Y3 = self.x_pos[:,(self.x_pos[0]>self.img.shape[1]*3/4) *(self.x_pos[0]<self.img.shape[1]/1) * (self.x_pos[1] > self.img.shape[0]/2) * (self.x_pos[1] < self.img.shape[0]*3/4)]

        # inisiasi region 13-16
        self.regX1Y4 = self.x_pos[:,(self.x_pos[0]<self.img.shape[1]/4) * (self.x_pos[1] > self.img.shape[0]*3/4) * (self.x_pos[1] < self.img.shape[0]*1)] 
        self.regX2Y4 = self.x_pos[:,(self.x_pos[0]>self.img.shape[1]/4) * (self.x_pos[0]<self.img.shape[1]/2) * (self.x_pos[1] > self.img.shape[0]*3/4) * (self.x_pos[1] < self.img.shape[0]*1)] 
        self.regX3Y4 = self.x_pos[:,(self.x_pos[0]>self.img.shape[1]/2) * (self.x_pos[0]<self.img.shape[1]*3/4) * (self.x_pos[1] > self.img.shape[0]*3/4) * (self.x_pos[1] < self.img.shape[0]*1)] 
        self.regX4Y4 = self.x_pos[:,(self.x_pos[0]>self.img.shape[1]*3/4) *(self.x_pos[0]<self.img.shape[1]/1) * (self.x_pos[1] > self.img.shape[0]*3/4) * (self.x_pos[1] < self.img.shape[0]*1)] 

        # inisiasi size
        size = np.max(self.img.shape)/self.ratio_size[0]

        # inisiasi random size tiap region
        rand_sizeX1Y1 = np.random.rand(self.regX1Y1.shape[1])
        rand_sizeX2Y1 = np.random.rand(self.regX2Y1.shape[1])
        rand_sizeX3Y1 = np.random.rand(self.regX3Y1.shape[1])
        rand_sizeX4Y1 = np.random.rand(self.regX4Y1.shape[1])
        # inisiasi random size tiap region
        rand_sizeX1Y2 = np.random.rand(self.regX1Y2.shape[1])
        rand_sizeX2Y2 = np.random.rand(self.regX2Y2.shape[1])
        rand_sizeX3Y2 = np.random.rand(self.regX3Y2.shape[1])
        rand_sizeX4Y2 = np.random.rand(self.regX4Y2.shape[1])
        # inisiasi random size tiap region
        rand_sizeX1Y3 = np.random.rand(self.regX1Y3.shape[1])
        rand_sizeX2Y3 = np.random.rand(self.regX2Y3.shape[1])
        rand_sizeX3Y3 = np.random.rand(self.regX3Y3.shape[1])
        rand_sizeX4Y3 = np.random.rand(self.regX4Y3.shape[1])
        # inisiasi random size tiap region
        rand_sizeX1Y4 = np.random.rand(self.regX1Y4.shape[1])
        rand_sizeX2Y4 = np.random.rand(self.regX2Y4.shape[1])
        rand_sizeX3Y4 = np.random.rand(self.regX3Y4.shape[1])
        rand_sizeX4Y4 = np.random.rand(self.regX4Y4.shape[1])

        ukuran_partikelX1Y1 = ((rand_sizeX1Y1+size)*2).astype(int)
        ukuran_partikelX2Y1 = ((rand_sizeX2Y1+size)*2).astype(int)
        ukuran_partikelX3Y1 = ((rand_sizeX3Y1+size)*2).astype(int)
        ukuran_partikelX4Y1 = ((rand_sizeX4Y1+size)*2).astype(int)

        ukuran_partikelX1Y2 = ((rand_sizeX1Y2+size)*2).astype(int)
        ukuran_partikelX2Y2 = ((rand_sizeX2Y2+size)*2).astype(int)
        ukuran_partikelX3Y2 = ((rand_sizeX3Y2+size)*2).astype(int)
        ukuran_partikelX4Y2 = ((rand_sizeX4Y2+size)*2).astype(int)
                    
        ukuran_partikelX1Y3 = ((rand_sizeX1Y3+size)*2).astype(int)
        ukuran_partikelX2Y3 = ((rand_sizeX2Y3+size)*2).astype(int)
        ukuran_partikelX3Y3 = ((rand_sizeX3Y3+size)*2).astype(int)
        ukuran_partikelX4Y3 = ((rand_sizeX4Y3+size)*2).astype(int)
                    
        ukuran_partikelX1Y4 = ((rand_sizeX1Y4+size)*2).astype(int)
        ukuran_partikelX2Y4 = ((rand_sizeX2Y4+size)*2).astype(int)
        ukuran_partikelX3Y4 = ((rand_sizeX3Y4+size)*2).astype(int)
        ukuran_partikelX4Y4 = ((rand_sizeX4Y4+size)*2).astype(int)

        # window
        self.windowX1Y1 = np.zeros((self.dimensi,self.regX1Y1.shape[1]))
        self.windowX2Y1 = np.zeros((self.dimensi,self.regX2Y1.shape[1]))
        self.windowX3Y1 = np.zeros((self.dimensi,self.regX3Y1.shape[1]))
        self.windowX4Y1 = np.zeros((self.dimensi,self.regX4Y1.shape[1]))
        # window
        self.windowX1Y2 = np.zeros((self.dimensi,self.regX1Y2.shape[1]))
        self.windowX2Y2 = np.zeros((self.dimensi,self.regX2Y2.shape[1]))
        self.windowX3Y2 = np.zeros((self.dimensi,self.regX3Y2.shape[1]))
        self.windowX4Y2 = np.zeros((self.dimensi,self.regX4Y2.shape[1]))
        # window
        self.windowX1Y3 = np.zeros((self.dimensi,self.regX1Y3.shape[1]))
        self.windowX2Y3 = np.zeros((self.dimensi,self.regX2Y3.shape[1]))
        self.windowX3Y3 = np.zeros((self.dimensi,self.regX3Y3.shape[1]))
        self.windowX4Y3 = np.zeros((self.dimensi,self.regX4Y3.shape[1]))
        # window
        self.windowX1Y4 = np.zeros((self.dimensi,self.regX1Y4.shape[1]))
        self.windowX2Y4 = np.zeros((self.dimensi,self.regX2Y4.shape[1]))
        self.windowX3Y4 = np.zeros((self.dimensi,self.regX3Y4.shape[1]))
        self.windowX4Y4 = np.zeros((self.dimensi,self.regX4Y4.shape[1]))


        for k in range(self.regX1Y1.shape[1]):
            if rand_sizeX1Y1[k] < .5:
                self.windowX1Y1[0,k] = (1 + np.random.rand(1))*ukuran_partikelX1Y1[k]
                self.windowX1Y1[1,k] = ukuran_partikelX1Y1[k]
            else:
                self.windowX1Y1[0,k] = ukuran_partikelX1Y1[k]
                self.windowX1Y1[1,k] = (1 + np.random.rand(1))*ukuran_partikelX1Y1[k]
        for k in range(self.regX2Y1.shape[1]):
            if rand_sizeX2Y1[k] < .5:
                self.windowX2Y1[0,k] = (1 + np.random.rand(1))*ukuran_partikelX2Y1[k]
                self.windowX2Y1[1,k] = ukuran_partikelX2Y1[k]
            else:
                self.windowX2Y1[0,k] = ukuran_partikelX2Y1[k]
                self.windowX2Y1[1,k] = (1 + np.random.rand(1))*ukuran_partikelX2Y1[k]
        for k in range(self.regX3Y1.shape[1]):
            if rand_sizeX3Y1[k] < .5:
                self.windowX3Y1[0,k] = (1 + np.random.rand(1))*ukuran_partikelX3Y1[k]
                self.windowX3Y1[1,k] = ukuran_partikelX3Y1[k]
            else:
                self.windowX3Y1[0,k] = ukuran_partikelX3Y1[k]
                self.windowX3Y1[1,k] = (1 + np.random.rand(1))*ukuran_partikelX3Y1[k]
        for k in range(self.regX4Y1.shape[1]):
            if rand_sizeX4Y1[k] < .5:
                self.windowX4Y1[0,k] = (1 + np.random.rand(1))*ukuran_partikelX4Y1[k]
                self.windowX4Y1[1,k] = ukuran_partikelX4Y1[k]
            else:
                self.windowX4Y1[0,k] = ukuran_partikelX4Y1[k]
                self.windowX4Y1[1,k] = (1 + np.random.rand(1))*ukuran_partikelX4Y1[k]

        for k in range(self.regX1Y2.shape[1]):
            if rand_sizeX1Y2[k] < .5:
                self.windowX1Y2[0,k] = (1 + np.random.rand(1))*ukuran_partikelX1Y2[k]
                self.windowX1Y2[1,k] = ukuran_partikelX1Y2[k]
            else:
                self.windowX1Y2[0,k] = ukuran_partikelX1Y2[k]
                self.windowX1Y2[1,k] = (1 + np.random.rand(1))*ukuran_partikelX1Y2[k]
        for k in range(self.regX2Y2.shape[1]):
            if rand_sizeX2Y2[k] < .5:
                self.windowX2Y2[0,k] = (1 + np.random.rand(1))*ukuran_partikelX2Y2[k]
                self.windowX2Y2[1,k] = ukuran_partikelX2Y2[k]
            else:
                self.windowX2Y2[0,k] = ukuran_partikelX2Y2[k]
                self.windowX2Y2[1,k] = (1 + np.random.rand(1))*ukuran_partikelX2Y2[k]
        for k in range(self.regX3Y2.shape[1]):
            if rand_sizeX3Y2[k] < .5:
                self.windowX3Y2[0,k] = (1 + np.random.rand(1))*ukuran_partikelX3Y2[k]
                self.windowX3Y2[1,k] = ukuran_partikelX3Y2[k]
            else:
                self.windowX3Y2[0,k] = ukuran_partikelX3Y2[k]
                self.windowX3Y2[1,k] = (1 + np.random.rand(1))*ukuran_partikelX3Y2[k]
        for k in range(self.regX4Y2.shape[1]):
            if rand_sizeX4Y2[k] < .5:
                self.windowX4Y2[0,k] = (1 + np.random.rand(1))*ukuran_partikelX4Y2[k]
                self.windowX4Y2[1,k] = ukuran_partikelX4Y2[k]
            else:
                self.windowX4Y2[0,k] = ukuran_partikelX4Y2[k]
                self.windowX4Y2[1,k] = (1 + np.random.rand(1))*ukuran_partikelX4Y2[k]
                    
        for k in range(self.regX1Y3.shape[1]):
            if rand_sizeX1Y3[k] < .5:
                self.windowX1Y3[0,k] = (1 + np.random.rand(1))*ukuran_partikelX1Y3[k]
                self.windowX1Y3[1,k] = ukuran_partikelX1Y3[k]
            else:
                self.windowX1Y3[0,k] = ukuran_partikelX1Y3[k]
                self.windowX1Y3[1,k] = (1 + np.random.rand(1))*ukuran_partikelX1Y3[k]
        for k in range(self.regX2Y3.shape[1]):
            if rand_sizeX2Y3[k] < .5:
                self.windowX2Y3[0,k] = (1 + np.random.rand(1))*ukuran_partikelX2Y3[k]
                self.windowX2Y3[1,k] = ukuran_partikelX2Y3[k]
            else:
                self.windowX2Y3[0,k] = ukuran_partikelX2Y3[k]
                self.windowX2Y3[1,k] = (1 + np.random.rand(1))*ukuran_partikelX2Y3[k]
        for k in range(self.regX3Y3.shape[1]):
            if rand_sizeX3Y3[k] < .5:
                self.windowX3Y3[0,k] = (1 + np.random.rand(1))*ukuran_partikelX3Y3[k]
                self.windowX3Y3[1,k] = ukuran_partikelX3Y3[k]
            else:
                self.windowX3Y3[0,k] = ukuran_partikelX3Y3[k]
                self.windowX3Y3[1,k] = (1 + np.random.rand(1))*ukuran_partikelX3Y3[k]
        for k in range(self.regX4Y3.shape[1]):
            if rand_sizeX4Y3[k] < .5:
                self.windowX4Y3[0,k] = (1 + np.random.rand(1))*ukuran_partikelX4Y3[k]
                self.windowX4Y3[1,k] = ukuran_partikelX4Y3[k]
            else:
                self.windowX4Y3[0,k] = ukuran_partikelX4Y3[k]
                self.windowX4Y3[1,k] = (1 + np.random.rand(1))*ukuran_partikelX4Y3[k]
                    
        for k in range(self.regX1Y4.shape[1]):
            if rand_sizeX1Y4[k] < .5:
                self.windowX1Y4[0,k] = (1 + np.random.rand(1))*ukuran_partikelX1Y4[k]
                self.windowX1Y4[1,k] = ukuran_partikelX1Y4[k]
            else:
                self.windowX1Y4[0,k] = ukuran_partikelX1Y4[k]
                self.windowX1Y4[1,k] = (1 + np.random.rand(1))*ukuran_partikelX1Y4[k]
        for k in range(self.regX2Y4.shape[1]):
            if rand_sizeX2Y4[k] < .5:
                self.windowX2Y4[0,k] = (1 + np.random.rand(1))*ukuran_partikelX2Y4[k]
                self.windowX2Y4[1,k] = ukuran_partikelX2Y4[k]
            else:
                self.windowX2Y4[0,k] = ukuran_partikelX2Y4[k]
                self.windowX2Y4[1,k] = (1 + np.random.rand(1))*ukuran_partikelX2Y4[k]
        for k in range(self.regX3Y4.shape[1]):
            if rand_sizeX3Y4[k] < .5:
                self.windowX3Y4[0,k] = (1 + np.random.rand(1))*ukuran_partikelX3Y4[k]
                self.windowX3Y4[1,k] = ukuran_partikelX3Y4[k]
            else:
                self.windowX3Y4[0,k] = ukuran_partikelX3Y4[k]
                self.windowX3Y4[1,k] = (1 + np.random.rand(1))*ukuran_partikelX3Y4[k]
        for k in range(self.regX4Y4.shape[1]):
            if rand_sizeX4Y4[k] < .5:
                self.windowX4Y4[0,k] = (1 + np.random.rand(1))*ukuran_partikelX4Y4[k]
                self.windowX4Y4[1,k] = ukuran_partikelX4Y4[k]
            else:
                self.windowX4Y4[0,k] = ukuran_partikelX4Y4[k]
                self.windowX4Y4[1,k] = (1 + np.random.rand(1))*ukuran_partikelX4Y4[k]

    def dimensi_partikel(self,ax, nilaiX, nilaiY, ukuranX, ukuranY, edgeColor,facecolor='none'):
        # startX = abs(nilaiX-(1/2*ukuranX)).astype(int)
        # startY = abs(nilaiY-(1/2*ukuranY)).astype(int)

        # mengatur posisi dan dimensi tiap-tiap partikel dengan looping
        kotak_dimensi = [Rectangle((x, y), panjangX, panjangY)
                    for x, y, panjangX, panjangY in zip(nilaiX, nilaiY, ukuranX, ukuranY)]

        pc = PatchCollection(kotak_dimensi, facecolor=facecolor,
                            edgecolor=edgeColor)

        ax.add_collection(pc)
    
    def plotDimensionWindow(self):
        # Plot dimensi dan partikel
        # fig, ax = plt.subplots(figsize=(3,3))
        # ax.plot(self.x_int, self.y_int, 'o', color='black')
        # for x, y in zip(self.x_int, self.y_int):
        #     ax.text(x, y, (str(x), str(y)), color="black", fontsize=8)
        # ax.imshow(self.img)
        # self.dimensi_partikel(ax, self.startX, self.startY, self.self.windowX, self.windowY, edgeColor='black')

        # plt.show()
        # return fig
        pass

    def dimensi_gbest(self,ax, x, y, ukuranX, ukuranY, edgeColor, faceColor='none'):
        startX = abs(x-(1/2*ukuranX)).astype(int)
        startY = abs(y-(1/2*ukuranY)).astype(int)

        # mengatur posisi dan dimensi tiap-tiap partikel dengan looping
        kotak_dimensi = [Rectangle((x, y), panjangX, panjangY)
                    for x, y, panjangX, panjangY in zip(startX, startY, ukuranX, ukuranY)]

        pc = PatchCollection(kotak_dimensi, facecolor=faceColor,
                            edgecolor=edgeColor)

        ax.add_collection(pc)

    def fitSum(self,x,y,gambar, windowX, windowY):
        # print([x,y])

        x[(x-(gambar.shape[1])).astype(int) >= 0] = (x[(x-(gambar.shape[1])).astype(int) >= 0]-((x[(x-(gambar.shape[1])).astype(int) >= 0]-(gambar.shape[1])).astype(int))).astype(int)
        y[(y-(gambar.shape[0])).astype(int) >= 0] = (y[(y-(gambar.shape[0])).astype(int) >= 0]-((y[(y-(gambar.shape[0])).astype(int) >= 0]-(gambar.shape[0])).astype(int))).astype(int)
        
        startX = abs(x-(1/2*windowX)).astype(int)
        startY = abs(y-(1/2*windowY)).astype(int)

        startX[(x-(1/2*windowX)).astype(int) <= 0] = 0
        startY[(y-(1/2*windowY)).astype(int) <= 0] = 0
        # print(x[(x-(gambar.shape[1])).astype(int) > 0] ,y[(y-(gambar.shape[0])).astype(int) > 0])

        endY = abs(startY + windowY).astype(int)#titik ujung y window
        endX = abs(startX + windowX).astype(int) #titik ujung x window

        if x[(x-(1/2*windowX)).astype(int) <= 0].all():
            # print(x[(x-(1/2*windowX)).astype(int) <= 0])
            x[(x-(1/2*windowX)).astype(int) <= 0] = abs(endX[(x-(1/2*windowX)).astype(int) <= 0]/2) 
            # print(f'{x[(x-(1/2*windowX)).astype(int) <= 0]}\n')
        if y[(y-(1/2*windowY)).astype(int) <= 0].all():
            # print(y[(y-(1/2*windowY)).astype(int) <= 0])  
            y[(y-(1/2*windowY)).astype(int) <= 0] = abs(endY[(y-(1/2*windowY)).astype(int) <= 0]/2) 
            # print(y[(y-(1/2*windowY)).astype(int) <= 0])

        position_update = np.array([x,y], dtype='int32')
        start_position_update = np.array([startX,startY], dtype='int32')

        def cvtHsv(image):    
            imageHSV = cv2.cvtColor(image,cv2.COLOR_RGB2HSV)
            H = imageHSV[:,:,0]
            S = imageHSV[:,:,1]
            V = imageHSV[:,:,2]

            # fig, ax = plt.subplots(3,2,figsize=(10,10))
            # ax[0,0].hist(H.flatten(),180, [0,180],color='r')
            # ax[0,0].set_title(f'Hue, {int(np.mean(H.flatten()))}')
            # ax[1,0].hist(S.flatten(),255, [0,255],color='g')
            # ax[1,0].set_title(f'Saturation, {int(np.mean(S.flatten()))}')
            # ax[2,0].hist(V.flatten(),255, [0,255],color='b')
            # ax[2,0].set_title(f'Value, {int(np.mean(S.flatten()))}')
            # ax[0,1].imshow(image)
            # ax[1,1].imshow(image)
            # ax[2,1].imshow(image)
            
            lower1 = np.array([0,200,200])
            upper1 = np.array([10,255,255])
            lower2 = np.array([169,150,150])
            upper2 = np.array([179,255,255])
                
            upper_mask = cv2.inRange(imageHSV, lower2, upper2)
            lower_mask = cv2.inRange(imageHSV, lower1, upper1)

            mostRed = np.sum(upper_mask+lower_mask)

            almostlower1 = np.array([0,100,100])
            almostupper1 = np.array([12,255,255])
            almostlower2 = np.array([167,100,100])
            almostupper2 = np.array([179,255,255])

            almostLower = cv2.inRange(imageHSV, almostlower1, almostupper1)
            almostUpper = cv2.inRange(imageHSV, almostlower2, almostupper2)

            almostRed = np.sum(almostLower+almostUpper)

            # greenLow = np.array([60,150,150])
            # greenUp = np.array([70,255,255])

            # mostGreen = np.sum(cv2.inRange(imageHSV, greenLow, greenUp))
            
            fitnes = (10*mostRed) + almostRed
    
            # fig, ax = plt.subplots(figsize=(3,3))
            # ax.imshow(image)
            # ax.set_title(fitnes)
            # print(fitnes)
            return fitnes
        result = np.array([cvtHsv(gambar[startY[i]:endY[i], startX[i]:endX[i]]) for i in range(x.shape[0])])
        resultInt = result.astype(int)
        return result, position_update, start_position_update
    
    def startPSO(self, c1=1, c2=1, iterasi=5, w=.5):
        self.iterasi = iterasi
        # inisialisasi kecepatan pastikel secara random
        print('pso start')
        # gbest
        self.gbest = np.zeros([iterasi,16,self.dimensi], dtype='int')
        self.gbest_val = np.zeros([iterasi,16], dtype='int')

        vX1Y1 = np.random.rand(self.dimensi,self.regX1Y1.shape[1])
        vX2Y1 = np.random.rand(self.dimensi,self.regX2Y1.shape[1])
        vX3Y1 = np.random.rand(self.dimensi,self.regX3Y1.shape[1])
        vX4Y1 = np.random.rand(self.dimensi,self.regX4Y1.shape[1])
                    
        vX1Y2 = np.random.rand(self.dimensi,self.regX1Y2.shape[1])
        vX2Y2 = np.random.rand(self.dimensi,self.regX2Y2.shape[1])
        vX3Y2 = np.random.rand(self.dimensi,self.regX3Y2.shape[1])
        vX4Y2 = np.random.rand(self.dimensi,self.regX4Y2.shape[1])

        vX1Y3 = np.random.rand(self.dimensi,self.regX1Y3.shape[1])
        vX2Y3 = np.random.rand(self.dimensi,self.regX2Y3.shape[1])
        vX3Y3 = np.random.rand(self.dimensi,self.regX3Y3.shape[1])
        vX4Y3 = np.random.rand(self.dimensi,self.regX4Y3.shape[1])

        vX1Y4 = np.random.rand(self.dimensi,self.regX1Y4.shape[1])
        vX2Y4 = np.random.rand(self.dimensi,self.regX2Y4.shape[1])
        vX3Y4 = np.random.rand(self.dimensi,self.regX3Y4.shape[1])
        vX4Y4 = np.random.rand(self.dimensi,self.regX4Y4.shape[1])

        self.startPosX1Y1 = np.zeros((self.dimensi,self.regX1Y1.shape[1]), dtype='int32')
        self.startPosX2Y1 = np.zeros((self.dimensi,self.regX2Y1.shape[1]), dtype='int32')
        self.startPosX3Y1 = np.zeros((self.dimensi,self.regX3Y1.shape[1]), dtype='int32')
        self.startPosX4Y1 = np.zeros((self.dimensi,self.regX4Y1.shape[1]), dtype='int32')

        self.startPosX1Y2 = np.zeros((self.dimensi,self.regX1Y2.shape[1]), dtype='int32')
        self.startPosX2Y2 = np.zeros((self.dimensi,self.regX2Y2.shape[1]), dtype='int32')
        self.startPosX3Y2 = np.zeros((self.dimensi,self.regX3Y2.shape[1]), dtype='int32')
        self.startPosX4Y2 = np.zeros((self.dimensi,self.regX4Y2.shape[1]), dtype='int32')

        self.startPosX1Y3 = np.zeros((self.dimensi,self.regX1Y3.shape[1]), dtype='int32')
        self.startPosX2Y3 = np.zeros((self.dimensi,self.regX2Y3.shape[1]), dtype='int32')
        self.startPosX3Y3 = np.zeros((self.dimensi,self.regX3Y3.shape[1]), dtype='int32')
        self.startPosX4Y3 = np.zeros((self.dimensi,self.regX4Y3.shape[1]), dtype='int32')

        self.startPosX1Y4 = np.zeros((self.dimensi,self.regX1Y4.shape[1]), dtype='int32')
        self.startPosX2Y4 = np.zeros((self.dimensi,self.regX2Y4.shape[1]), dtype='int32')
        self.startPosX3Y4 = np.zeros((self.dimensi,self.regX3Y4.shape[1]), dtype='int32')
        self.startPosX4Y4 = np.zeros((self.dimensi,self.regX4Y4.shape[1]), dtype='int32')

        # print(self.regX1Y1[0], self.fitSum(x = self.regX1Y1[0], y = self.regX1Y1[1], gambar = self.img, windowX = self.windowX1Y1[1], windowY= self.windowX1Y1[0]))

        self.pbest_valX1Y1, self.regX1Y1, self.startPosX1Y1 = self.fitSum(x = self.regX1Y1[0], y = self.regX1Y1[1], gambar = self.img, windowX = self.windowX1Y1[1], windowY= self.windowX1Y1[0])
        self.pbestX1Y1 = self.regX1Y1 # posisi self.pbest awal
        self.pbest_valX2Y1, self.regX2Y1, self.startPosX2Y1 = self.fitSum(self.regX2Y1[0], self.regX2Y1[1], self.img, self.windowX2Y1[1], self.windowX2Y1[0])
        self.pbestX2Y1 = self.regX2Y1 # posisi self.pbest awal
        self.pbest_valX3Y1, self.regX3Y1, self.startPosX3Y1 = self.fitSum(self.regX3Y1[0], self.regX3Y1[1], self.img, self.windowX3Y1[1], self.windowX3Y1[0])
        self.pbestX3Y1 = self.regX3Y1 # posisi self.pbest awal
        self.pbest_valX4Y1, self.regX4Y1, self.startPosX4Y1 = self.fitSum(self.regX4Y1[0], self.regX4Y1[1], self.img, self.windowX4Y1[1], self.windowX4Y1[0])
        self.pbestX4Y1 = self.regX4Y1 # posisi self.pbest awal

        self.pbest_valX1Y2, self.regX1Y2, self.startPosX1Y2 = self.fitSum(self.regX1Y2[0], self.regX1Y2[1], self.img, self.windowX1Y2[1], self.windowX1Y2[0])
        self.pbestX1Y2 = self.regX1Y2 # posisi self.pbest awal
        self.pbest_valX2Y2, self.regX2Y2, self.startPosX2Y2 = self.fitSum(self.regX2Y2[0], self.regX2Y2[1], self.img, self.windowX2Y2[1], self.windowX2Y2[0])
        self.pbestX2Y2 = self.regX2Y2 # posisi self.pbest awal
        self.pbest_valX3Y2, self.regX3Y2, self.startPosX3Y2 = self.fitSum(self.regX3Y2[0], self.regX3Y2[1], self.img, self.windowX3Y2[1], self.windowX3Y2[0])
        self.pbestX3Y2 = self.regX3Y2 # posisi self.pbest awal
        self.pbest_valX4Y2, self.regX4Y2, self.startPosX4Y2 = self.fitSum(self.regX4Y2[0], self.regX4Y2[1], self.img, self.windowX4Y2[1], self.windowX4Y2[0])
        self.pbestX4Y2 = self.regX4Y2 # posisi self.pbest awal

        self.pbest_valX1Y3, self.regX1Y3, self.startPosX1Y3 = self.fitSum(self.regX1Y3[0], self.regX1Y3[1], self.img, self.windowX1Y3[1], self.windowX1Y3[0])
        self.pbestX1Y3 = self.regX1Y3 # posisi self.pbest awal
        self.pbest_valX2Y3, self.regX2Y3, self.startPosX2Y3 = self.fitSum(self.regX2Y3[0], self.regX2Y3[1], self.img, self.windowX2Y3[1], self.windowX2Y3[0])
        self.pbestX2Y3 = self.regX2Y3 # posisi self.pbest awal
        self.pbest_valX3Y3, self.regX3Y3, self.startPosX3Y3 = self.fitSum(self.regX3Y3[0], self.regX3Y3[1], self.img, self.windowX3Y3[1], self.windowX3Y3[0])
        self.pbestX3Y3 = self.regX3Y3 # posisi self.pbest awal
        self.pbest_valX4Y3, self.regX4Y3, self.startPosX4Y3 = self.fitSum(self.regX4Y3[0], self.regX4Y3[1], self.img, self.windowX4Y3[1], self.windowX4Y3[0])
        self.pbestX4Y3 = self.regX4Y3 # posisi self.pbest awal

        self.pbest_valX1Y4, self.regX1Y4, self.startPosX1Y4 = self.fitSum(self.regX1Y4[0], self.regX1Y4[1], self.img, self.windowX1Y4[1], self.windowX1Y4[0])
        self.pbestX1Y4 = self.regX1Y4 # posisi self.pbest awal
        self.pbest_valX2Y4, self.regX2Y4, self.startPosX2Y4 = self.fitSum(self.regX2Y4[0], self.regX2Y4[1], self.img, self.windowX2Y4[1], self.windowX2Y4[0])
        self.pbestX2Y4 = self.regX2Y4 # posisi self.pbest awal
        self.pbest_valX3Y4, self.regX3Y4, self.startPosX3Y4 = self.fitSum(self.regX3Y4[0], self.regX3Y4[1], self.img, self.windowX3Y4[1], self.windowX3Y4[0])
        self.pbestX3Y4 = self.regX3Y4 # posisi self.pbest awal
        self.pbest_valX4Y4, self.regX4Y4, self.startPosX4Y4 = self.fitSum(self.regX4Y4[0], self.regX4Y4[1], self.img, self.windowX4Y4[1], self.windowX4Y4[0])
        self.pbestX4Y4 = self.regX4Y4 # posisi self.pbest awal

        index = np.array([self.pbest_valX1Y1.argmax(),self.pbest_valX2Y1.argmax(),self.pbest_valX3Y1.argmax(),self.pbest_valX4Y1.argmax(),self.pbest_valX1Y2.argmax(),self.pbest_valX2Y2.argmax(),self.pbest_valX3Y2.argmax(),self.pbest_valX4Y2.argmax(),self.pbest_valX1Y3.argmax(),self.pbest_valX2Y3.argmax(),self.pbest_valX3Y3.argmax(),self.pbest_valX4Y3.argmax(),self.pbest_valX1Y4.argmax(),self.pbest_valX2Y4.argmax(),self.pbest_valX3Y4.argmax(),self.pbest_valX4Y4.argmax()])

        self.gbest[0,0] = self.pbestX1Y1[:,index[0]]
        self.gbest_val[0,0] = self.pbest_valX1Y1.max()
        self.gbest[0,1] = self.pbestX2Y1[:,index[1]]
        self.gbest_val[0,1] = self.pbest_valX2Y1.max()
        self.gbest[0,2] = self.pbestX3Y1[:,index[2]]
        self.gbest_val[0,2] = self.pbest_valX3Y1.max()
        self.gbest[0,3] = self.pbestX4Y1[:,index[3]]
        self.gbest_val[0,3] = self.pbest_valX4Y1.max()

        self.gbest[0,4] = self.pbestX1Y2[:,index[4]]
        self.gbest_val[0,4] = self.pbest_valX1Y2.max()
        self.gbest[0,5] = self.pbestX2Y2[:,index[5]]
        self.gbest_val[0,5] = self.pbest_valX2Y2.max()
        self.gbest[0,6] = self.pbestX3Y2[:,index[6]]
        self.gbest_val[0,6] = self.pbest_valX3Y2.max()
        self.gbest[0,7] = self.pbestX4Y2[:,index[7]]
        self.gbest_val[0,7] = self.pbest_valX4Y2.max()

        self.gbest[0,8] = self.pbestX1Y3[:,index[8]]
        self.gbest_val[0,8] = self.pbest_valX1Y3.max()
        self.gbest[0,9] = self.pbestX2Y3[:,index[9]]
        self.gbest_val[0,9] = self.pbest_valX2Y3.max()
        self.gbest[0,10] = self.pbestX3Y3[:,index[10]]
        self.gbest_val[0,10] = self.pbest_valX3Y3.max()
        self.gbest[0,11] = self.pbestX4Y3[:,index[11]]
        self.gbest_val[0,11] = self.pbest_valX4Y3.max()

        self.gbest[0,12] = self.pbestX1Y4[:,index[12]]
        self.gbest_val[0,12] = self.pbest_valX1Y4.max()
        self.gbest[0,13] = self.pbestX2Y4[:,index[13]]
        self.gbest_val[0,13] = self.pbest_valX2Y4.max()
        self.gbest[0,14] = self.pbestX3Y4[:,index[14]]
        self.gbest_val[0,14] = self.pbest_valX3Y4.max()
        self.gbest[0,15] = self.pbestX4Y4[:,index[15]]
        self.gbest_val[0,15] = self.pbest_valX4Y4.max()

        # fig, ax = plt.subplots(figsize=(5,5))
        # fig.tight_layout()
        # ax.imshow(self.img)
        # ax.plot(self.regX1Y1[0], self.regX1Y1[1], 'o', color='#cf127b')
        # ax.plot(self.regX2Y1[0], self.regX2Y1[1], 'o', color='#8fdc83')
        # ax.plot(self.regX3Y1[0], self.regX3Y1[1], 'o', color='#089159')
        # ax.plot(self.regX4Y1[0], self.regX4Y1[1], 'o', color='#c18e2c')

        # ax.plot(self.regX1Y2[0], self.regX1Y2[1], 'o', color='#c1c4cf')
        # ax.plot(self.regX2Y2[0], self.regX2Y2[1], 'o', color='#f274ab')
        # ax.plot(self.regX3Y2[0], self.regX3Y2[1], 'o', color='#9b89f7')
        # ax.plot(self.regX4Y2[0], self.regX4Y2[1], 'o', color='#927409')

        # ax.plot(self.regX1Y3[0], self.regX1Y3[1], 'o', color='#1f12e5')
        # ax.plot(self.regX2Y3[0], self.regX2Y3[1], 'o', color='#f2d104')
        # ax.plot(self.regX3Y3[0], self.regX3Y3[1], 'o', color='#61bf00')
        # ax.plot(self.regX4Y3[0], self.regX4Y3[1], 'o', color='#02c121')

        # ax.plot(self.regX1Y4[0], self.regX1Y4[1], 'o', color='#715d6e')
        # ax.plot(self.regX2Y4[0], self.regX2Y4[1], 'o', color='#377f20')
        # ax.plot(self.regX3Y4[0], self.regX3Y4[1], 'o', color='#6e9e42')
        # ax.plot(self.regX4Y4[0], self.regX4Y4[1], 'o', color='#b28a68')
                                
        # dimensi_partikel(ax, self.startPosX1Y1[0], self.startPosX1Y1[1], self.windowX1Y1[0], self.windowX1Y1[1], edgeColor='black')
        # dimensi_partikel(ax, self.startPosX2Y1[0], self.startPosX2Y1[1], self.windowX2Y1[0], self.windowX2Y1[1], edgeColor='blue')
        # dimensi_partikel(ax, self.startPosX3Y1[0], self.startPosX3Y1[1], self.windowX3Y1[0], self.windowX3Y1[1], edgeColor='cyan')
        # dimensi_partikel(ax, self.startPosX4Y1[0], self.startPosX4Y1[1], self.windowX4Y1[0], self.windowX4Y1[1], edgeColor='green')
                                
        # dimensi_partikel(ax, self.startPosX1Y2[0], self.startPosX1Y2[1], self.windowX1Y2[0], self.windowX1Y2[1], edgeColor='black')
        # dimensi_partikel(ax, self.startPosX2Y2[0], self.startPosX2Y2[1], self.windowX2Y2[0], self.windowX2Y2[1], edgeColor='blue')
        # dimensi_partikel(ax, self.startPosX3Y2[0], self.startPosX3Y2[1], self.windowX3Y2[0], self.windowX3Y2[1], edgeColor='cyan')
        # dimensi_partikel(ax, self.startPosX4Y2[0], self.startPosX4Y2[1], self.windowX4Y2[0], self.windowX4Y2[1], edgeColor='green')
                                
        # dimensi_partikel(ax, self.startPosX1Y3[0], self.startPosX1Y3[1], self.windowX1Y3[0], self.windowX1Y3[1], edgeColor='black')
        # dimensi_partikel(ax, self.startPosX2Y3[0], self.startPosX2Y3[1], self.windowX2Y3[0], self.windowX2Y3[1], edgeColor='blue')
        # dimensi_partikel(ax, self.startPosX3Y3[0], self.startPosX3Y3[1], self.windowX3Y3[0], self.windowX3Y3[1], edgeColor='cyan')
        # dimensi_partikel(ax, self.startPosX4Y3[0], self.startPosX4Y3[1], self.windowX4Y3[0], self.windowX4Y3[1], edgeColor='green')
                                
        # dimensi_partikel(ax, self.startPosX1Y4[0], self.startPosX1Y4[1], self.windowX1Y4[0], self.windowX1Y4[1], edgeColor='black')
        # dimensi_partikel(ax, self.startPosX2Y4[0], self.startPosX2Y4[1], self.windowX2Y4[0], self.windowX2Y4[1], edgeColor='blue')
        # dimensi_partikel(ax, self.startPosX3Y4[0], self.startPosX3Y4[1], self.windowX3Y4[0], self.windowX3Y4[1], edgeColor='cyan')
        # dimensi_partikel(ax, self.startPosX4Y4[0], self.startPosX4Y4[1], self.windowX4Y4[0], self.windowX4Y4[1], edgeColor='green')

        plt.grid()

        for j in range(1,iterasi):
            print(j)
            r1 = np.random.rand()
            r2 = np.random.rand()
                                    
                            # atur nilai kecepatan dan posisi
            vX1Y1 = w + vX1Y1 + (c1*r1*(self.pbestX1Y1-self.regX1Y1))+(c2*r2*(self.gbest[j-1,0].reshape(-1,1)-self.regX1Y1))
            vX2Y1 = w + vX2Y1 + (c1*r1*(self.pbestX2Y1-self.regX2Y1))+(c2*r2*(self.gbest[j-1,1].reshape(-1,1)-self.regX2Y1))
            vX3Y1 = w + vX3Y1 + (c1*r1*(self.pbestX3Y1-self.regX3Y1))+(c2*r2*(self.gbest[j-1,2].reshape(-1,1)-self.regX3Y1))
            vX4Y1 = w + vX4Y1 + (c1*r1*(self.pbestX4Y1-self.regX4Y1))+(c2*r2*(self.gbest[j-1,3].reshape(-1,1)-self.regX4Y1))
            self.regX1Y1 = (self.regX1Y1+vX1Y1).astype(int)
            self.regX2Y1 = (self.regX2Y1+vX2Y1).astype(int)
            self.regX3Y1 = (self.regX3Y1+vX3Y1).astype(int)
            self.regX4Y1 = (self.regX4Y1+vX4Y1).astype(int)
            # x_pos = x_pos.astype(int)
            self.regX1Y1[self.regX1Y1<0] = self.regX1Y1[self.regX1Y1<0] + abs(self.regX1Y1[self.regX1Y1<0])
            self.regX2Y1[self.regX2Y1<0] = self.regX2Y1[self.regX2Y1<0] + abs(self.regX2Y1[self.regX2Y1<0])
            self.regX3Y1[self.regX3Y1<0] = self.regX3Y1[self.regX3Y1<0] + abs(self.regX3Y1[self.regX3Y1<0])
            self.regX4Y1[self.regX4Y1<0] = self.regX4Y1[self.regX4Y1<0] + abs(self.regX4Y1[self.regX4Y1<0])
                                    
            # atur nilai kecepatan dan posisi
            vX1Y2 = w + vX1Y2 + (c1*r1*(self.pbestX1Y2-self.regX1Y2))+(c2*r2*(self.gbest[j-1,4].reshape(-1,1)-self.regX1Y2))
            vX2Y2 = w + vX2Y2 + (c1*r1*(self.pbestX2Y2-self.regX2Y2))+(c2*r2*(self.gbest[j-1,5].reshape(-1,1)-self.regX2Y2))
            vX3Y2 = w + vX3Y2 + (c1*r1*(self.pbestX3Y2-self.regX3Y2))+(c2*r2*(self.gbest[j-1,6].reshape(-1,1)-self.regX3Y2))
            vX4Y2 = w + vX4Y2 + (c1*r1*(self.pbestX4Y2-self.regX4Y2))+(c2*r2*(self.gbest[j-1,7].reshape(-1,1)-self.regX4Y2))
            self.regX1Y2 = (self.regX1Y2+vX1Y2).astype(int)
            self.regX2Y2 = (self.regX2Y2+vX2Y2).astype(int)
            self.regX3Y2 = (self.regX3Y2+vX3Y2).astype(int)
            self.regX4Y2 = (self.regX4Y2+vX4Y2).astype(int)
            # x_pos = x_pos.astype(int)
            self.regX1Y2[self.regX1Y2<0] = self.regX1Y2[self.regX1Y2<0] + abs(self.regX1Y2[self.regX1Y2<0])
            self.regX2Y2[self.regX2Y2<0] = self.regX2Y2[self.regX2Y2<0] + abs(self.regX2Y2[self.regX2Y2<0])
            self.regX3Y2[self.regX3Y2<0] = self.regX3Y2[self.regX3Y2<0] + abs(self.regX3Y2[self.regX3Y2<0])
            self.regX4Y2[self.regX4Y2<0] = self.regX4Y2[self.regX4Y2<0] + abs(self.regX4Y2[self.regX4Y2<0])
                                    
            # atur nilai kecepatan dan posisi
            vX1Y3 = w + vX1Y3 + (c1*r1*(self.pbestX1Y3-self.regX1Y3))+(c2*r2*(self.gbest[j-1,8].reshape(-1,1)-self.regX1Y3))
            vX2Y3 = w + vX2Y3 + (c1*r1*(self.pbestX2Y3-self.regX2Y3))+(c2*r2*(self.gbest[j-1,9].reshape(-1,1)-self.regX2Y3))
            vX3Y3 = w + vX3Y3 + (c1*r1*(self.pbestX3Y3-self.regX3Y3))+(c2*r2*(self.gbest[j-1,10].reshape(-1,1)-self.regX3Y3))
            vX4Y3 = w + vX4Y3 + (c1*r1*(self.pbestX4Y3-self.regX4Y3))+(c2*r2*(self.gbest[j-1,11].reshape(-1,1)-self.regX4Y3))
            self.regX1Y3 = (self.regX1Y3+vX1Y3).astype(int)
            self.regX2Y3 = (self.regX2Y3+vX2Y3).astype(int)
            self.regX3Y3 = (self.regX3Y3+vX3Y3).astype(int)
            self.regX4Y3 = (self.regX4Y3+vX4Y3).astype(int)
            # x_pos = x_pos.astype(int)
            self.regX1Y3[self.regX1Y3<0] = self.regX1Y3[self.regX1Y3<0] + abs(self.regX1Y3[self.regX1Y3<0])
            self.regX2Y3[self.regX2Y3<0] = self.regX2Y3[self.regX2Y3<0] + abs(self.regX2Y3[self.regX2Y3<0])
            self.regX3Y3[self.regX3Y3<0] = self.regX3Y3[self.regX3Y3<0] + abs(self.regX3Y3[self.regX3Y3<0])
            self.regX4Y3[self.regX4Y3<0] = self.regX4Y3[self.regX4Y3<0] + abs(self.regX4Y3[self.regX4Y3<0])
                                    
            # atur nilai kecepatan dan posisi
            vX1Y4 = w + vX1Y4 + (c1*r1*(self.pbestX1Y4-self.regX1Y4))+(c2*r2*(self.gbest[j-1,12].reshape(-1,1)-self.regX1Y4))
            vX2Y4 = w + vX2Y4 + (c1*r1*(self.pbestX2Y4-self.regX2Y4))+(c2*r2*(self.gbest[j-1,13].reshape(-1,1)-self.regX2Y4))
            vX3Y4 = w + vX3Y4 + (c1*r1*(self.pbestX3Y4-self.regX3Y4))+(c2*r2*(self.gbest[j-1,14].reshape(-1,1)-self.regX3Y4))
            vX4Y4 = w + vX4Y4 + (c1*r1*(self.pbestX4Y4-self.regX4Y4))+(c2*r2*(self.gbest[j-1,15].reshape(-1,1)-self.regX4Y4))
            self.regX1Y4 = (self.regX1Y4+vX1Y4).astype(int)
            self.regX2Y4 = (self.regX2Y4+vX2Y4).astype(int)
            self.regX3Y4 = (self.regX3Y4+vX3Y4).astype(int)
            self.regX4Y4 = (self.regX4Y4+vX4Y4).astype(int)
            # x_pos = x_pos.astype(int)
            self.regX1Y4[self.regX1Y4<0] = self.regX1Y4[self.regX1Y4<0] + abs(self.regX1Y4[self.regX1Y4<0])
            self.regX2Y4[self.regX2Y4<0] = self.regX2Y4[self.regX2Y4<0] + abs(self.regX2Y4[self.regX2Y4<0])
            self.regX3Y4[self.regX3Y4<0] = self.regX3Y4[self.regX3Y4<0] + abs(self.regX3Y4[self.regX3Y4<0])
            self.regX4Y4[self.regX4Y4<0] = self.regX4Y4[self.regX4Y4<0] + abs(self.regX4Y4[self.regX4Y4<0])
                            

            # masukkan nilai self.pbest baru
            self.fitnessX1Y1, self.regX1Y1, self.startPosX1Y1 = self.fitSum(self.regX1Y1[0], self.regX1Y1[1], self.img, self.windowX1Y1[0], self.windowX1Y1[1])
            self.fitnessX2Y1, self.regX2Y1, self.startPosX2Y1 = self.fitSum(self.regX2Y1[0], self.regX2Y1[1], self.img, self.windowX2Y1[0], self.windowX2Y1[1])
            self.fitnessX3Y1, self.regX3Y1, self.startPosX3Y1 = self.fitSum(self.regX3Y1[0], self.regX3Y1[1], self.img, self.windowX3Y1[0], self.windowX3Y1[1])
            self.fitnessX4Y1, self.regX4Y1, self.startPosX4Y1 = self.fitSum(self.regX4Y1[0], self.regX4Y1[1], self.img, self.windowX4Y1[0], self.windowX4Y1[1])

            self.fitnessX1Y2, self.regX1Y2, self.startPosX1Y2 = self.fitSum(self.regX1Y2[0], self.regX1Y2[1], self.img, self.windowX1Y2[0], self.windowX1Y2[1])
            self.fitnessX2Y2, self.regX2Y2, self.startPosX2Y2 = self.fitSum(self.regX2Y2[0], self.regX2Y2[1], self.img, self.windowX2Y2[0], self.windowX2Y2[1])
            self.fitnessX3Y2, self.regX3Y2, self.startPosX3Y2 = self.fitSum(self.regX3Y2[0], self.regX3Y2[1], self.img, self.windowX3Y2[0], self.windowX3Y2[1])
            self.fitnessX4Y2, self.regX4Y2, self.startPosX4Y2 = self.fitSum(self.regX4Y2[0], self.regX4Y2[1], self.img, self.windowX4Y2[0], self.windowX4Y2[1])

            self.fitnessX1Y3, self.regX1Y3, self.startPosX1Y3 = self.fitSum(self.regX1Y3[0], self.regX1Y3[1], self.img, self.windowX1Y3[0], self.windowX1Y3[1])
            self.fitnessX2Y3, self.regX2Y3, self.startPosX2Y3 = self.fitSum(self.regX2Y3[0], self.regX2Y3[1], self.img, self.windowX2Y3[0], self.windowX2Y3[1])
            self.fitnessX3Y3, self.regX3Y3, self.startPosX3Y3 = self.fitSum(self.regX3Y3[0], self.regX3Y3[1], self.img, self.windowX3Y3[0], self.windowX3Y3[1])
            self.fitnessX4Y3, self.regX4Y3, self.startPosX4Y3 = self.fitSum(self.regX4Y3[0], self.regX4Y3[1], self.img, self.windowX4Y3[0], self.windowX4Y3[1])

            self.fitnessX1Y4, self.regX1Y4, self.startPosX1Y4 = self.fitSum(self.regX1Y4[0], self.regX1Y4[1], self.img, self.windowX1Y4[0], self.windowX1Y4[1])
            self.fitnessX2Y4, self.regX2Y4, self.startPosX2Y4 = self.fitSum(self.regX2Y4[0], self.regX2Y4[1], self.img, self.windowX2Y4[0], self.windowX2Y4[1])
            self.fitnessX3Y4, self.regX3Y4, self.startPosX3Y4 = self.fitSum(self.regX3Y4[0], self.regX3Y4[1], self.img, self.windowX3Y4[0], self.windowX3Y4[1])
            self.fitnessX4Y4, self.regX4Y4, self.startPosX4Y4 = self.fitSum(self.regX4Y4[0], self.regX4Y4[1], self.img, self.windowX4Y4[0], self.windowX4Y4[1])
                            # print(x_pos)

            self.pbestX1Y1[:,(self.pbest_valX1Y1 > self.fitnessX1Y1)] = self.pbestX1Y1[:,(self.pbest_valX1Y1 > self.fitnessX1Y1)]
            self.pbestX1Y1[:,(self.fitnessX1Y1 > self.pbest_valX1Y1)] = self.regX1Y1[:,(self.fitnessX1Y1 > self.pbest_valX1Y1)]
            self.pbestX2Y1[:,(self.pbest_valX2Y1 > self.fitnessX2Y1)] = self.pbestX2Y1[:,(self.pbest_valX2Y1 > self.fitnessX2Y1)]
            self.pbestX2Y1[:,(self.fitnessX2Y1 > self.pbest_valX2Y1)] = self.regX2Y1[:,(self.fitnessX2Y1 > self.pbest_valX2Y1)]
            self.pbestX3Y1[:,(self.pbest_valX3Y1 > self.fitnessX3Y1)] = self.pbestX3Y1[:,(self.pbest_valX3Y1 > self.fitnessX3Y1)]
            self.pbestX3Y1[:,(self.fitnessX3Y1 > self.pbest_valX3Y1)] = self.regX3Y1[:,(self.fitnessX3Y1 > self.pbest_valX3Y1)]
            self.pbestX4Y1[:,(self.pbest_valX4Y1 > self.fitnessX4Y1)] = self.pbestX4Y1[:,(self.pbest_valX4Y1 > self.fitnessX4Y1)]
            self.pbestX4Y1[:,(self.fitnessX4Y1 > self.pbest_valX4Y1)] = self.regX4Y1[:,(self.fitnessX4Y1 > self.pbest_valX4Y1)]

            self.pbestX1Y2[:,(self.pbest_valX1Y2 > self.fitnessX1Y2)] = self.pbestX1Y2[:,(self.pbest_valX1Y2 > self.fitnessX1Y2)]
            self.pbestX1Y2[:,(self.fitnessX1Y2 > self.pbest_valX1Y2)] = self.regX1Y2[:,(self.fitnessX1Y2 > self.pbest_valX1Y2)]
            self.pbestX2Y2[:,(self.pbest_valX2Y2 > self.fitnessX2Y2)] = self.pbestX2Y2[:,(self.pbest_valX2Y2 > self.fitnessX2Y2)]
            self.pbestX2Y2[:,(self.fitnessX2Y2 > self.pbest_valX2Y2)] = self.regX2Y2[:,(self.fitnessX2Y2 > self.pbest_valX2Y2)]
            self.pbestX3Y2[:,(self.pbest_valX3Y2 > self.fitnessX3Y2)] = self.pbestX3Y2[:,(self.pbest_valX3Y2 > self.fitnessX3Y2)]
            self.pbestX3Y2[:,(self.fitnessX3Y2 > self.pbest_valX3Y2)] = self.regX3Y2[:,(self.fitnessX3Y2 > self.pbest_valX3Y2)]
            self.pbestX4Y2[:,(self.pbest_valX4Y2 > self.fitnessX4Y2)] = self.pbestX4Y2[:,(self.pbest_valX4Y2 > self.fitnessX4Y2)]
            self.pbestX4Y2[:,(self.fitnessX4Y2 > self.pbest_valX4Y2)] = self.regX4Y2[:,(self.fitnessX4Y2 > self.pbest_valX4Y2)]

            self.pbestX1Y3[:,(self.pbest_valX1Y3 > self.fitnessX1Y3)] = self.pbestX1Y3[:,(self.pbest_valX1Y3 > self.fitnessX1Y3)]
            self.pbestX1Y3[:,(self.fitnessX1Y3 > self.pbest_valX1Y3)] = self.regX1Y3[:,(self.fitnessX1Y3 > self.pbest_valX1Y3)]
            self.pbestX2Y3[:,(self.pbest_valX2Y3 > self.fitnessX2Y3)] = self.pbestX2Y3[:,(self.pbest_valX2Y3 > self.fitnessX2Y3)]
            self.pbestX2Y3[:,(self.fitnessX2Y3 > self.pbest_valX2Y3)] = self.regX2Y3[:,(self.fitnessX2Y3 > self.pbest_valX2Y3)]
            self.pbestX3Y3[:,(self.pbest_valX3Y3 > self.fitnessX3Y3)] = self.pbestX3Y3[:,(self.pbest_valX3Y3 > self.fitnessX3Y3)]
            self.pbestX3Y3[:,(self.fitnessX3Y3 > self.pbest_valX3Y3)] = self.regX3Y3[:,(self.fitnessX3Y3 > self.pbest_valX3Y3)]
            self.pbestX4Y3[:,(self.pbest_valX4Y3 > self.fitnessX4Y3)] = self.pbestX4Y3[:,(self.pbest_valX4Y3 > self.fitnessX4Y3)]
            self.pbestX4Y3[:,(self.fitnessX4Y3 > self.pbest_valX4Y3)] = self.regX4Y3[:,(self.fitnessX4Y3 > self.pbest_valX4Y3)]

            self.pbestX1Y4[:,(self.pbest_valX1Y4 > self.fitnessX1Y4)] = self.pbestX1Y4[:,(self.pbest_valX1Y4 > self.fitnessX1Y4)]
            self.pbestX1Y4[:,(self.fitnessX1Y4 > self.pbest_valX1Y4)] = self.regX1Y4[:,(self.fitnessX1Y4 > self.pbest_valX1Y4)]
            self.pbestX2Y4[:,(self.pbest_valX2Y4 > self.fitnessX2Y4)] = self.pbestX2Y4[:,(self.pbest_valX2Y4 > self.fitnessX2Y4)]
            self.pbestX2Y4[:,(self.fitnessX2Y4 > self.pbest_valX2Y4)] = self.regX2Y4[:,(self.fitnessX2Y4 > self.pbest_valX2Y4)]
            self.pbestX3Y4[:,(self.pbest_valX3Y4 > self.fitnessX3Y4)] = self.pbestX3Y4[:,(self.pbest_valX3Y4 > self.fitnessX3Y4)]
            self.pbestX3Y4[:,(self.fitnessX3Y4 > self.pbest_valX3Y4)] = self.regX3Y4[:,(self.fitnessX3Y4 > self.pbest_valX3Y4)]
            self.pbestX4Y4[:,(self.pbest_valX4Y4 > self.fitnessX4Y4)] = self.pbestX4Y4[:,(self.pbest_valX4Y4 > self.fitnessX4Y4)]
            self.pbestX4Y4[:,(self.fitnessX4Y4 > self.pbest_valX4Y4)] = self.regX4Y4[:,(self.fitnessX4Y4 > self.pbest_valX4Y4)]
                                    
            self.pbest_valX1Y1 = np.array([self.pbest_valX1Y1, self.fitnessX1Y1]).max(axis=0)
            self.pbest_valX2Y1 = np.array([self.pbest_valX2Y1, self.fitnessX2Y1]).max(axis=0)
            self.pbest_valX3Y1 = np.array([self.pbest_valX3Y1, self.fitnessX3Y1]).max(axis=0)
            self.pbest_valX4Y1 = np.array([self.pbest_valX4Y1, self.fitnessX4Y1]).max(axis=0)
                                    
            self.pbest_valX1Y2 = np.array([self.pbest_valX1Y2, self.fitnessX1Y2]).max(axis=0)
            self.pbest_valX2Y2 = np.array([self.pbest_valX2Y2, self.fitnessX2Y2]).max(axis=0)
            self.pbest_valX3Y2 = np.array([self.pbest_valX3Y2, self.fitnessX3Y2]).max(axis=0)
            self.pbest_valX4Y2 = np.array([self.pbest_valX4Y2, self.fitnessX4Y2]).max(axis=0)
                                    
            self.pbest_valX1Y3 = np.array([self.pbest_valX1Y3, self.fitnessX1Y3]).max(axis=0)
            self.pbest_valX2Y3 = np.array([self.pbest_valX2Y3, self.fitnessX2Y3]).max(axis=0)
            self.pbest_valX3Y3 = np.array([self.pbest_valX3Y3, self.fitnessX3Y3]).max(axis=0)
            self.pbest_valX4Y3 = np.array([self.pbest_valX4Y3, self.fitnessX4Y3]).max(axis=0)
                                    
            self.pbest_valX1Y4 = np.array([self.pbest_valX1Y4, self.fitnessX1Y4]).max(axis=0)
            self.pbest_valX2Y4 = np.array([self.pbest_valX2Y4, self.fitnessX2Y4]).max(axis=0)
            self.pbest_valX3Y4 = np.array([self.pbest_valX3Y4, self.fitnessX3Y4]).max(axis=0)
            self.pbest_valX4Y4 = np.array([self.pbest_valX4Y4, self.fitnessX4Y4]).max(axis=0)
            
            # set index nilai terbesar
            self.index = np.array([self.pbest_valX1Y1.argmax(),self.pbest_valX2Y1.argmax(),self.pbest_valX3Y1.argmax(),self.pbest_valX4Y1.argmax(),self.pbest_valX1Y2.argmax(),self.pbest_valX2Y2.argmax(),self.pbest_valX3Y2.argmax(),self.pbest_valX4Y2.argmax(),self.pbest_valX1Y3.argmax(),self.pbest_valX2Y3.argmax(),self.pbest_valX3Y3.argmax(),self.pbest_valX4Y3.argmax(),self.pbest_valX1Y4.argmax(),self.pbest_valX2Y4.argmax(),self.pbest_valX3Y4.argmax(),self.pbest_valX4Y4.argmax()])

            self.gbest[j,0] = self.pbestX1Y1[...,self.index[0]]
            self.gbest_val[j,0] = self.pbest_valX1Y1.max()
            self.gbest[j,1] = self.pbestX2Y1[...,self.index[1]]
            self.gbest_val[j,1] = self.pbest_valX2Y1.max()
            self.gbest[j,2] = self.pbestX3Y1[...,self.index[2]]
            self.gbest_val[j,2] = self.pbest_valX3Y1.max()
            self.gbest[j,3] = self.pbestX4Y1[...,self.index[3]]
            self.gbest_val[j,3] = self.pbest_valX4Y1.max()

            self.gbest[j,4] = self.pbestX1Y2[...,self.index[4]]
            self.gbest_val[j,4] = self.pbest_valX1Y2.max()
            self.gbest[j,5] = self.pbestX2Y2[...,self.index[5]]
            self.gbest_val[j,5] = self.pbest_valX2Y2.max()
            self.gbest[j,6] = self.pbestX3Y2[...,self.index[6]]
            self.gbest_val[j,6] = self.pbest_valX3Y2.max()
            self.gbest[j,7] = self.pbestX4Y2[...,self.index[7]]
            self.gbest_val[j,7] = self.pbest_valX4Y2.max()

            self.gbest[j,8] = self.pbestX1Y3[...,self.index[8]]
            self.gbest_val[j,8] = self.pbest_valX1Y3.max()
            self.gbest[j,9] = self.pbestX2Y3[...,self.index[9]]
            self.gbest_val[j,9] = self.pbest_valX2Y3.max()
            self.gbest[j,10] = self.pbestX3Y3[...,self.index[10]]
            self.gbest_val[j,10] = self.pbest_valX3Y3.max()
            self.gbest[j,11] = self.pbestX4Y3[...,self.index[11]]
            self.gbest_val[j,11] = self.pbest_valX4Y3.max()

            self.gbest[j,12] = self.pbestX1Y4[...,self.index[12]]
            self.gbest_val[j,12] = self.pbest_valX1Y4.max()
            self.gbest[j,13] = self.pbestX2Y4[...,self.index[13]]
            self.gbest_val[j,13] = self.pbest_valX2Y4.max()
            self.gbest[j,14] = self.pbestX3Y4[...,self.index[14]]
            self.gbest_val[j,14] = self.pbest_valX3Y4.max()
            self.gbest[j,15] = self.pbestX4Y4[...,self.index[15]]
            self.gbest_val[j,15] = self.pbest_valX4Y4.max()

            # if j%2==0:
            #     fig, ax = plt.subplots(figsize=(5,5))
            #     fig.tight_layout()
            #     ax.imshow(self.img)
            #     ax.plot(self.regX1Y1[0], self.regX1Y1[1], 'o', color='#cf127b')
            #     ax.plot(self.regX2Y1[0], self.regX2Y1[1], 'o', color='#8fdc83')
            #     ax.plot(self.regX3Y1[0], self.regX3Y1[1], 'o', color='#089159')
            #     ax.plot(self.regX4Y1[0], self.regX4Y1[1], 'o', color='#c18e2c')

            #     ax.plot(self.regX1Y2[0], self.regX1Y2[1], 'o', color='#c1c4cf')
            #     ax.plot(self.regX2Y2[0], self.regX2Y2[1], 'o', color='#f274ab')
            #     ax.plot(self.regX3Y2[0], self.regX3Y2[1], 'o', color='#9b89f7')
            #     ax.plot(self.regX4Y2[0], self.regX4Y2[1], 'o', color='#927409')

            #     ax.plot(self.regX1Y3[0], self.regX1Y3[1], 'o', color='#1f12e5')
            #     ax.plot(self.regX2Y3[0], self.regX2Y3[1], 'o', color='#f2d104')
            #     ax.plot(self.regX3Y3[0], self.regX3Y3[1], 'o', color='#61bf00')
            #     ax.plot(self.regX4Y3[0], self.regX4Y3[1], 'o', color='#02c121')

            #     ax.plot(self.regX1Y4[0], self.regX1Y4[1], 'o', color='#715d6e')
            #     ax.plot(self.regX2Y4[0], self.regX2Y4[1], 'o', color='#377f20')
            #     ax.plot(self.regX3Y4[0], self.regX3Y4[1], 'o', color='#6e9e42')
            #     ax.plot(self.regX4Y4[0], self.regX4Y4[1], 'o', color='#b28a68')

            #     ax.set_title(f't = {j}, optima {self.gbest_val[j]/100},\nC1 = {c1} C2 = {c2} \nRatio = {self.ratio_size}')
                                
            #     self.dimensi_partikel(ax, self.startPosX1Y1[0], self.startPosX1Y1[1], self.windowX1Y1[0], self.windowX1Y1[1], edgeColor='#cf127b')
            #     self.dimensi_partikel(ax, self.startPosX2Y1[0], self.startPosX2Y1[1], self.windowX2Y1[0], self.windowX2Y1[1], edgeColor='#8fdc83')
            #     self.dimensi_partikel(ax, self.startPosX3Y1[0], self.startPosX3Y1[1], self.windowX3Y1[0], self.windowX3Y1[1], edgeColor='#089159')
            #     self.dimensi_partikel(ax, self.startPosX4Y1[0], self.startPosX4Y1[1], self.windowX4Y1[0], self.windowX4Y1[1], edgeColor='#c18e2c')
                                
            #     self.dimensi_partikel(ax, self.startPosX1Y2[0], self.startPosX1Y2[1], self.windowX1Y2[0], self.windowX1Y2[1], edgeColor='#c1c4cf')
            #     self.dimensi_partikel(ax, self.startPosX2Y2[0], self.startPosX2Y2[1], self.windowX2Y2[0], self.windowX2Y2[1], edgeColor='#f274ab')
            #     self.dimensi_partikel(ax, self.startPosX3Y2[0], self.startPosX3Y2[1], self.windowX3Y2[0], self.windowX3Y2[1], edgeColor='#9b89f7')
            #     self.dimensi_partikel(ax, self.startPosX4Y2[0], self.startPosX4Y2[1], self.windowX4Y2[0], self.windowX4Y2[1], edgeColor='#927409')
                                
            #     self.dimensi_partikel(ax, self.startPosX1Y3[0], self.startPosX1Y3[1], self.windowX1Y3[0], self.windowX1Y3[1], edgeColor='#1f12e5')
            #     self.dimensi_partikel(ax, self.startPosX2Y3[0], self.startPosX2Y3[1], self.windowX2Y3[0], self.windowX2Y3[1], edgeColor='#f2d104')
            #     self.dimensi_partikel(ax, self.startPosX3Y3[0], self.startPosX3Y3[1], self.windowX3Y3[0], self.windowX3Y3[1], edgeColor='#61bf00')
            #     self.dimensi_partikel(ax, self.startPosX4Y3[0], self.startPosX4Y3[1], self.windowX4Y3[0], self.windowX4Y3[1], edgeColor='#02c121')
                                
            #     self.dimensi_partikel(ax, self.startPosX1Y4[0], self.startPosX1Y4[1], self.windowX1Y4[0], self.windowX1Y4[1], edgeColor='#715d6e')
            #     self.dimensi_partikel(ax, self.startPosX2Y4[0], self.startPosX2Y4[1], self.windowX2Y4[0], self.windowX2Y4[1], edgeColor='#377f20')
            #     self.dimensi_partikel(ax, self.startPosX3Y4[0], self.startPosX3Y4[1], self.windowX3Y4[0], self.windowX3Y4[1], edgeColor='#6e9e42')
            #     self.dimensi_partikel(ax, self.startPosX4Y4[0], self.startPosX4Y4[1], self.windowX4Y4[0], self.windowX4Y4[1], edgeColor='#b28a68')

            #     plt.grid()


        self.gbest_box = np.zeros((16,4), dtype='int32')

        self.gbest_box[self.gbest_box < 0 ] = 0 
        # print(gbest_box)
                    
        self.gbest_box[0] = np.array([self.gbest[iterasi-1,0,0], self.gbest[iterasi-1,0,1], self.windowX1Y1[0,self.index[0]], self.windowX1Y1[1,self.index[0]]])
        self.gbest_box[1] = np.array([self.gbest[iterasi-1,1,0], self.gbest[iterasi-1,1,1], self.windowX2Y1[0,self.index[1]], self.windowX2Y1[1,self.index[1]]])
        self.gbest_box[2] = np.array([self.gbest[iterasi-1,2,0], self.gbest[iterasi-1,2,1], self.windowX3Y1[0,self.index[2]], self.windowX3Y1[1,self.index[2]]])
        self.gbest_box[3] = np.array([self.gbest[iterasi-1,3,0], self.gbest[iterasi-1,3,1], self.windowX4Y1[0,self.index[3]], self.windowX4Y1[1,self.index[3]]])

        self.gbest_box[4] = np.array([self.gbest[iterasi-1,4,0], self.gbest[iterasi-1,4,1], self.windowX1Y2[0,self.index[4]], self.windowX1Y2[1,self.index[4]]])
        self.gbest_box[5] = np.array([self.gbest[iterasi-1,5,0], self.gbest[iterasi-1,5,1], self.windowX2Y2[0,self.index[5]], self.windowX2Y2[1,self.index[5]]])
        self.gbest_box[6] = np.array([self.gbest[iterasi-1,6,0], self.gbest[iterasi-1,6,1], self.windowX3Y2[0,self.index[6]], self.windowX3Y2[1,self.index[6]]])
        self.gbest_box[7] = np.array([self.gbest[iterasi-1,7,0], self.gbest[iterasi-1,7,1], self.windowX4Y2[0,self.index[7]], self.windowX4Y2[1,self.index[7]]])

        self.gbest_box[8] = np.array([self.gbest[iterasi-1,8,0], self.gbest[iterasi-1,8,1], self.windowX1Y3[0,self.index[8]], self.windowX1Y3[1,self.index[8]]])
        self.gbest_box[9] = np.array([self.gbest[iterasi-1,9,0], self.gbest[iterasi-1,9,1], self.windowX2Y3[0,self.index[9]], self.windowX2Y3[1,self.index[9]]])
        self.gbest_box[10] = np.array([self.gbest[iterasi-1,10,0], self.gbest[iterasi-1,10,1], self.windowX3Y3[0,self.index[10]], self.windowX3Y3[1,self.index[10]]])
        self.gbest_box[11] = np.array([self.gbest[iterasi-1,11,0], self.gbest[iterasi-1,11,1], self.windowX4Y3[0,self.index[11]], self.windowX4Y3[1,self.index[11]]])

        self.gbest_box[12] = np.array([self.gbest[iterasi-1,12,0], self.gbest[iterasi-1,12,1], self.windowX1Y4[0,self.index[12]], self.windowX1Y4[1,self.index[12]]])
        self.gbest_box[13] = np.array([self.gbest[iterasi-1,13,0], self.gbest[iterasi-1,13,1], self.windowX2Y4[0,self.index[13]], self.windowX2Y4[1,self.index[13]]])
        self.gbest_box[14] = np.array([self.gbest[iterasi-1,14,0], self.gbest[iterasi-1,14,1], self.windowX3Y4[0,self.index[14]], self.windowX3Y4[1,self.index[14]]])
        self.gbest_box[15] = np.array([self.gbest[iterasi-1,15,0], self.gbest[iterasi-1,15,1], self.windowX4Y4[0,self.index[15]], self.windowX4Y4[1,self.index[15]]])


        plotGbest = self.gbest[iterasi-1,self.gbest_val[iterasi-1] >0 ]
        print(plotGbest.shape)
        # fig, ax = plt.subplots(figsize=(5,5))
        # fig.tight_layout()
        # ax.imshow(self.img)
        # # ax.set_title()
        # self.dimensi_gbest(ax, self.gbest_box[:,0], self.gbest_box[:,1], self.gbest_box[:,2], self.gbest_box[:,3], edgeColor='black')

        # for i in range(plotGbest.shape[0]):
        #     print(i)

        # ax.plot(self.gbest[iterasi-1,0,0], self.gbest[iterasi-1,0,1], 'o', color='#cf127b')
        # ax.plot(self.gbest[iterasi-1,1,0], self.gbest[iterasi-1,1,1], 'o', color='#8fdc83')
        # ax.plot(self.gbest[iterasi-1,2,0], self.gbest[iterasi-1,2,1], 'o', color='#089159')
        # ax.plot(self.gbest[iterasi-1,3,0], self.gbest[iterasi-1,3,1], 'o', color='#c18e2c')

        # ax.plot(self.gbest[iterasi-1,4,0], self.gbest[iterasi-1,4,1], 'o', color='#c1c4cf')
        # ax.plot(self.gbest[iterasi-1,5,0], self.gbest[iterasi-1,5,1], 'o', color='#f274ab')
        # ax.plot(self.gbest[iterasi-1,6,0], self.gbest[iterasi-1,6,1], 'o', color='#9b89f7')
        # ax.plot(self.gbest[iterasi-1,7,0], self.gbest[iterasi-1,7,1], 'o', color='#927409')

        # ax.plot(self.gbest[iterasi-1,8,0], self.gbest[iterasi-1,8,1], 'o', color='#1f12e5')
        # ax.plot(self.gbest[iterasi-1,9,0], self.gbest[iterasi-1,9,1], 'o', color='#f2d104')
        # ax.plot(self.gbest[iterasi-1,10,0], self.gbest[iterasi-1,10,1], 'o', color='#61bf00')
        # ax.plot(self.gbest[iterasi-1,11,0], self.gbest[iterasi-1,11,1], 'o', color='#02c121')

        # ax.plot(self.gbest[iterasi-1,12,0], self.gbest[iterasi-1,12,1], 'o', color='#715d6e')
        # ax.plot(self.gbest[iterasi-1,13,0], self.gbest[iterasi-1,13,1], 'o', color='#377f20')
        # ax.plot(self.gbest[iterasi-1,14,0], self.gbest[iterasi-1,14,1], 'o', color='#6e9e42')
        # ax.plot(self.gbest[iterasi-1,15,0], self.gbest[iterasi-1,15,1], 'o', color='#b28a68')

        plt.grid()

        print('pso end')

    def createPath(self, x_init_end = 100, y_init_end=200):
        print('create path start')

        box = self.gbest_box
        box = box[self.gbest_val[self.iterasi-1] != 0]

        shape = self.gbest_val[self.iterasi-1,self.gbest_val[self.iterasi-1] != 0].shape[0]
        self.path_point = np.zeros((shape,3), dtype='int32')
        radius = np.zeros((shape,2), dtype='int32')
        radius[...,1] = np.array([i for i in range(radius.shape[0])])

        path_plan = np.zeros((shape,4), dtype='int32')
        path_plan[...,0] = self.gbest_val[self.iterasi-1,self.gbest_val[self.iterasi-1] != 0]
        path_plan[...,1] = self.gbest[self.iterasi-1,self.gbest_val[self.iterasi-1] != 0,0]
        path_plan[...,2] = self.gbest[self.iterasi-1,self.gbest_val[self.iterasi-1] != 0 ,1]
        path_plan[...,3] = radius[...,1]

        start_pointX = x_init_end
        start_pointY = y_init_end

        start_point = np.array([start_pointX, start_pointY], dtype='int')
        back_point = start_point

        self.path_point[0,0] = start_point[0]
        self.path_point[0,1] = start_point[1]
        self.path_point[shape-1,0] = back_point[0]
        self.path_point[shape-1,1] = back_point[1]

        # radius[...,0] = (start_point[0]-path_plan[...,1])**2+(start_point[1]-path_plan[..., 2])**2


        for j in range(shape):
        #         # gunakan rumu pythagoras
            radius[...,0] = (start_point[0]-path_plan[...,1])**2+(start_point[1]-path_plan[..., 2])**2
            radius[...,0] = [sqrt(radius[i,0]) for i in range(radius.shape[0])]
        #         # urutkan berdasarkan jarak terdekat
                # radius = radius[radius[...,0].argsort()]
                # print(radius[0,1])
                # print(path_plan)
                # print(np.where(path_plan[...,3] == radius[0,1])[0][0])

            self.path_point[j,0] = path_plan[np.where(path_plan[:,3] == radius[0,1])[0][0],1]
            self.path_point[j,1] = path_plan[np.where(path_plan[:,3] == radius[0,1])[0][0],2]
            self.path_point[j,2] = radius[0,0]
                
            start_point = self.gbest[self.iterasi-1,radius[0,1]]
            path_plan = np.delete(path_plan ,[np.where(path_plan == radius[0,1])[0][0]] ,axis=0)
            radius = np.delete(radius, [0], axis=0)
            radius = radius[radius[...,1].argsort()]
        print('create path done')

        start_point = np.array([start_pointX, start_pointY], dtype='int')

        final_point = np.zeros((shape+2,2))
        final_point[0] = start_point
        final_point[shape+1] = back_point 
        final_point[1:shape+1] = self.path_point[:,:2]
 
        return final_point, box, self.img
        
    # def pathPlan(self):
    #     box = self.gbest_box
    #     box = box[self.gbest_val[self.iterasi-1] != 0]
    #     fig, ax = plt.subplots(figsize=(3,3))
    #     ax.imshow(self.img)
    #     ax.plot(self.path_point[...,0], self.path_point[...,1], linestyle='dashed', color='black')
    #     ax.plot(self.path_point[...,0], self.path_point[...,1], 'o', color='black')
    #     self.dimensi_gbest(ax, box[:,0], box[:,1], box[:,2], box[:,3], edgeColor='black')

    #     # print(path_point)
    #     # plt.show()
    #     return fig


# test_pso = PSO()
# test_pso.input_gambar('dataset/dataset3.png')
# test_pso.input_partikel(160)
# # test_pso.plotDimensionWindow()
# test_pso.startPSO(iterasi=21)
# test_pso.createPath(100,300)
# test_pso.pathPlan()