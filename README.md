# Laboratorio 4 - Cinemática Directa con ROS 2
## PhantomX Pincher X100 | Mecatrónica UNAL 2025-I

### Integrantes del Grupo
Esta práctica se llevó a cabo con la participación conjunta de los integrantes de dos grupos de laboratorio.

| Andrés Mauricio Avilán |
| Juan David Meza |
| Hector Andrés Aponte Porras |
| Juan Manuel Barrero |

---

## Modelado Cinemático

El modelado matemático del manipulador incluye:

![Foto 1](Imagenes/01.jpg)


## Tabla de parámetros DH estándar (Denavit–Hartenberg)

  Este modelo representa el brazo robótico **Phantom X Pincher** utilizando la biblioteca `roboticstoolbox` de Peter Corke. Se basa en la convención **Denavit–Hartenberg (DH clásico)** para describir la cinemática directa del robot.

### Descripción general

- Se usa el modelo `DHRobot` con articulaciones `RevoluteDH`.
- Las longitudes de los eslabones están en metros.
- Se aplica un **offset de +90° (π/2 rad)** en la segunda articulación para alinear el modelo con la configuración real del robot.

### Estructura del robot

| Articulación | a [m]   | α [rad]  | d [m]    | θ [rad] (variable) | Offset [rad] |
|--------------|---------|----------|----------|---------------------|--------------|
| 1            | 0       | π/2      | 0.15205  | θ₁                  | 0            |
| 2            | 0.13682 | 0        | 0        | θ₂                  | π/2          |
| 3            | 0.07412 | 0        | 0        | θ₃                  | 0            |
| 4            | 0.1084  | 0        | 0        | θ₄                  | 0            |

> 💡 **Nota:** La cuarta articulación representa un eslabón final (efector) sin desplazamiento `d` ni torsión, pero con longitud `a` correspondiente al último tramo.

---

## Descripción de la Solución Planteada

El script `macarena.py` desarrollado para controlar el manipulador PhantomX Pincher X100 está basado en ROS 2 y hace uso de los servicios de Dynamixel para controlar las articulaciones del brazo.

---

## Diagrama de Flujo del script macarena.py`

```mermaid
flowchart TD
    A[INICIO] --> B[Inicializar el nodo de ROS]
    B --> C[Definir torques máximos por motor]
    C --> D[Configurar límites de torque con send_joint_command]
    D --> E[Llevar el robot a posición HOME]
    E --> F[Seleccionar configuración]
    F --> G{¿Configuración seleccionada?}
    G -->|1| H1[Aplicar CONFIGURACIÓN 1]
    G -->|2| H2[Aplicar CONFIGURACIÓN 2]
    G -->|3| H3[Aplicar CONFIGURACIÓN 3]
    G -->|4| H4[Aplicar CONFIGURACIÓN 4]
    H1 --> Z[FIN]
    H2 --> Z
    H3 --> Z
    H4 --> Z
```

## Configuración ROS 2 - `macarena`

Este proyecto está desarrollado en **ROS 2 Humble**, y usa el paquete `dynamixel_sdk` para la comunicación con los motores del manipulador.
Para lanzar el sistema completo:

ros2 launch phanthon_control macarena.py


### 🔧 Configuración de Torque y Análisis de Límites de Movimiento

Antes de realizar cualquier tipo de movimiento con el manipulador, fue necesario identificar tanto los **valores máximos de torque permitidos para cada motor** como los **límites físicos de movimiento** de cada articulación expresados en **pulsos y grados**.

#### Torques máximos permitidos por motor

Estos valores fueron ajustados empíricamente para asegurar un movimiento suave y seguro, evitando vibraciones y pérdida de fuerza en posiciones extremas:

```python
torques = [500, 400, 350, 350, 350]  # [waist, shoulder, elbow, wrist, gripper]
```

---

### Análisis de límites de pulsos y conversión a grados

Para tener control preciso sobre las articulaciones, se midieron los límites de pulsos y su correspondencia con ángulos reales, permitiendo definir rangos válidos y realizar conversiones confiables entre grados y pulsos. Este análisis fue clave para programar movimientos seguros, sin sobrepasar los límites físicos del robot.

| Articulación  | Pulsos mínimo-máximo | Rango Angular estimado | Pulsos para 90° |
|---------------|----------------------|-------------------------|------------------|
| **x1 (cadera)**   | 0 – 657               | ~0° – 205°               | 290              |
| **x2 (hombro)**   | 220 – 804             | ~0° – 180°               | 290              |
| **x3 (codo)**     | 80 – 944              | ~-45° – 225°             | 290              |
| **x4 (muñeca)**   | 200 – 824             | ~0° – 180°               | 312              |
| **x5 (gripper)**  | 0 – 512               | ~4 mm – 38 mm (apertura) | —                |

> Con esta tabla, fue posible establecer funciones de conversión entre grados ↔ pulsos para programar los movimientos con precisión, evitando zonas peligrosas de saturación o colisión entre eslabones.

---

### Función Setup_py
Este archivo setup.py es fundamental para definir cómo se construye, instala y ejecuta un paquete ROS 2 en Python:
```Python

from setuptools import find_packages, setup

package_name = 'pincher_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='juanmeza',
    maintainer_email='juanmeza@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'macarena = pincher_control.macarena:main',
            'control_servo = pincher_control.control_servo:main',
            'lumos = pincher_control.lumos:main',
            'pentando = pincher_control.pentando:main'
        ],
    },
)

```

**Parámetros**
- `package_name = 'pincher_control'
packages=find_packages(exclude=['test']),
` : Se declara que el paquete se llama pincher_control y se incluyen todos los submódulos Python dentro de esa carpeta, excepto los de pruebas. Esto le dice a ROS 2 qué código debe incluir.

- `entry_points={
    'console_scripts': [
        'macarena = pincher_control.macarena:main',
        ...
    ],
}
ros2 run pincher_control macarena
` : Cada línea enlaza un alias ejecutable (macarena, control_servo, etc.) con una función main() ubicada dentro del respectivo módulo Python.
---


### Función de Envío de Comandos

Se definió una función central llamada `macarena` para encapsular la lógica de comunicación con los motores Dynamixel:

```python

aqui todo codigo python

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

```

**Parámetros:**

- `port = PortHandler(port_name)
packet = PacketHandler(1.0)
`: El código usa dynamixel_sdk para conectarse con los motores mediante un puerto serie (/dev/ttyUSB0) y una velocidad de transmisión de 1 Mbps. Esto es esencial para que la comunicación entre el controlador y los servomotores sea posible.
- `ADDR_TORQUE_ENABLE = 24
ADDR_GOAL_POSITION = 30
ADDR_MOVING_SPEED = 32
ADDR_TORQUE_LIMIT  = 34
`: Estas direcciones son necesarias para enviar comandos correctos a cada motor, como habilitar torque, establecer velocidad, límite de torque y posición.
- `packet.write2ByteTxRx(..., ADDR_GOAL_POSITION, home_pos[i])
...
packet.write2ByteTxRx(..., ADDR_GOAL_POSITION, target_pos[i])
`: Esto demuestra cómo se puede controlar directamente cada articulación de un brazo robótico, con temporización (time.sleep) entre comandos para permitir que los motores lleguen a su posición..
- `class Macarena(Node):`: También, el uso de `rclpy.init()` y `rclpy.shutdown()` muestra cómo se gestiona el ciclo de vida del nodo, incluso si no hay suscriptores o editores, permitiendo control directo desde el nodo principal.
Esta función se usa para configurar torques, mover motores a HOME y moverlos a poses específicas.

---


### Video demostrativo

A continuación, se presenta el video de demostración con las poses programadas para el robot PhantomX Pincher X100:

[![Video](https://img.youtube.com/vi/1_Vng2bOtXY/0.jpg)](https://www.youtube.com/watch?v=1_Vng2bOtXY)


---

### Comparación de poses digitales vs reales

A continuación se muestra una tabla con las comparaciones entre la simulación digital y la fotografía real del manipulador:

![Foto 2](Imagenes/Panthom01.jpg)
![Foto 3](Imagenes/Panthom02.jpg)
![Foto 4](Imagenes/Panthom03.jpg)
![Foto 5](Imagenes/Panthom04.jpg)

