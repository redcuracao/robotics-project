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
    print("Initializing robot for m6_put_shaker")
    print(f"ROBOT_ID    : {ROBOT_ID}")
    print(f"ROBOT_MODEL : {ROBOT_MODEL}")
    print("#" * 50)

    set_tool(ROBOT_TOOL)
    set_tcp(ROBOT_TCP)


# --------------------
# DSR Motion Functions
# --------------------
def shaker_ungrip():
    """DRL: shaker_ungrip"""
    from DSR_ROBOT2 import set_digital_output, wait

    set_digital_output(1, 0)   # OFF
    wait(0.2)
    set_digital_output(2, 1)   # ON


def put_shaker():
    """DRL: put_shaker"""
    from DSR_ROBOT2 import movej, movel, posj, posx, set_desired_force, release_force, wait

    # MoveJNode
    movej(
        posj(-1.00, 10.16, 127.80, 0.93, -38.28, -91.65),
        vel=VEL_J,
        acc=ACC_J
    )

    # MoveJNode
    movej(
        posj(0.87, 32.60, 106.30, 3.38, -47.42, -93.07),
        vel=VEL_J,
        acc=ACC_J
    )

    # MoveLNode (REL)
    movel(
        posx(0.00, 0.00, -60.00, 0.00, 0.00, 0.00),
        vel=VEL_L,
        acc=ACC_L,
        ref=0,
        mod=1
    )

    # set_desired_force(
    #     [0.0, 0.0, -15.0, 0.0, 0.0, 0.0],
    #     [0, 0, 1, 0, 0, 0],
    #     time=0.0,
    #     mod=0
    # )
    # wait(5.0)
    # release_force(time=0.0)


# --------------------
# Sequence
# --------------------
def put_shaker_seq():
    from DSR_ROBOT2 import (
        set_singular_handling,
        set_velj,
        set_accj,
        set_velx,
        set_accx,
        DR_AVOID,
        movel,
        posx,
        wait
    )

    # DRL: global motion settings
    set_singular_handling(DR_AVOID)
    set_velj(VEL_J)
    set_accj(ACC_J)
    set_velx(VEL_L, 68.25)
    set_accx(ACC_L, 273.0)

    # DRL loop body
    put_shaker()
    shaker_ungrip()
    wait(1.0)

    movel(
        posx(-80.00, 0.00, 0.00, 0.00, 0.00, 0.00),
        vel=VEL_L,
        acc=ACC_L,
        ref=0,
        mod=1
    )


# --------------------
# Main
# --------------------
def main():
    rclpy.init()
    node = rclpy.create_node("m6_put_shaker_node", namespace=ROBOT_ID)
    DR_init.__dsr__node = node

    try:
        initialize_robot()
        put_shaker_seq()

    except KeyboardInterrupt:
        pass

    finally:
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
