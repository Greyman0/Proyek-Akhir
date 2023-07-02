from Vrep import sim
import time
import numpy as np
from math import *

class simulate():
    def __init__(self):
        pass
        

    def initiateSim(self, coorX, coorY):
        print ('Program started')
        self.clientID=sim.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to CoppeliaSim


        if self.clientID!=-1:
            print ('Connected to remote API server')

            returCodeDrone, self.drone = sim.simxGetObjectHandle(self.clientID, 'Quadricopter_target', sim.simx_opmode_blocking)

            returnCodePos, self.pos = sim.simxGetObjectPosition(self.clientID, self.drone, -1, sim.simx_opmode_blocking)

            self.x_int = self.pos[0]
            self.y_int = self.pos[1]
            self.z_int = self.pos[2]

            self.index = 0

            self.posTargetX = coorX
            self.posTargetY = coorY
            self.X = (self.x_int-self.posTargetX[self.index])**2
            self.Y = (self.y_int-self.posTargetY[self.index])**2

            self.t_stepX = 0

            self.distance = sqrt(self.X+self.Y)
            self.gradient = (self.posTargetY[self.index]-self.y_int)/(self.posTargetX[self.index]-self.x_int)
            print(self.gradient)
            if self.posTargetX[self.index] > self.x_int:
                self.t_stepX = 0.01
            elif self.posTargetX[self.index] < self.x_int:
                self.t_stepX = -0.01
        # pass

    def startSim(self):
        
            
            # startTime=time.time()

            # while time.time()-startTime < 1000:
                    
            if self.distance > 0.03 and self.index < self.posTargetX.shape[0]:
                self.x_int = self.x_int + self.t_stepX
                self.y_int = self.y_int + (self.t_stepX*self.gradient)
                sim.simxSetObjectPosition(self.clientID, self.drone, -1, [self.x_int, self.y_int, self.pos[2]], sim.simx_opmode_streaming)
                self.X = (self.x_int-self.posTargetX[self.index])**2
                self.Y = (self.y_int-self.posTargetY[self.index])**2
                self.distance = sqrt(self.X+self.Y)
                print(self.distance)
            elif self.index < self.posTargetX.shape[0]-1:
                self.index +=1
                returnCodePos, self.pos = sim.simxGetObjectPosition(self.clientID, self.drone, -1, sim.simx_opmode_blocking)

                self.x_int = self.pos[0]
                self.y_int = self.pos[1]
                self.z_int = self.pos[2]

                X = (self.x_int-self.posTargetX[self.index])**2
                Y = (self.y_int-self.posTargetY[self.index])**2
                self.distance = sqrt(X+Y)

                self.gradient = (self.posTargetY[self.index]-self.y_int)/(self.posTargetX[self.index]-self.x_int)
                print(self.index)
                if self.posTargetX[self.index] > self.x_int:
                    self.t_stepX = 0.01
                elif self.posTargetX[self.index] < self.x_int:
                    self.t_stepX = -0.01

                    
            time.sleep(0.01)

        #     # Now send some data to CoppeliaSim in a non-blocking fashion:
        #     sim.simxAddStatusbarMessage(self.clientID,'Hello CoppeliaSim!',sim.simx_opmode_oneshot)

        #     # Before closing the connection to CoppeliaSim, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
        #     sim.simxGetPingTime(self.clientID)

        #     # Now close the connection to CoppeliaSim:
        #     sim.simxFinish(self.clientID)
        # else:
        #     print ('Failed connecting to remote API server')

    def closeConnection(self):
        sim.simxFinish(self.clientID)
        print('Close Connection')
            
        
