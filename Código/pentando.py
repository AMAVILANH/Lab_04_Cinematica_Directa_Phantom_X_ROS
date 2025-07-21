#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from dynamixel_sdk import PortHandler, PacketHandler
import numpy as np
import time
import matplotlib.pyplot as plt
from phantom_dh import crear_robot_phantom  # ← Tu modelo DH personalizado

class SimuladorPincher(Node):
    def __init__(self):
        super().__init__('simulador_pincher')

        dxl_ids = [1, 2, 3, 4]  # IDs Dynamixel
        pose = [25, 25, 20, -20]  # ← Cambia según la pose que quieras graficar

        port = PortHandler('/dev/ttyUSB0')
        packet = PacketHandler(1.0)
        port.openPort()
        port.setBaudRate(1000000)

        # Configura torque, velocidad, posición
        for i, dxl_id in enumerate(dxl_ids):
            packet.write2ByteTxRx(port, dxl_id, 34, 800)      # Torque limit
            packet.write2ByteTxRx(port, dxl_id, 32, 100)      # Velocidad
            packet.write1ByteTxRx(port, dxl_id, 24, 1)        # Enable torque
            valor_raw = self.angulo_a_raw(pose[i])
            packet.write2ByteTxRx(port, dxl_id, 30, valor_raw)
            self.get_logger().info(f'[ID {dxl_id}] → {pose[i]}° → raw {valor_raw}')
            time.sleep(0.5)

        # GRAFICAR con Toolbox
        robot = crear_robot_phantom()
        q_rad = np.radians(pose)
        robot.plot(q_rad, backend='pyplot', block=True)

        port.closePort()
        rclpy.shutdown()

    def angulo_a_raw(self, grados):
        # Convierte de -150° a 150° → 0–1023
        return int((grados + 150) * 1023 / 300)

def main(args=None):
    rclpy.init(args=args)
    SimuladorPincher()

if __name__ == '__main__':
    main()
