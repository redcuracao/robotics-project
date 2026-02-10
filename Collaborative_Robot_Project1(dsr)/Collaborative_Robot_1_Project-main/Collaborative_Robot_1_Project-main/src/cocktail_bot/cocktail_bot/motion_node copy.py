import rclpy
import DR_init
from std_msgs.msg import String

def command_cb(msg):
    if msg.data != "START":
        return

    perform_task()
    done_pub.publish(String(data="DONE"))

# 로봇 설정 상수
ROBOT_ID = "dsr01"
ROBOT_MODEL = "m0609"
ROBOT_TOOL = "Tool Weight"
ROBOT_TCP = "GripperDA"

DR_init.__dsr__id = ROBOT_ID
DR_init.__dsr__model = ROBOT_MODEL


def initialize_robot():
    from DSR_ROBOT2 import set_tool, set_tcp

    print("#" * 50)
    print("Initializing robot for motion_node")
    print(f"ROBOT_ID: {ROBOT_ID}")
    print(f"ROBOT_MODEL: {ROBOT_MODEL}")
    print("#" * 50)

    set_tool(ROBOT_TOOL)
    set_tcp(ROBOT_TCP)


# ------------------------------
#   Global variables (초기화는 main()에서 한다)
# ------------------------------
Global_shaker_point = None
Global_dispenser_first_point = None
Global_dispenser_second_point = None
Global_dispenser_third_point = None


# ------------------------------
#   Sub Functions (grip/ungrip)
# ------------------------------
def shaker_grip():
    from DSR_ROBOT2 import set_digital_output, wait
    ON = 1
    OFF = 0

    set_digital_output(2, OFF)
    wait(0.20)
    set_digital_output(1, ON)
    wait(0.50)


def shaker_ungrip():
    from DSR_ROBOT2 import set_digital_output, wait
    ON = 1
    OFF = 0

    set_digital_output(1, OFF)
    wait(0.20)
    set_digital_output(2, ON)
    wait(0.50)


# ------------------------------
#   High-level Functions
# ------------------------------
def get_shaker():
    from DSR_ROBOT2 import movej, movel, posx, posj, wait, DR_MV_MOD_ABS, DR_MV_MOD_REL

    global Global_shaker_point

    movej(posj(-0.42, 30.35, 123.52, -0.81, -61.43, -89.35), radius=20.0)

    movel(
        posx(586.13, 0.66, 146.01, 179.92, -92.28, 90.08),
        radius=0.0,
        ref=0,
        mod=DR_MV_MOD_ABS,
    )

    shaker_grip()

    movel(
        posx(0.0, 0.0, 100.0, 0.0, 0.0, 0.0),
        radius=50.0,
        ref=0,
        mod=DR_MV_MOD_REL,
    )

    movel(
        posx(-100.0, 0.0, 0.0, 0.0, 0.0, 0.0),
        radius=0.0,
        ref=0,
        mod=DR_MV_MOD_REL,
    )


def get_drink():
    from DSR_ROBOT2 import movel, wait, DR_MV_MOD_ABS

    global Global_dispenser_first_point
    global Global_dispenser_second_point
    global Global_dispenser_third_point

    movel(Global_dispenser_first_point, radius=0.0, ref=0, mod=DR_MV_MOD_ABS)
    wait(4.0)

    movel(Global_dispenser_second_point, radius=0.0, ref=0, mod=DR_MV_MOD_ABS)
    wait(4.0)

    movel(Global_dispenser_third_point, radius=0.0, ref=0, mod=DR_MV_MOD_ABS)
    wait(4.0)

# def put_shaker():
#     from DSR_ROBOT2 import posx, posj, movej, movel, DR_MV_MOD_REL

#     # MoveJ #1
#     movej(posj(-24.65, -24.51, 104.93, 31.44, 54.92, -124.97), radius=0.0)

#     # MoveJ #2
#     movej(posj(-0.4, 38.91, 106.59, -0.81, -53.22, -89.25), radius=0.0)

#     # MoveL (REL)
#     movel(
#         posx(0.0, 0.0, -100.0, 0.0, 0.0, 0.0),
#         radius=0.0,
#         ref=0,
#         mod=DR_MV_MOD_REL
#     )

#     shaker_ungrip()


# ------------------------------
#   Main Task Executor
# ------------------------------
def perform_task():
    from DSR_ROBOT2 import set_singular_handling, set_velj, set_accj, set_velx, set_accx, DR_AVOID

    set_singular_handling(DR_AVOID)
    set_velj(45.0)
    set_accj(70.0)

    set_velx(100.0, 68.25)
    set_accx(80.0, 273.0)

    get_shaker()
    get_drink()
    # put_shaker()


def main(args=None):
    global Global_shaker_point
    global Global_dispenser_first_point
    global Global_dispenser_second_point
    global Global_dispenser_third_point
    global done_pub

    rclpy.init(args=args)
    node = rclpy.create_node("motion_node", namespace=ROBOT_ID)
    DR_init.__dsr__node = node

    # ---------------------------
    # DSR_ROBOT2 import (이 시점에서 해야 함!)
    # ---------------------------
    from DSR_ROBOT2 import posx, posj

    # ---------------------------
    # Global posx 초기화
    # ---------------------------
    Global_shaker_point = posx(500.0, 0.0, 100.0, 0.22, 90.00, -90.00)
    Global_dispenser_first_point  = posx(546.43, -85.13, 258.13, 87.00, -92.82, 89.05)
    Global_dispenser_second_point = posx(436.43, -85.13, 258.13, 87.00, -92.82, 89.05)
    Global_dispenser_third_point  = posx(326.43, -85.13, 258.13, 87.00, -92.82, 89.05)

    try:
        initialize_robot()
        # perform_task()
        done_pub = node.create_publisher(String, '/motion/done', 10)
        node.create_subscription(String, '/motion/command', command_cb, 10)

    except KeyboardInterrupt:
        print("\nUser interrupted. Shutting down...")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        rclpy.shutdown()


if __name__ == "__main__":
    main()
