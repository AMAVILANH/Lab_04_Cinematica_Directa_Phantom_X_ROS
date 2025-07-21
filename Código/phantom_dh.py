from roboticstoolbox import DHRobot, RevoluteDH
import numpy as np

def crear_robot_phantom():
    L1 = 0.15205
    L2 = 0.13682
    L3 = 0.07412
    L4 = 0.1084

    return DHRobot([
        RevoluteDH(d=L1, a=0,     alpha=np.pi/2),
        RevoluteDH(d=0,  a=L2,    alpha=0, offset=np.pi/2),  # q2 + 90°
        RevoluteDH(d=0,  a=L3,    alpha=0),
        RevoluteDH(d=0,  a=L4,    alpha=0),
    ], name='Phantom_X_Pincher')
