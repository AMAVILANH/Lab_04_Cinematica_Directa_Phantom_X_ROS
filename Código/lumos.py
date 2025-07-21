# pincher_control/control_servo.py
import rclpy
from rclpy.node import Node
from dynamixel_sdk import PortHandler, PacketHandler
import time

# Direcciones de registro en el AX-12A
ADDR_TORQUE_ENABLE    = 24
ADDR_MOVING_SPEED     = 32
ADDR_TORQUE_LIMIT     = 34
ADDR_PRESENT_POSITION = 36

class PincherController(Node):
    def __init__(self):
        super().__init__('pincher_controller')

        # Parámetros
        self.declare_parameter('port', '/dev/ttyUSB0')
        self.declare_parameter('baudrate', 1000000)
        self.declare_parameter('dxl_ids', [1, 2, 3, 4, 5])
        self.declare_parameter('moving_speed', 100)
        self.declare_parameter('torque_limit', 1000)
        self.declare_parameter('delay', 2.0)

        port_name     = self.get_parameter('port').value
        baudrate      = self.get_parameter('baudrate').value
        dxl_ids       = self.get_parameter('dxl_ids').value
        moving_speed  = self.get_parameter('moving_speed').value
        torque_limit  = self.get_parameter('torque_limit').value
        delay_seconds = self.get_parameter('delay').value

        # Inicializar comunicación
        port   = PortHandler(port_name)
        port.openPort()
        port.setBaudRate(baudrate)
        packet = PacketHandler(1.0)

        # 1) Configurar torque y velocidad para cada servo, sin moverlos
        for dxl_id in dxl_ids:
            # Limitar torque
            packet.write2ByteTxRx(port, dxl_id, ADDR_TORQUE_LIMIT, torque_limit)
            # Limitar velocidad
            packet.write2ByteTxRx(port, dxl_id, ADDR_MOVING_SPEED, moving_speed)
            # Habilitar torque
            packet.write1ByteTxRx(port, dxl_id, ADDR_TORQUE_ENABLE, 1)
            self.get_logger().info(f'[ID {dxl_id}] Torque activado, speed={moving_speed}, torque_limit={torque_limit}')

        # 2) Leer y mostrar posición actual
        for dxl_id in dxl_ids:
            pos, _, _ = packet.read2ByteTxRx(port, dxl_id, ADDR_PRESENT_POSITION)
            self.get_logger().info(f'[ID {dxl_id}] posición actual={pos}')

        # 3) Esperar un poco por si se desea observar el estado
        self.get_logger().info(f'Esperando {delay_seconds}s...')
        time.sleep(delay_seconds)

        # 4) Mantener torque activo (no apagarlo)
        # Si quieres apagarlo, descomenta:
        # for dxl_id in dxl_ids:
        #     packet.write1ByteTxRx(port, dxl_id, ADDR_TORQUE_ENABLE, 0)

        # 5) Cerrar puerto y terminar nodo
        port.closePort()
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    PincherController()

if __name__ == '__main__':
    main()