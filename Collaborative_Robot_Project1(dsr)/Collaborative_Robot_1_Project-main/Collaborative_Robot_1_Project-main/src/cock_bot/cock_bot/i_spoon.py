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

VEL_J = 30
ACC_J = 200


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
    from DSR_ROBOT2 import set_digital_output, wait, movel, posx
    set_digital_output(1, 0)   # OFF
    wait(0.2)
    set_digital_output(2, 1)   # ON
    wait(1.0)





# --------------------
# Motion Blocks
# --------------------
def get_spoon():
    from DSR_ROBOT2 import movel, posx, wait, movej, posj

    # movel(
    #     posx(469.210, -162.470, 134.960, 148.41, -91.23, 88.96),
    #     vel=VELX_LIN,
    #     acc=ACCX_LIN
    # )
    movej(
        posj(-15.82, 34.28, 121.81, 16.97, -65.74, -97.66),
        vel=VEL_J,
        acc=ACC_J
    )
    wait(0.5)
    shaker_grip()

    movel(
        posx(0.00, 0.00, 100.00, 0.00, 0.00, 0.00),
        vel=VELX_LIN,
        acc=ACCX_LIN,
        ref=0,
        mod=1
    )


def move_spoon():
    from DSR_ROBOT2 import movel, posx, wait

    movel(
        posx(466.240, 7.680, 379.390, 178.47, -88.71, -93.13),
        vel=VELX_LIN,
        acc=ACCX_LIN
    )

    wait(1.0)

    movel(
        posx(553.910, 11.040, 372.420, 178.29, -88.88, -93.04),
        vel=VELX_LIN,
        acc=ACCX_LIN
    )

    movel(
        posx(0.00, 0.00, -130.00, 0.00, 0.00, 0.00),
        vel=VELX_LIN,
        acc=ACCX_LIN,
        ref=0,
        mod=1
    )

def rev_move_spoon():
    from DSR_ROBOT2 import movel, posx, wait

    movel(
        posx(0.00, 0.00, 130.00, 0.00, 0.00, 0.00),
        vel=VELX_LIN,
        acc=ACCX_LIN,
        ref=0,
        mod=1
    )

    movel(
        posx(379.900, 11.680, 366.480, 178.62, -88.73, -92.97),
        vel=VELX_LIN,
        acc=ACCX_LIN
    )
    
    wait(1.0)

    movel(
        posx(466.700, -167.900, 221.980, 148.57, -91.21, 89.05),
        vel=VELX_LIN,
        acc=ACCX_LIN
    )

    movel(
        posx(469.210, -162.470, 134.000, 148.41, -91.23, 88.96),
        vel=VELX_LIN,
        acc=ACCX_LIN
    )



# def rev_get_spoon():
#     from DSR_ROBOT2 import movel, posx, wait

#     movel(
#         posx(492.76, -91.51, 458.34, 167.3, -96.05, 89.56),
#         vel=VELX_LIN,
#         acc=ACCX_LIN
#     )

#     wait(0.5)

    
#     movel(
#         posx(502.92, -86.31, 232.210, 154.83, -92.03, 89.56),
#         vel=VELX_LIN,
#         acc=ACCX_LIN
#     )
#     shaker_ungrip()
    
#     movel(
#         posx(444.160, 11.040, 202.08, 178.12, -91.6, 88.95),
#         vel=VELX_LIN,
#         acc=ACCX_LIN
#     )


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
        movel,
        posx
    )

    set_singular_handling(1)  # DR_AVOID
    set_velj(VELJ_WORK)
    set_accj(ACCJ_WORK)

    get_spoon()
    move_spoon()
    stir_spiral()
    rev_move_spoon()
    shaker_ungrip()
    movel(
        posx(479.940, -2.900, 144.510, 0.93, 91.58, -90.67),
        vel=VELX_LIN,
        acc=ACCX_LIN
    )


    # rev_get_spoon()


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
