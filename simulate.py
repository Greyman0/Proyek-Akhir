from Vrep import sim
import time
import numpy as np
from math import *


print ('Program started')
clientID=sim.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to CoppeliaSim

if clientID!=-1:
    print ('Connected to remote API server')

    startTime=time.time()
    returCodeDrone, drone = sim.simxGetObjectHandle(clientID, 'Quadricopter_target', sim.simx_opmode_blocking)

    returnCodePos, pos = sim.simxGetObjectPosition(clientID, drone, -1, sim.simx_opmode_blocking)

    x_int = pos[0]
    y_int = pos[1]
    z_int = pos[2]

    index = 0

    posTargetX = np.array([-3.99, -4.24, -1.06,  2.59,  3.15, -4.59,  1.26,  4.47, -3.35, -0.21,
  1.35,  2.80, -0.43,  2.60, -3.99])
    posTargetY = np.array([-0.07, -2.01, -2.35, -2.67, -2.22, -1.65, -0.69, -0.95,  0.58,  1.51,
 -0.04,  0.74,  2.39,  1.22, -0.07])

    X = (x_int-posTargetX[index])**2
    Y = (y_int-posTargetY[index])**2

    t_stepX = 0

    distance = sqrt(X+Y)
    gradient = (posTargetY[index]-y_int)/(posTargetX[index]-x_int)
    print(gradient)
    if posTargetX[index] > x_int:
        t_stepX = 0.01
    elif posTargetX[index] < x_int:
        t_stepX = -0.01


    while time.time()-startTime < 1000:
        
        if distance > 0.04 and index <= posTargetX.shape[0]:
            x_int = x_int + t_stepX
            y_int = y_int + (t_stepX*gradient)
            sim.simxSetObjectPosition(clientID, drone, -1, [x_int, y_int, pos[2]], sim.simx_opmode_streaming)
            X = (x_int-posTargetX[index])**2
            Y = (y_int-posTargetY[index])**2
            distance = sqrt(X+Y)
            print(distance)
        elif index <= posTargetX.shape[0]:
            index +=1
            returnCodePos, pos = sim.simxGetObjectPosition(clientID, drone, -1, sim.simx_opmode_blocking)

            x_int = pos[0]
            y_int = pos[1]
            z_int = pos[2]

            X = (x_int-posTargetX[index])**2
            Y = (y_int-posTargetY[index])**2
            distance = sqrt(X+Y)

            gradient = (posTargetY[index]-y_int)/(posTargetX[index]-x_int)
            print(x_int,y_int,z_int, distance, gradient)
            if posTargetX[index] > x_int:
                t_stepX = 0.01
            elif posTargetX[index] < x_int:
                t_stepX = -0.01

                
        time.sleep(0.01)

    # Now send some data to CoppeliaSim in a non-blocking fashion:
    sim.simxAddStatusbarMessage(clientID,'Hello CoppeliaSim!',sim.simx_opmode_oneshot)

    # Before closing the connection to CoppeliaSim, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
    sim.simxGetPingTime(clientID)

    # Now close the connection to CoppeliaSim:
    sim.simxFinish(clientID)
else:
    print ('Failed connecting to remote API server')
print ('Program ended')