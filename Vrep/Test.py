import sim
import time
import numpy as np

print ('Program started')
clientID=sim.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to CoppeliaSim

if clientID!=-1:
    print ('Connected to remote API server')
else:
    print ('Failed connecting to remote API server')

time.sleep(2)

# setting handles   
res, cube = sim.simxGetObjectHandle(clientID, 'Cuboid', sim.simx_opmode_oneshot_wait)
res, cubePos = sim.simxGetObjectPosition(clientID, cube, -1, sim.simx_opmode_oneshot_wait)

x_int = cubePos[0]
y_int = cubePos[1]
z_int = cubePos[2]

# res, motorKiri = sim.simxGetObjectHandle(clientID, 'MotorKiri', sim.simx_opmode_oneshot_wait)

# errorCode=sim.simxSetJointTargetVelocity(clientID,motorKiri,0, sim.simx_opmode_streaming)
# errorCode=sim.simxSetJointTargetVelocity(clientID,motorKanan,0, sim.simx_opmode_streaming)

t = time.time()

while(time.time()-t)<5:
    print(cubePos)

    # errorCode=sim.simxSetJointTargetVelocity(clientID,motorKiri,.5, sim.simx_opmode_streaming)
    # errorCode=sim.simxSetJointTargetVelocity(clientID,motorKanan,.5, sim.simx_opmode_streaming)

    # res, vel = sim.simxGetObjectVelocity(clientID, motorKanan, sim.simx_opmode_streaming)

    # print(f'Time : {time.time()-t}')

sim.simxFinish(clientID)