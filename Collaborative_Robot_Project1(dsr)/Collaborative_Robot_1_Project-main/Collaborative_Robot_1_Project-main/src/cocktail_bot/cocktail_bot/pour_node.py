import rclpy
import DR_init
# from std_msgs.msg import String

# def command_cb(msg):
#     if msg.data != "START":
#         return

#     perform_task()
#     done_pub.publish(String(data="DONE"))

# ------------------------------
# Robot config
# ------------------------------
ROBOT_ID = "dsr01"
ROBOT_MODEL = "m0609"
ROBOT_TOOL = "Tool Weight"
ROBOT_TCP = "GripperDA"

DR_init.__dsr__id = ROBOT_ID
DR_init.__dsr__model = ROBOT_MODEL


# ------------------------------
# Init
# ------------------------------
def initialize_robot():
    from DSR_ROBOT2 import set_tool, set_tcp

    print("#" * 50)
    print("Initializing pour_drink_node")
    print(f"ROBOT_ID: {ROBOT_ID}")
    print("#" * 50)

    set_tool(ROBOT_TOOL)
    set_tcp(ROBOT_TCP)


# ------------------------------
# Gripper
# ------------------------------
def shaker_grip():
    from DSR_ROBOT2 import set_digital_output, wait
    ON, OFF = 1, 0

    set_digital_output(1, ON)
    wait(0.20)
    set_digital_output(2, OFF)


def shaker_ungrip():
    from DSR_ROBOT2 import set_digital_output, wait
    ON, OFF = 1, 0

    set_digital_output(1, OFF)
    wait(0.20)
    set_digital_output(2, ON)


# ------------------------------
# Motion blocks
# ------------------------------
def grip_up_shaker():
    from DSR_ROBOT2 import movej, movel, posj, posx, DR_MV_MOD_REL

    movej(
        posj(-0.40, 38.91, 106.59, -0.81, -53.22, -89.25),
        radius=0.0
    )

    shaker_grip()

    movel(
        posx(0.0, 0.0, 110.0, 0.0, 0.0, 0.0),
        ref=0,
        mod=DR_MV_MOD_REL
    )


def move_and_pour_drink():
    from DSR_ROBOT2 import movej, movel, posj, posx, wait, DR_MV_MOD_REL

    # 앞으로 이동
    movel(
        posx(0.0, 120.0, 0.0, 0.0, 0.0, 0.0),
        radius=50.0,
        ref=0,
        mod=DR_MV_MOD_REL
    )

    # 손목 회전 (pour)
    movej(
        posj(0.0, 0.0, 0.0, 0.0, 0.0, -120.0),
        mod=DR_MV_MOD_REL
    )

    wait(1.5)

    # 내려주기
    movel(
        posx(0.0, 0.0, -50.0, 0.0, 0.0, 0.0),
        ref=0,
        mod=DR_MV_MOD_REL
    )


def move_back_shaker_point():
    from DSR_ROBOT2 import movej, movel, posj, posx, DR_MV_MOD_REL

    movel(
        posx(0.0, 0.0, 50.0, 0.0, 0.0, 0.0),
        ref=0,
        mod=DR_MV_MOD_REL
    )

    movej(
        posj(0.0, 0.0, 0.0, 0.0, 0.0, 120.0),
        mod=DR_MV_MOD_REL
    )

    movel(
        posx(0.0, -120.0, 0.0, 0.0, 0.0, 0.0),
        ref=0,
        mod=DR_MV_MOD_REL
    )

    movel(
        posx(0.0, 0.0, -110.0, 0.0, 0.0, 0.0),
        ref=0,
        mod=DR_MV_MOD_REL
    )


# ------------------------------
# Main task
# ------------------------------
def perform_task():
    from DSR_ROBOT2 import (
        set_singular_handling,
        set_velj,
        set_accj,
        set_velx,
        set_accx,
        DR_AVOID,
    )

    set_singular_handling(DR_AVOID)
    set_velj(30.0)
    set_accj(200.0)
    set_velx(100.0, 68.25)
    set_accx(200.0, 273.0)

    grip_up_shaker()
    move_and_pour_drink()
    move_back_shaker_point()
    shaker_ungrip()


# ------------------------------
# ROS2 entry
# ------------------------------
def main(args=None):
    # global done_pub

    rclpy.init(args=args)
    node = rclpy.create_node("pour_drink_node", namespace=ROBOT_ID)
    DR_init.__dsr__node = node

    try:
        initialize_robot()
        perform_task()
        # done_pub = node.create_publisher(String, '/pour/done', 10)
        # node.create_subscription(String, '/pour/command', command_cb, 10)
        
    except KeyboardInterrupt:
        print("\nInterrupted by user")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        rclpy.shutdown()


if __name__ == "__main__":
    main()
