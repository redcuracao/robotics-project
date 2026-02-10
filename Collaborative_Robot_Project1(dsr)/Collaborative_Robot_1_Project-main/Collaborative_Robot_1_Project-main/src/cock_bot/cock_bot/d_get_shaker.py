import rclpy
import DR_init

# --------------------
# Robot Config
# --------------------
ROBOT_ID = "dsr01"
ROBOT_MODEL = "m0609"
ROBOT_TCP = "Tool Weight"      # TCP 이름
ROBOT_TOOL = "GripperDA_v1"    # Tool 이름

DR_init.__dsr__id = ROBOT_ID
DR_init.__dsr__model = ROBOT_MODEL


# --------------------
# Motion Parameters
# (DRL: set_velj / set_accj / set_velx / set_accx)
# --------------------
VEL_J = 60
ACC_J = 100

VEL_L = 250
ACC_L = 1000


# --------------------
# Robot Initialize
# --------------------
def initialize_robot():
    from DSR_ROBOT2 import set_tool, set_tcp

    print("#" * 50)
    print("Initializing robot for m4_get_shaker")
    print(f"ROBOT_ID    : {ROBOT_ID}")
    print(f"ROBOT_MODEL : {ROBOT_MODEL}")
    print("#" * 50)

    set_tool(ROBOT_TOOL)
    set_tcp(ROBOT_TCP)


# --------------------
# DSR Motion Functions
# --------------------
def shaker_grip():
    """DRL: shaker_grip"""
    from DSR_ROBOT2 import set_digital_output, wait

    set_digital_output(2, 0)   # OFF
    wait(0.2)
    set_digital_output(1, 1)   # ON
    wait(1.0)


def get_shaker():
    """DRL: get_shaker"""
    from DSR_ROBOT2 import movej, movel, posj, posx

    # MoveJNode
    movej(
        posj(-0.24, 6.74, 97.26, 2.63, 33.00, -87.63),
        vel=VEL_J,
        acc=ACC_J
    )

    # MoveJNode
    movej(
        posj(-0.42, 30.35, 123.52, -0.81, -61.43, -89.35),
        vel=VEL_J,
        acc=ACC_J
    )

    # MoveLNode (ABS)
    movel(
        posx(585.02, 1.26, 147.97, 179.93, -92.39, 90.06),
        vel=VEL_L,
        acc=ACC_L,
        ref=0,
        mod=0
    )


def get_out_shaker():
    """DRL: get_out_shaker"""
    from DSR_ROBOT2 import movel, posx

    # MoveLNode (REL)
    movel(
        posx(0.00, 0.00, 100.00, 0.00, 0.00, 0.00),
        vel=VEL_L,
        acc=ACC_L,
        ref=0,
        mod=1
    )

    # MoveLNode (ABS)
    movel(
        posx(422.55, 2.06, 300.62, 179.71, -97.15, 90.05),
        vel=VEL_L,
        acc=ACC_L,
        ref=0,
        mod=0
    )


# --------------------
# Sequence
# --------------------
def get_shaker_seq():
    from DSR_ROBOT2 import (
        set_singular_handling,
        set_velj,
        set_accj,
        set_velx,
        set_accx,
        DR_AVOID
    )

    # DRL: set_singular_handling / set_vel* / set_acc*
    set_singular_handling(DR_AVOID)
    set_velj(VEL_J)
    set_accj(ACC_J)
    set_velx(VEL_L, 80.625)
    set_accx(ACC_L, 322.5)

    # DRL loop body
    get_shaker()
    shaker_grip()
    get_out_shaker()


# --------------------
# Main
# --------------------
def main():
    rclpy.init()
    node = rclpy.create_node("m4_get_shaker_node", namespace=ROBOT_ID)
    DR_init.__dsr__node = node

    try:
        initialize_robot()
        get_shaker_seq()

    except KeyboardInterrupt:
        pass

    finally:
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
