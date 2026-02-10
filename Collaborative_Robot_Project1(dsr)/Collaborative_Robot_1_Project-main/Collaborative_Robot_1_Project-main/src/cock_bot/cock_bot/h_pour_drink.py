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
VEL_J = 30
ACC_J = 200

VEL_L = 100
ACC_L = 200


# --------------------
# Robot Initialize
# --------------------
def initialize_robot():
    from DSR_ROBOT2 import set_tool, set_tcp

    print("#" * 50)
    print("Initializing robot for m8_pour_drink")
    print(f"ROBOT_ID    : {ROBOT_ID}")
    print(f"ROBOT_MODEL : {ROBOT_MODEL}")
    print("#" * 50)

    set_tool(ROBOT_TOOL)
    set_tcp(ROBOT_TCP)


# --------------------
# DSR Motion / IO Functions
# --------------------
def shaker_grip():
    """DRL: shaker_grip"""
    from DSR_ROBOT2 import set_digital_output, wait
    set_digital_output(1, 1)   # ON
    wait(0.2)
    set_digital_output(2, 0)   # OFF


def shaker_ungrip():
    """DRL: shaker_ungrip"""
    from DSR_ROBOT2 import set_digital_output, wait
    set_digital_output(1, 0)   # OFF
    wait(0.2)
    set_digital_output(2, 1)   # ON


def grip_up_shaker():
    """DRL: grip_up_shaker"""
    from DSR_ROBOT2 import movej, movel, posj, posx

    movej(
        posj(-0.40, 38.91, 106.59, -0.81, -53.22, -89.25),
        vel=VEL_J,
        acc=ACC_J
    )

    shaker_grip()

    movel(
        posx(0.00, 0.00, 110.00, 0.00, 0.00, 0.00),
        vel=VEL_L,
        acc=ACC_L,
        ref=0,
        mod=1
    )


def move_and_pour_drink():
    """DRL: move_and_pour_drink"""
    from DSR_ROBOT2 import movel, amovej, posx, posj, wait

    # MoveLNode (REL) – approach pour position
    movel(
        posx(0.00, 105.00, 0.00, 0.00, 0.00, 0.00),
        vel=VEL_L,
        acc=ACC_L,
        ref=0,
        mod=1,
        radius=50.0
    )

    

    # AMoveJNode (REL) – rotate wrist for pouring
    amovej(
        posj(0.00, 0.00, 0.00, 0.00, 0.00, -120.00),
        mod=1
    )

    wait(1.5)

    # MoveLNode (REL) – pour down
    movel(
        posx(0.00, 0.00, -50.00, 0.00, 0.00, 0.00),
        vel=VEL_L,
        acc=ACC_L,
        ref=0,
        mod=1
    )

    wait(1.0)

def move_back_shaker_point():
    """DRL: move_back_shaker_point"""
    from DSR_ROBOT2 import amovel, movej, movel, posx, posj

    # AMoveLNode (REL) – lift up
    amovel(
        posx(0.00, 0.00, 50.00, 0.00, 0.00, 0.00),
        ref=0,
        mod=1
    )

    # MoveJNode (REL) – rotate back
    movej(
        posj(0.00, 0.00, 0.00, 0.00, 0.00, 120.00),
        vel=VEL_J,
        acc=ACC_J,
        mod=1
    )

    # MoveLNode (REL) – retreat from pour position
    movel(
        posx(0.00, -105.00, 0.00, 0.00, 0.00, 0.00),
        vel=VEL_L,
        acc=ACC_L,
        ref=0,
        mod=1
    )

    # MoveLNode (REL) – 내려놓기 높이
    movel(
        posx(0.00, 0.00, -110.00, 0.00, 0.00, 0.00),
        vel=VEL_L,
        acc=ACC_L,
        ref=0,
        mod=1
    )


# --------------------
# Sequence
# --------------------
def pour_drink_seq():
    from DSR_ROBOT2 import (
        movej,
        posj,
        set_singular_handling,
        set_velj,
        set_accj,
        set_velx,
        set_accx,
        DR_AVOID
    )

    # DRL: global motion settings
    set_singular_handling(DR_AVOID)
    set_velj(VEL_J)
    set_accj(ACC_J)
    set_velx(VEL_L, 68.25)
    set_accx(ACC_L, 273.0)

    grip_up_shaker()
    move_and_pour_drink()
    move_back_shaker_point()
    shaker_ungrip()

    # MoveJNode – retreat
    movej(
        posj(-0.41, -4.49, 108.21, 4.44, 44.88, -84.86),
        vel=VEL_J,
        acc=ACC_J
    )

    # MoveJNode – home
    movej(
        posj(0.00, 0.00, 90.00, 0.00, 90.00, 0.00),
        vel=VEL_J,
        acc=ACC_J
    )


# --------------------
# Main
# --------------------
def main():
    rclpy.init()
    node = rclpy.create_node("m8_pour_drink_node", namespace=ROBOT_ID)
    DR_init.__dsr__node = node

    try:
        initialize_robot()
        pour_drink_seq()

    except KeyboardInterrupt:
        pass

    finally:
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
