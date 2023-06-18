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
        return fig

    def input_partikel(self,partikel):
         # ambil path gambar dan jumlah partikel yang diinginkan
        print('tes threading')
        self.partikel = partikel

        # read image dari path dan memasukkannya ke variable

        # inisialisasi posisi partikel secara random
        self.x = np.random.rand(self.dimensi, self.partikel)

        self.y_int = (self.img.shape[0]*self.x[0]).astype(int)
        self.x_int = (self.img.shape[1]*self.x[1]).astype(int)

        self.x_pos = np.zeros((self.dimensi, self.partikel), dtype='int32')
        self.x_pos[0] = self.x_int
        self.x_pos[1] = self.y_int

        # membuat ukuran dimensi partikel
        self.size = np.mean(self.img.shape)/25
        self.rand_size = np.random.rand(1, self.partikel)

        # ukuran window random awal
        self.ukuran_partikel = (self.rand_size+self.size)*2
        self.ukuran_partikel = self.ukuran_partikel.astype(int)

        # array untuk window
        self.windowX = np.zeros(self.partikel)
        self.windowY = np.zeros(self.partikel)

        # generate nilai window dengan random
        for i in range(self.partikel):
            if self.rand_size[0,i] < .5:
                self.windowX[i] = (1 + np.random.rand(1))*self.ukuran_partikel[0, i]
                self.windowY[i] = self.ukuran_partikel[0, i]
            else:
                self.windowX[i] = self.ukuran_partikel[0, i]
                self.windowY[i] = (1 + np.random.rand(1))*self.ukuran_partikel[0,i]

        # merubah window jadi bentuk integer
        self.windowY = self.windowY.astype(int)
        self.windowX = self.windowX.astype(int)
        
        self.startX = abs(self.x_int-(1/2*self.windowX)).astype(int)
        self.startY = abs(self.y_int-(1/2*self.windowY)).astype(int)
        
        self.startX[(self.x_int-(1/2*self.windowX)).astype(int) <= 0] = 0
        self.startY[(self.y_int-(1/2*self.windowY)).astype(int) <= 0] = 0
        
        self.endY = abs(self.startY + self.windowY).astype(int)#titik ujung y window
        self.endX = abs(self.startX + self.windowX).astype(int) #titik ujung x window

    def dimensi_partikel(self, ax, nilaiX, nilaiY, ukuranX, ukuranY, edgeColor, facecolor='none'):
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
        # self.dimensi_partikel(ax, self.startX, self.startY, self.windowX, self.windowY, edgeColor='black')

        # plt.show()
        # return fig
        pass

    def fitSum(self,x,y,gambar):
    # print([x,y])

        x[(x-(gambar.shape[1])).astype(int) >= 0] = (x[(x-(gambar.shape[1])).astype(int) >= 0]-((x[(x-(gambar.shape[1])).astype(int) >= 0]-(gambar.shape[1])).astype(int))).astype(int)
        y[(y-(gambar.shape[0])).astype(int) >= 0] = (y[(y-(gambar.shape[0])).astype(int) >= 0]-((y[(y-(gambar.shape[0])).astype(int) >= 0]-(gambar.shape[1])).astype(int))).astype(int)
    
        startX = abs(x-(1/2*self.windowX)).astype(int)
        startY = abs(y-(1/2*self.windowY)).astype(int)

        startX[(x-(1/2*self.windowX)).astype(int) <= 0] = 0
        startY[(y-(1/2*self.windowY)).astype(int) <= 0] = 0
        # print(x[(x-(gambar.shape[1])).astype(int) > 0] ,y[(y-(gambar.shape[0])).astype(int) > 0])

        endY = abs(startY + self.windowY).astype(int)#titik ujung y window
        endX = abs(startX + self.windowX).astype(int) #titik ujung x window

        if x[(x-(1/2*self.windowX)).astype(int) <= 0].all():
            # print(x[(x-(1/2*windowX)).astype(int) <= 0])
            x[(x-(1/2*self.windowX)).astype(int) <= 0] = abs(endX[(x-(1/2*self.windowX)).astype(int) <= 0]/2) 
            # print(f'{x[(x-(1/2*windowX)).astype(int) <= 0]}\n')
        if y[(y-(1/2*self.windowY)).astype(int) <= 0].all():
            # print(y[(y-(1/2*windowY)).astype(int) <= 0])  
            y[(y-(1/2*self.windowY)).astype(int) <= 0] = abs(endY[(y-(1/2*self.windowY)).astype(int) <= 0]/2) 
            # print(y[(y-(1/2*windowY)).astype(int) <= 0])

        position_update = np.array([x,y], dtype='int32')
        start_position_update = np.array([startX,startY], dtype='int32')

        def cvtHsv(image):    
            imageHSV = cv2.cvtColor(image,cv2.COLOR_RGB2HSV)
            H = imageHSV[:,:,0]
            S = imageHSV[:,:,1]
            V = imageHSV[:,:,2]

            lower1 = np.array([0,100,150])
            upper1 = np.array([10,185,255])
            lower2 = np.array([160,100,150])
            upper2 = np.array([179,185,255])
            
            upper_mask = cv2.inRange(imageHSV, lower2, upper2)
            lower_mask = cv2.inRange(imageHSV, lower1, upper1)

            mostRed = np.sum(upper_mask+lower_mask)

            almostlower1 = np.array([0,150,100])
            almostupper1 = np.array([10,255,185])
            almostlower2 = np.array([160,150,100])
            almostupper2 = np.array([179,255,185])

            almostLower = cv2.inRange(imageHSV, almostlower1, almostupper1)
            almostUpper = cv2.inRange(imageHSV, almostlower2, almostupper2)

            almostRed = np.sum(almostLower+almostUpper)

            greenLow = np.array([25,150,150])
            greenUp = np.array([75,255,255])

            mostGreen = np.sum(cv2.inRange(imageHSV, greenLow, greenUp))
        
            fitnes = (1.5*mostRed) + almostRed - mostGreen

        # fig, ax = plt.subplots(figsize=(3,3))
        # ax.imshow(image)
        # ax.set_title(fitnes)
        # print(fitnes)
            return fitnes
        result = np.array([cvtHsv(gambar[startY[i]:endY[i], startX[i]:endX[i]]) for i in range(self.partikel)])
        # resultInt = result.astype(int)
        return result, position_update, start_position_update
    
    def startPSO(self, c1=1, c2=1, iterasi=5, w=.5):
        # inisialisasi kecepatan pastikel secara random
        print('pso start')
        v = np.random.rand(self.dimensi,self.partikel)

        # distance 
        self.distance = np.zeros(iterasi, dtype='int')

        # nilai pbest
        # self.pbest = np.zeros((self.dimensi,self.partikel), dtype='int32')
        # self.startPos = np.zeros((self.dimensi,self.partikel), dtype='int32')
        # self.pbest_val = np.zeros((self.partikel))

        # nilai gbest
        self.gbest = np.zeros((iterasi,self.dimensi), dtype='int32')
        self.gbest_val = np.zeros(iterasi, dtype='int32')
        self.pbest_val, self.x_pos, self.startPos = self.fitSum(self.x_int, self.y_int, self.img)
        self.pbest = self.x_pos # posisi pbest 
        
        # temukan index di mana nilai optima ada pada pbest
        self.index = self.pbest_val.argmax()

        # isi gbest dengan nilai posisi partike, dan gbest val untuk nilai fitness pada partikel spesifik
        self.gbest[0] = self.pbest[:,self.index]
        self.gbest_val[0] = self.pbest_val.max()

        for i in range(1,iterasi):
            print(i)
            # atur nilai random
            r1 = np.random.rand()
            r2 = np.random.rand()

            # atur nilai kecepatan dan posisi
            v = w + v + (c1*r1*(self.pbest-self.x_pos))+(c2*r2*(self.gbest[i-1].reshape(-1,1)-self.x_pos))
            self.x_pos = (self.x_pos+v).astype(int)
            # self.x_pos = self.x_pos.astype(int)
            self.x_pos[self.x_pos<0] = self.x_pos[self.x_pos<0] + abs(self.x_pos[self.x_pos<0])

            # masukkan nilai pbest baru
            self.fitness, self.x_pos, startPos = self.fitSum(self.x_pos[0], self.x_pos[1], self.img)

            self.pbest[:,(self.pbest_val > self.fitness)] = self.pbest[:,(self.pbest_val > self.fitness)]
            self.pbest[:,(self.fitness > self.pbest_val)] = self.x_pos[:,(self.fitness > self.pbest_val)]

            self.pbest_val = np.array([self.pbest_val, self.fitness]).max(axis=0)

            self.index = self.pbest_val.argmax()

            self.gbest[i] = self.pbest[...,self.index]
            self.gbest_val[i] = self.pbest_val.max()
            # print(self.gbest_val, iterasi)

            # if i % iterasi-1 == 0:
                # fig, ax = plt.subplots(figsize=(3,3))
                # fig.tight_layout()
                # ax.imshow(self.img)
                # ax.plot(self.x_pos[0], self.x_pos[1], 'o', color='black')
                # ax.set_title(f't = {i}, optima {self.gbest_val[i]}, \ngbest {self.gbest[i]}')
                # self.dimensi_partikel(ax, startPos[0], startPos[1], self.windowX, self.windowY, edgeColor='black')
                # return fig
                # ax[1].set_title(f'Fitness Value = {self.gbest_val[i]}')
                # barplot = ax[1].bar(range(self.partikel), pbest_val/10000)
                # ax[1].bar_label(barplot, labels=pbest_val/10000, label_type='edge')
                # ax[1].imshow(self.img)
                # ax[1].plot(self.gbest[i,0], self.gbest[i,1], 'o', color='black')

                # plt.show()
                # return fig
        print('pso end')

    def createPath(self, x_init_end = 100, y_init_end=200):
        print('create path start')
        # radius_part = self.distance[self.distance != 0]
        # radius_part.shape

        # true_gbest_val = self.gbest_val[self.gbest_val != 0]
        # true_gbest_val.shape

        # jumlah path 
        shape = self.gbest_val[self.gbest_val != 0].shape[0]
        # inisialisasi variable path berisi array dimensi nx3
        self.path_point = np.zeros((shape,3), dtype='int32')

        # inisialisasi variable radius berisi array nx2
        radius = np.zeros((shape,2), dtype='int32')

        # dimensi kedua [1] berisi nilai index 
        radius[...,1] = np.array([i for i in range(radius.shape[0])])

        # inisialisasi array path plan yang berisi fitness, koordinat x, koordinat y, dan indexnya
        path_plan = np.zeros((shape,4), dtype='int32')
        path_plan[...,0] = self.gbest_val[self.gbest_val != 0]
        path_plan[...,1] = self.gbest[0:shape ,0]
        path_plan[...,2] = self.gbest[0:shape ,1]
        path_plan[...,3] = radius[...,1]

        # start point
        start_pointX = x_init_end
        start_pointY = y_init_end

        start_point = np.array([start_pointX, start_pointY], dtype='int')
        back_point = start_point

        # print(path_point.shape, start_point.shape, shape)

        self.path_point[0,0] = start_point[0]
        self.path_point[0,1] = start_point[1]
        self.path_point[shape-1,0] = back_point[0]
        self.path_point[shape-1,1] = back_point[1]

        # print(self.path_point.shape)

        for j in range(1,shape-1):
            # gunakan rumu pythagoras
            radius[...,0] = (start_point[0]-path_plan[...,1])**2+(start_point[1]-path_plan[..., 2])**2
            radius[...,0] = [sqrt(radius[i,0]) for i in range(radius.shape[0])]
            # urutkan berdasarkan jarak terdekat
            radius = radius[radius[...,0].argsort()]

            self.path_point[j,0] = path_plan[np.where(path_plan == radius[0,1])[0][0],1]
            self.path_point[j,1] = path_plan[np.where(path_plan == radius[0,1])[0][0],2]
            self.path_point[j,2] = radius[0,0]
            start_point = self.gbest[radius[0,1]]
            path_plan = np.delete(path_plan ,[np.where(path_plan == radius[0,1])[0][0]] ,axis=0)
            radius = np.delete(radius, [0], axis=0)
            radius = radius[radius[...,1].argsort()]
        print('create path done')
        
    def pathPlan(self):
        fig, ax = plt.subplots(figsize=(3,3))
        ax.imshow(self.img)
        ax.plot(self.path_point[...,0], self.path_point[...,1], linestyle='dashed', color='black')
        ax.plot(self.path_point[...,0], self.path_point[...,1], 'o', color='black')
        # print(path_point)
        # plt.show()
        return fig


# test_pso = PSO()
# test_pso.input_gambar('vari1.jpg')
# test_pso.input_partikel(20)
# test_pso.plotDimensionWindow()
# test_pso.startPSO(iterasi=11)
# test_pso.createPath(100,300)
# test_pso.pathPlan()