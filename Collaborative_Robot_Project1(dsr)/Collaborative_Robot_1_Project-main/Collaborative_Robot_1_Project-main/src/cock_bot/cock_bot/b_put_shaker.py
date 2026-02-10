import rclpy
import DR_init

from std_msgs.msg import String

# --------------------
# Robot Config
# --------------------
ROBOT_ID = "dsr01"
ROBOT_MODEL = "m0609"
ROBOT_TCP = "Tool Weight" #본인 TCP 이름 설정
ROBOT_TOOL = "GripperDA_v1"  #본인 그리퍼 이름 설정

DR_init.__dsr__id = ROBOT_ID
DR_init.__dsr__model = ROBOT_MODEL

# 전역 포인트


# --------------------
# Robot Initialize
# --------------------
def initialize_robot():
    from DSR_ROBOT2 import set_tool, set_tcp, set_robot_mode, ROBOT_MODE_AUTONOMOUS

    print("#" * 50)
    print("Initializing robot for motion_node")
    print(f"ROBOT_ID: {ROBOT_ID}")
    print(f"ROBOT_MODEL: {ROBOT_MODEL}")
    print("#" * 50)

    set_tool(ROBOT_TOOL)
    set_tcp(ROBOT_TCP)

# --------------------
# DSR Motion Functions
# --------------------

def put_shaker():
    from DSR_ROBOT2 import movej, posj, movel, posx, DR_MV_MOD_REL, DR_MV_MOD_ABS

    movej(posj(-0.01, 19.67, 124.45, -0.16, -51.77, -89.24))
    movel(posx(582.00, -0.02, 192.31, 179.55, -92.27, 90.53), radius=0.00, ref=0, mod=DR_MV_MOD_ABS)
    movel(posx(0.00, 0.00, -55.00, 0.00, 0.00, 0.00), radius=0.00, ref=0, mod=DR_MV_MOD_REL)

def shaker_grip():
    from DSR_ROBOT2 import set_digital_output, wait
    set_digital_output(2, 0)
    wait(0.2)
    set_digital_output(1, 1)
    wait(0.5)

def shaker_ungrip():
    from DSR_ROBOT2 import set_digital_output, wait
    set_digital_output(1, 0)
    wait(0.2)
    set_digital_output(2, 1)
    wait(0.5)

def put_shaker_seq():
    from DSR_ROBOT2 import movel, posx, set_singular_handling, set_velj, set_accj, set_velx, set_accx, DR_AVOID, DR_MV_MOD_ABS
    set_singular_handling(DR_AVOID)
    set_velj(60.0)
    set_accj(100.0)
    set_velx(150.0, 68.25)
    set_accx(100.0, 273.0)

    put_shaker()
    shaker_ungrip()
    movel(posx(439.69, 0.26, 332.33, 179.14, -90.00, 91.07), radius=0.00, ref=0, mod=DR_MV_MOD_ABS)


# --------------------
# Main
# --------------------
def main():

    rclpy.init()
    node = rclpy.create_node("put_shaker_node", namespace=ROBOT_ID)
    DR_init.__dsr__node = node

    from DSR_ROBOT2 import posx
    Global_dispenser_first_point = posx(546.43, -85.13, 258.13, 87.00, -92.82, 89.05)
    Global_dispenser_second_point = posx(436.43, -85.13, 258.13, 87.00, -92.82, 89.05)
    Global_dispenser_third_point = posx(326.43, -85.13, 258.13, 87.00, -92.82, 89.05)

    # Doosan 노드 등록
    DR_init.__dsr__node = node

    print("Ready. Waiting for /cocktail_cmd")

    try:
        initialize_robot()
        put_shaker_seq()

    except KeyboardInterrupt:
        pass

    finally:
        rclpy.shutdown()

if __name__ == "__main__":
    main()
