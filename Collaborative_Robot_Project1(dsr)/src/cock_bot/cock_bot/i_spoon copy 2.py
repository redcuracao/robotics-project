# stururur.py
import rclpy
import DR_init

# --------------------
# Robot Config
# --------------------
ROBOT_ID = "dsr01"
ROBOT_MODEL = "m0609"
ROBOT_TCP = "Tool Weight"
ROBOT_TOOL = "GripperDA_v1"

DR_init.__dsr__id = ROBOT_ID
DR_init.__dsr__model = ROBOT_MODEL


# --------------------
# Speed Params (LOWER & SAFE)
# --------------------
VELJ_WORK = 50.0
ACCJ_WORK = 80.0

VELX_LIN = 120.0        # mm/s
ACCX_LIN = 400.0        # mm/s²


# --------------------
# Spiral Params (OLD API)
# --------------------
SP_REV  = 5.0
SP_RMAX = 20.0
SP_L    = 10.0          
SP_T    = 22.0         


# --------------------
# Robot Initialize
# --------------------
def initialize_robot():
    from DSR_ROBOT2 import set_tool, set_tcp
    set_tool(ROBOT_TOOL)
    set_tcp(ROBOT_TCP)


# --------------------
# Tool Control
# --------------------
def shaker_grip():
    from DSR_ROBOT2 import set_digital_output, wait
    set_digital_output(1, 1)   # ON
    wait(0.2)
    set_digital_output(2, 1)   # ON
    wait(1.0)
    
def shaker_ungrip():
    from DSR_ROBOT2 import set_digital_output, wait
    set_digital_output(1, 0)   # OFF
    wait(0.2)
    set_digital_output(2, 1)   # ON
    wait(1.0)




# --------------------
# Motion Blocks
# --------------------
def get_spoon():
    from DSR_ROBOT2 import movel, posx, wait

    movel(
        posx(502.92, -86.31, 232.210, 154.83, -92.03, 89.56),
        vel=VELX_LIN,
        acc=ACCX_LIN
    )
    wait(0.5)
    shaker_grip()

    movel(
        posx(492.76, -91.51, 458.34, 167.3, -96.05, 89.56),
        vel=VELX_LIN,
        acc=ACCX_LIN
    )


def move_spoon():
    from DSR_ROBOT2 import movel, posx, wait

    movel(
        posx(557.15, 7.54, 441.68, 178.24, -96.62, 90.86),
        vel=VELX_LIN,
        acc=ACCX_LIN
    )

    wait(1.0)

    movel(
        posx(572.30, 14.41, 387.67, 178.01, -100.21, 91.27),
        vel=VELX_LIN,
        acc=ACCX_LIN
    )

def rev_move_spoon():
    from DSR_ROBOT2 import movel, posx, wait


    movel(
        posx(572.30, 14.41, 387.67, 178.01, -100.21, 91.27),
        vel=VELX_LIN,
        acc=ACCX_LIN
    )
    
    wait(1.0)

    movel(
        posx(557.15, 7.54, 441.68, 178.24, -96.62, 90.86),
        vel=VELX_LIN,
        acc=ACCX_LIN
    )

def rev_get_spoon():
    from DSR_ROBOT2 import movel, posx, wait

    movel(
        posx(492.76, -91.51, 458.34, 167.3, -96.05, 89.56),
        vel=VELX_LIN,
        acc=ACCX_LIN
    )

    wait(0.5)

    
    movel(
        posx(502.92, -86.31, 232.210, 154.83, -92.03, 89.56),
        vel=VELX_LIN,
        acc=ACCX_LIN
    )
    shaker_ungrip()
    
    movel(
        posx(444.160, 11.040, 202.08, 178.12, -91.6, 88.95),
        vel=VELX_LIN,
        acc=ACCX_LIN
    )


def stir_spiral():
    from DSR_ROBOT2 import move_spiral


    move_spiral(
        SP_REV,
        SP_RMAX,
        SP_L,
        SP_T,
        2,   # axis = Z
        0    # ref = TOOL
    )


# --------------------
# Sequence
# --------------------
def cocktail_sequence():
    from DSR_ROBOT2 import (
        set_singular_handling,
        set_velj,
        set_accj,
    )

    set_singular_handling(1)  # DR_AVOID
    set_velj(VELJ_WORK)
    set_accj(ACCJ_WORK)

    get_spoon()
    move_spoon()
    stir_spiral()
    rev_move_spoon()
    rev_get_spoon()


# --------------------
# Main
# --------------------
def main(args=None):
    rclpy.init(args=args)

    node = rclpy.create_node("spoon_spin_node", namespace=ROBOT_ID)
    DR_init.__dsr__node = node

    try:
        initialize_robot()
        cocktail_sequence()
    except Exception as e:
        node.get_logger().error(f"[ERROR] motion failed: {e}")
    finally:
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
