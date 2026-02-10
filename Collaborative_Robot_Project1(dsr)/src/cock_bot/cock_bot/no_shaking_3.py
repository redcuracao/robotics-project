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
ACC_J = 150

VEL_L = 250
ACC_L = 1000


# --------------------
# Robot Initialize
# --------------------
def initialize_robot():
    from DSR_ROBOT2 import set_tool, set_tcp

    print("#" * 50)
    print("Initializing robot for m5_shaking")
    print(f"ROBOT_ID    : {ROBOT_ID}")
    print(f"ROBOT_MODEL : {ROBOT_MODEL}")
    print("#" * 50)

    set_tool(ROBOT_TOOL)
    set_tcp(ROBOT_TCP)


# --------------------
# DSR Motion Functions
# --------------------
def shaking_motion():
    """DRL: m5_shaking main body"""
    from DSR_ROBOT2 import movej, move_periodic, posj

    # MoveJNode
    movej(
        posj(-22.92, -23.42, 102.94, 18.46, 55.67, -85.95),
        vel=100.0,
        acc=200.0,
    )

    # MovePeriodicNode
    move_periodic(
        amp=[40.0, 0.0, 40.0, 0.0, 0.0, 0.0],
        period=[0.80, 0.0, 0.80, 0.0, 0.0, 0.0],
        atime=2.0,
        repeat=5,
        ref=0,
    )

    # MoveJNode
    movej(
        posj(-1.49, -26.95, 113.04, 25.20, 45.65, -146.29),
        vel=100.0,
        acc=200.0,
    )

    # MovePeriodicNode
    move_periodic(
        amp=[40.0, 15.0, 40.0, 0.0, 0.0, 0.0],
        period=[0.80, 0.80, 0.80, 0.0, 0.0, 0.0],
        atime=1.5,
        repeat=5,
        ref=0,
    )

    # MoveJNode
    movej(
        posj(-24.65, -24.51, 104.93, 31.44, 54.92, -124.97),
        vel=100.0,
        acc=200.0,
    )

    # MovePeriodicNode
    move_periodic(
        amp=[40.0, 0.0, 40.0, 0.0, 0.0, 0.0],
        period=[0.80, 0.0, 0.80, 0.0, 0.0, 0.0],
        atime=1.5,
        repeat=5,
        ref=0,
    )


# --------------------
# Sequence
# --------------------
def shaking_seq():
    from DSR_ROBOT2 import (
        set_singular_handling,
        set_velj,
        set_accj,
        set_velx,
        set_accx,
        DR_AVOID,
    )

    # DRL: global motion settings
    set_singular_handling(DR_AVOID)

    set_velj(VEL_J)
    set_accj(ACC_J)

    set_velx(VEL_L, 80.625)
    set_accx(ACC_L, 400.0)

    # DRL main sequence
    shaking_motion()


# --------------------
# Main
# --------------------
def main():
    rclpy.init()
    node = rclpy.create_node("m5_shaking_node", namespace=ROBOT_ID)
    DR_init.__dsr__node = node

    try:
        initialize_robot()
        shaking_seq()
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()