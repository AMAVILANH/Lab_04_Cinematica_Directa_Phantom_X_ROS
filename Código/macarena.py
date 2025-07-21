#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from dynamixel_sdk import PortHandler, PacketHandler
import time

ADDR_TORQUE_ENABLE    = 24
ADDR_GOAL_POSITION    = 30
ADDR_MOVING_SPEED     = 32
ADDR_TORQUE_LIMIT     = 34

class Macarena(Node):
    def __init__(self):
        super().__init__('macarena_node')

        port_name = '/dev/ttyUSB0'
        baudrate = 1000000
        dxl_ids = [1, 2, 3, 4]  # waist, shoulder, elbow, wrist
        home_pos = [512, 512, 512, 512]
        target_pos = [600, 600, 400, 300]
        speed = 100
        torque = 1000

        port = PortHandler(port_name)
        packet = PacketHandler(1.0)

        if not port.openPort():
            self.get_logger().error("No se pudo abrir el puerto")
            return
        port.setBaudRate(baudrate)

        # Mover a home
        self.get_logger().info("Moviendo a posición HOME...")
        for i, dxl_id in enumerate(dxl_ids):
            packet.write2ByteTxRx(port, dxl_id, ADDR_TORQUE_LIMIT, torque)
            packet.write2ByteTxRx(port, dxl_id, ADDR_MOVING_SPEED, speed)
            packet.write1ByteTxRx(port, dxl_id, ADDR_TORQUE_ENABLE, 1)
            packet.write2ByteTxRx(port, dxl_id, ADDR_GOAL_POSITION, home_pos[i])
            self.get_logger().info(f'[ID {dxl_id}] → {home_pos[i]}')
            time.sleep(1)

        time.sleep(2)

        # Mover a posición objetivo
        self.get_logger().info("Moviendo a posición OBJETIVO...")
        for i, dxl_id in enumerate(dxl_ids):
            packet.write2ByteTxRx(port, dxl_id, ADDR_GOAL_POSITION, target_pos[i])
            self.get_logger().info(f'[ID {dxl_id}] → {target_pos[i]}')
            time.sleep(1)

        time.sleep(2)

        port.closePort()
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    Macarena()

if __name__ == '__main__':
    main()
