import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import serial.tools.list_ports
import serial
import sys
import glob
import threading
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PSO_OOP1
import matplotlib.pyplot as plt
from tkinter import messagebox
import simulate 


PSO1 = PSO_OOP1.PSO()
simVrep = simulate.simulate()
fig, ax = plt.subplots()

global connectedSerial
connectedSerial = 0
global ports
ports = ''
global simsState, initState 
simsState = -1
initState = 1

global x_path, y_path
x_path = 0
y_path = 0 

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

window = tk.Tk()
window.resizable(width=False, height=False)
window.title("Serial Arduino")

serialInst = serial.Serial(baudrate='115200')

def turnOn():
    global connectedSerial
    serialInst.port = drop_listCom.get()
    serialInst.open()
    serialInst.write(b'o')
    connectedSerial = 1
    print(drop_listCom.get(), connectedSerial)

def turnOff():
    global connectedSerial
    connectedSerial = 0
    serialInst.close()
    lbl_serialStatusOn.config(bg='red', text='Disconnected')
    lbl_sprayStatusOn.config(bg='red', text='Off')

def select_file():

    path = filedialog.askopenfilename(title="Select an Image", filetype=(('Image Files','*.jpg .PNG .JPEG'),('All Files', '*.*')))
    ent_img.delete(0, 'end')
    ent_img.insert(0,path)
    window.after(1000, disImage)

def connectSerial():
    global connectedSerial
    while True:
        if connectedSerial == 1:
            lbl_serialStatusOn.config(background='green')
            data = serialInst.readline()

            # print(f'data = {data}')

            if data == b'o\r\n':
                lbl_sprayStatusOn.config(background='green', text='Connected')
                print(data)
            elif data == b'i\r\n':
                lbl_sprayStatusOn.config(background='red', text='Off')
        
def generatePath():
    if int(ent_c1.get()) <= 2 and int(ent_c2.get()) <= 2 and int(ent_jumlahParticle.get()) >= 80 and int(ent_jumlahiterasi.get())> 1:
        pathThreading = threading.Thread(target=dispPath)
        pathThreading.daemon = True
        pathThreading.start()
    else :
        messagebox.showwarning(title='Error', message='C1 dan C2 harus kurang dari atau sama dengan 2, Jumlah partikel minimal 80, jumlah iterasi minimal 2')


def disImage():
    if ent_img.get():
        img = PSO1.input_gambar(ent_img.get())
        ax1.clear()
        ax1.imshow(img)
        ax2.imshow(img)
        monitoringPath.draw()
        graph_image.draw()
    else:
        ax1.clear()
        graph_image.draw()
    # pass

def createPath(path_point, box, img):
    ax.clear()
    ax.imshow(img)
    
    ax.plot(path_point[:,0], path_point[:,1], linestyle='dashed', color='black')
    ax.plot(path_point[:,0], path_point[:,1], 'o', color='black')
    PSO1.dimensi_gbest(ax, box[:,0], box[:,1], box[:,2], box[:,3], edgeColor='black')

    print(PSO1.path_point)
    print(f'shape path point : {PSO1.path_point[:,1].shape[0]}')
    if PSO1.path_point.shape:    
        # createdPath.get_tk_widget().pack(side='left', fill='both')
        createdPath.draw()
        ent_coordinate.delete(0, 'end')
        ent_coordinate.insert(0,((path_point[:,0].flatten()-(img.shape[1]/2))/100, (path_point[:,1].flatten()-(img.shape[0]/2))/100))

def dispPath():
    global box
    PSO1.input_partikel(int(ent_jumlahParticle.get()))
    PSO1.startPSO(c1=int(ent_c1.get()), c2=int(ent_c2.get()), iterasi = int(ent_jumlahiterasi.get()))
    path_point, box, img = PSO1.createPath(100,300)
    createPath(path_point, box, img)
    
    # pass


def startEndSim():
    global simsState, initState
    if ent_coordinate.get():
        simsState *= -1
        if initState < 0 :
            initState *= -1

        print(f'state 1 : {simsState}, state 2 : {initState}')

def simulation():
    global simsState, initState, x_path, y_path, box
    # samplingStep = 0
    while True:
        if simsState > 0:
            # print(f'state 1 : {simsState}, state 2 : {initState}')
            if initState > 0 and  simsState > 0:
                x_coor =  (PSO1.path_point[:,0].flatten()-(PSO1.img.shape[1]/2))/100
                y_coor = (PSO1.path_point[:,1].flatten()-(PSO1.img.shape[0]/2))/100

                print(x_coor.shape)
                simVrep.initiateSim(x_coor, y_coor)
                # print(simVrep.posTargetX)
                initState *= -1
            if simVrep.clientID!=-1:
                simVrep.startSim()
                # samplingStep+=1
                # if samplingStep == 50 and simVrep.index < PSO1.path_point[:,0].flatten().shape[0]-1:
                    # print('hallo')
                # if simVrep.distance%0.5 == 0:
                x_path = (simVrep.x_int*100) + (PSO1.img.shape[1]/2)
                y_path = (simVrep.y_int*100) + (PSO1.img.shape[0]/2)

                # boxXMin = (box[:,0]-(PSO1.img.shape[1]/2))/100
                # boxXmax = ((box[:,0] + box[:,2])-(PSO1.img.shape[1]/2))/100
                # boxYMin = (box[:,1]-(PSO1.img.shape[0]/2))/100
                # boxYmax = ((box[:,1] + box[:,3])-(PSO1.img.shape[0]/2))/100
                # boxXMin = box[:,0]
                # boxXmax = (box[:,0] + box[:,2])
                # boxYMin = box[:,1]
                # boxYmax = (box[:,1] + box[:,3])
                    # print(f'x = {x}, y = {y}, distance = {simVrep.distance}')
                # print(f'y_min = {boxYMin[simVrep.index]}, y = {y_path}, y_max = { boxYmax[simVrep.index]}')
                # print(f'x_min = {boxXMin[simVrep.index]}, x = {x_path}, x_max = { boxXmax[simVrep.index]}')
                    # samplingStep = 0
                if simVrep.distance <= 0.08 and simVrep.index < PSO1.path_point[:,0].flatten().shape[0]-1 :
                    print('in here ?')
                    lbl_sprayStatusOn.config(background='green', text='Connected')
                    # p = b'1'
                    # serialInst.write(b'o')
                else:
                    lbl_sprayStatusOn.config(background='red', text='Off')


def plotMovement():
    global x_path, y_path
    while True:
        if x_path > 0 and y_path > 0:

        # ax2.clear()
        # ax2.imshow(img)
            ax2.plot(x_path, y_path, 'o', color='black')
            monitoringPath.draw()



# frame indicator dan command start
frm_indicator_cmd = ttk.Frame(master=window, relief='flat', borderwidth=2, padding=(10,10,10,10))
frm_indicator_cmd.pack()

# input
# input upload image
frm_inputImage = ttk.Frame(master=frm_indicator_cmd)
lbl_inputImage = ttk.Label(master=frm_inputImage, text="Upload Image")
frm_entryImage = ttk.Frame(master=frm_inputImage)
ent_img = ttk.Entry(master=frm_entryImage, width=20)
btn_img = ttk.Button(master=frm_entryImage, text="Browse Image", command=select_file)

lbl_inputImage.pack()
frm_entryImage.pack()
ent_img.grid(row=0, column=0, sticky='w')
btn_img.grid(row=0, column=1, sticky='e')

# input jumlah particle
frm_particle = ttk.Frame(master=frm_indicator_cmd)
lbl_jumlahParticle = ttk.Label(master=frm_particle, text="Jumlah Partikel")
frm_particle_input = ttk.Frame(master=frm_particle)
ent_jumlahParticle = ttk.Entry(master=frm_particle_input, width=20)
# btn_jumlahParticle = ttk.Button(master=frm_particle_input, text="Generate", command=generateParticle)

lbl_jumlahParticle.pack()
frm_particle_input.pack()
ent_jumlahParticle.grid(row=0, column=0, sticky='e', padx=5)
# btn_jumlahParticle.grid(row=0, column=1, sticky='w', padx=5)

# input jumlah iterasi
frm_iterasi = ttk.Frame(master=frm_indicator_cmd)
lbl_jumlahiterasi = ttk.Label(master=frm_iterasi, text="Jumlah Iterasi")
frm_iterasi_input = ttk.Frame(master=frm_iterasi)
ent_jumlahiterasi = ttk.Entry(master=frm_iterasi_input, width=20)

lbl_jumlahiterasi.pack()
frm_iterasi_input.pack()
ent_jumlahiterasi.grid(row=0, column=0, sticky='e', padx=5)

# input C1 dan C2
frm_Cvar = ttk.Frame(master=frm_indicator_cmd)
frm_ent_cvar = ttk.Frame(master=frm_Cvar)
btn_Cvar = ttk.Button(master=frm_Cvar, text="Generate", width=20, command=generatePath)
lbl_c1 = ttk.Label(master=frm_ent_cvar, text='C1')
ent_c1 = ttk.Entry(master=frm_ent_cvar, width=10)
lbl_c2 = ttk.Label(master=frm_ent_cvar, text='C2')
ent_c2 = ttk.Entry(master=frm_ent_cvar, width=10)

frm_ent_cvar.pack()
btn_Cvar.pack(pady=4)
lbl_c1.grid(row=1, column=0, padx=2)
ent_c1.grid(row=1, column=1, padx=2)
lbl_c2.grid(row=1, column=2, padx=2)
ent_c2.grid(row=1, column=3, padx=2)


# Dropdown Connect 
def serialPorts(): 
    print('masuk thread serial ports')
    while True:
        ports = serial_ports()
        drop_listCom.config(values=ports)

frm_btn_ledSerial = ttk.Frame(master=frm_indicator_cmd)
lbl_Serial = ttk.Label(master=frm_btn_ledSerial, text= "Serial Connection")
frm_btn_Serial = ttk.Frame(master=frm_btn_ledSerial)
drop_listCom = ttk.Combobox(
    master=frm_btn_Serial,
    state='readonly',
    values=ports
)

if ports == True:
    drop_listCom.set(ports[0])
lbl_Serial.pack()
frm_btn_Serial.pack()
drop_listCom.pack()


frm_btn_Connect = ttk.Frame(master=frm_indicator_cmd)
btn_ledCon = ttk.Button(master=frm_btn_Connect,
                      text="Connect", width=20, command=turnOn)
btn_ledDisc = ttk.Button(master=frm_btn_Connect,
                       text="Disconnect", width=20, command=turnOff)

btn_ledCon.pack(pady=2)
btn_ledDisc.pack()

# Serial status
frm_serialStatus = ttk.Frame(master=frm_indicator_cmd)
lbl_srialIndicator = tk.Label(master=frm_serialStatus, text="MCU Indicator")
frm_ledSerialIndicator = ttk.Frame(master=frm_serialStatus)
lbl_serialStatusOn = tk.Label(
    master=frm_ledSerialIndicator, text="Connected", width=20, bg='red')
# lbl_serialStatusOff = tk.Label(
#     master=frm_ledSerialIndicator, text="Disconnected", width=20)

lbl_srialIndicator.pack()
frm_ledSerialIndicator.pack()
lbl_serialStatusOn.grid(row=0, column=0, sticky='e')
# lbl_serialStatusOff.grid(row=0, column=1, sticky='w')

# spray indicator
frm_sprayStatus = ttk.Frame(master=frm_indicator_cmd)
lbl_sprayIndicator = tk.Label(master=frm_sprayStatus, text="Sprayer Indicator")
frm_ledsprayIndicator = ttk.Frame(master=frm_sprayStatus)
lbl_sprayStatusOn = tk.Label(
    master=frm_ledsprayIndicator, text="Off", width=20,bg='red')
# lbl_sprayStatusOff = tk.Label(
#     master=frm_ledsprayIndicator, text="Disconnected", width=20)

lbl_sprayIndicator.pack()
frm_ledsprayIndicator.pack()
lbl_sprayStatusOn.grid(row=0, column=0, sticky='e')
# lbl_sprayStatusOff.grid(row=0, column=1, sticky='w')

# position
frm_inputImage.grid(row=0, column=0, padx=10, pady=2)
frm_particle.grid(row=1, column=0, padx=10)
frm_iterasi.grid(row=0, column=1, padx=10)
frm_Cvar.grid(row=1, column=1, padx=2, pady=2)
frm_btn_ledSerial.grid(row=0, column=3, padx=5)
frm_btn_Connect.grid(row=1, column=3)
frm_serialStatus.grid(row=0, column=4, pady=2)
frm_sprayStatus.grid(row=1, column=4)
# frame indicator dan command end

# frame img
frm_main_disp = ttk.Frame(master=window)
frm_main_disp.pack()
frm_display = ttk.Frame(master=frm_main_disp)
frm_display.pack(pady=10)

frm_disp_upper = ttk.Frame(master=frm_display)
frm_disp_bottom = ttk.Frame(master=frm_display)

frm_disp_upper.pack(fill='both')
frm_disp_bottom.pack(fill='both')

fig1, ax1 = plt.subplots(figsize=(3,3))
graph_image = FigureCanvasTkAgg(fig1
    , frm_disp_upper)
graph_image.get_tk_widget().pack(side='left', fill='both', expand=True)

fig, ax = plt.subplots(figsize=(3,3))
createdPath = FigureCanvasTkAgg(master=frm_disp_upper, figure = fig)
createdPath.get_tk_widget().pack(side='left', fill='both')

fig2, ax2 = plt.subplots(figsize=(3,3))
monitoringPath = FigureCanvasTkAgg(master=frm_disp_bottom, figure = fig2)
monitoringPath.get_tk_widget().pack(fill='both')

# frame img end

# frame disply koordinat
frm_coordinate = ttk.Frame(master=frm_main_disp)
frm_coordinate.pack(pady=10)
lbl_coordinate = ttk.Label(master=frm_coordinate, text="Coordinate")
frm_coordinate_ent = ttk.Frame(frm_coordinate)
ent_coordinate = ttk.Entry(master=frm_coordinate_ent, width=70)
btn_startSim = ttk.Button(master=frm_coordinate_ent, text="Start Simulation", command=startEndSim)

lbl_coordinate.pack()
frm_coordinate_ent.pack()

ent_coordinate.grid(row=0, column=0)
btn_startSim.grid(row=0, column=1)

# threading start
serialState = threading.Thread(target=connectSerial)
serialState.daemon = True
serialState.start()
serialPort = threading.Thread(target=serialPorts)
serialPort.daemon = True
serialPort.start()

simThread = threading.Thread(target=simulation)
simThread.daemon = True
simThread.start()

plotThread = threading.Thread(target=plotMovement)
plotThread.daemon = True
plotThread.start()


# threading end

window.mainloop()
