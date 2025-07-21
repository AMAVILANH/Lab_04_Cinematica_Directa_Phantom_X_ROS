# hmi_pincher.py
import tkinter as tk
from tkinter import ttk
from dynamixel_sdk import PortHandler, PacketHandler
import time

# Parámetros Dynamixel
ADDR_PRESENT_POSITION = 36
ADDR_GOAL_POSITION = 30
ADDR_TORQUE_ENABLE = 24
ADDR_MOVING_SPEED = 32
ADDR_TORQUE_LIMIT = 34
DXL_IDS = [1, 2, 3, 4]
PORT = '/dev/ttyUSB0'
BAUDRATE = 1000000

# 5 poses (en grados)
POSES = {
    'Pose 1: [0, 0, 0, 0]':        [0, 0, 0, 0],
    'Pose 2: [25, 25, 20, -20]':   [25, 25, 20, -20],
    'Pose 3: [-35, 35, -30, 30]':  [-35, 35, -30, 30],
    'Pose 4: [85, -20, 55, 25]':   [85, -20, 55, 25],
    'Pose 5: [80, -35, 55, -45]':  [80, -35, 55, -45]
}

def grados_a_raw(grados):
    return int((grados + 150) * 1023 / 300)

def raw_a_grados(raw):
    return round((raw * 300 / 1023) - 150, 1)

class HMI:
    def __init__(self, root):
        self.root = root
        self.root.title("HMI - Phantom X Pincher")
        self.root.geometry("400x300")

        # Título y datos del grupo
        tk.Label(root, text="LABORATORIO 04 ", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(root, text="Juan Meza, Andrés Avilan, Hector Aponte, Manuel B", font=("Arial", 10)).pack()
        
        # Selector de poses
        self.pose_var = tk.StringVar(value=list(POSES.keys())[0])
        ttk.Combobox(root, textvariable=self.pose_var, values=list(POSES.keys()), width=40).pack(pady=10)

        # Botón para enviar pose
        tk.Button(root, text="Enviar al robot", command=self.enviar_pose).pack(pady=5)

        # Área de lectura de posiciones
        self.status = tk.Label(root, text="Valores actuales: q1=?, q2=?, q3=?, q4=?", font=("Courier", 10))
        self.status.pack(pady=10)

        self.port = PortHandler(PORT)
        self.packet = PacketHandler(1.0)
        self.inicializar_puerto()
        self.leer_posiciones()  # leer al iniciar

    def inicializar_puerto(self):
        if self.port.openPort():
            self.port.setBaudRate(BAUDRATE)
            for dxl_id in DXL_IDS:
                self.packet.write2ByteTxRx(self.port, dxl_id, ADDR_MOVING_SPEED, 100)
                self.packet.write2ByteTxRx(self.port, dxl_id, ADDR_TORQUE_LIMIT, 800)
                self.packet.write1ByteTxRx(self.port, dxl_id, ADDR_TORQUE_ENABLE, 1)
        else:
            print("No se pudo abrir el puerto")

    def enviar_pose(self):
        pose = POSES[self.pose_var.get()]
        for i, dxl_id in enumerate(DXL_IDS):
            raw = grados_a_raw(pose[i])
            self.packet.write2ByteTxRx(self.port, dxl_id, ADDR_GOAL_POSITION, raw)
            time.sleep(0.1)
        self.leer_posiciones()

    def leer_posiciones(self):
        posiciones = []
        for dxl_id in DXL_IDS:
            pos, _, _ = self.packet.read2ByteTxRx(self.port, dxl_id, ADDR_PRESENT_POSITION)
            posiciones.append(raw_a_grados(pos))
        self.status.config(text=f"Valores actuales: q1={posiciones[0]}°, q2={posiciones[1]}°, q3={posiciones[2]}°, q4={posiciones[3]}°")

if __name__ == '__main__':
    root = tk.Tk()
    app = HMI(root)
    root.mainloop()
