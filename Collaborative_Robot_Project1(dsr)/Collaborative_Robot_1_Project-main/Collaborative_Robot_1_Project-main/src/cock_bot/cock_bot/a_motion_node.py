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
GLOBAL_DISPENSER_FIRST = None
GLOBAL_DISPENSER_SECOND = None
GLOBAL_DISPENSER_THIRD = None

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

def cocktail_sequence():
    from DSR_ROBOT2 import set_singular_handling, set_velj, set_ac

def get_shaker():
    from DSR_ROBOT2 import movej, movel, posj, posx

    movej(posj(-0.42, 30.35, 123.52, -0.81, -61.43, -89.35))
    movel(posx(586.13, 0.66, 146.01, 179.92, -92.28, 90.08))
    shaker_grip()
    movel(posx(0, 0, 100, 0, 0, 0), ref=0, mod=1)
    movel(posx(-120, 0, 0, 0, 0, 0), ref=0, mod=1)

def get_drink():
    from DSR_ROBOT2 import movel, wait, posx
    global Global_dispenser_first_point
    global Global_dispenser_second_point
    global Global_dispenser_third_point

    movel(Global_dispenser_first_point)
    wait(4.0)
    # movel(Global_dispenser_second_point)
    # wait(4.0)
    movel(Global_dispenser_third_point)
    wait(4.0)

def cocktail_sequence():
    from DSR_ROBOT2 import set_singular_handling, set_velj, set_accj, set_velx, set_accx, DR_AVOID
    set_singular_handling(DR_AVOID)
    set_velj(45.0)
    set_accj(70.0)
    set_velx(100.0, 68.25)
    set_accx(80.0, 273.0)
    
    get_shaker()
    shaker_grip()
    get_drink()


# --------------------
# Main
# --------------------
def main():
    global execute_flag
    global Global_dispenser_first_point
    global Global_dispenser_second_point
    global Global_dispenser_third_point

    rclpy.init()
    node = rclpy.create_node("m1_motion_node", namespace=ROBOT_ID)
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
        cocktail_sequence()

    except KeyboardInterrupt:
        pass

    finally:
        rclpy.shutdown()

if __name__ == "__main__":
    main()