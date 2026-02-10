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
    print("Initializing robot for m7_twist_open_cap")
    print(f"ROBOT_ID    : {ROBOT_ID}")
    print(f"ROBOT_MODEL : {ROBOT_MODEL}")
    print("#" * 50)

    set_tool(ROBOT_TOOL)
    set_tcp(ROBOT_TCP)


# --------------------
# DSR Motion / IO Functions
# --------------------
def cap_grip():
    from DSR_ROBOT2 import set_digital_output, wait
    set_digital_output(1, 1)   # ON
    wait(0.2)
    set_digital_output(2, 1)   # ON


def cap_ungrip():
    from DSR_ROBOT2 import set_digital_output, wait
    set_digital_output(1, 0)   # OFF
    wait(0.2)
    set_digital_output(2, 1)   # ON


def open_cap():
    """DRL: open_cap (twist with force/compliance)"""
    from DSR_ROBOT2 import (
        task_compliance_ctrl,
        set_stiffnessx,
        set_desired_force,
        release_force,
        release_compliance_ctrl,
        movel,
        posx,
        wait
    )

    # Compliance ON
    task_compliance_ctrl()
    set_stiffnessx([3000.0, 3000.0, 50.0, 200.0, 200.0, 200.0], time=0.0)

    # Z-rotation force (twist open)
    set_desired_force(
        [0.0, 0.0, 0.0, 0.0, 0.0, 5.0],
        [0, 0, 0, 0, 0, 1],
        time=0.0,
        mod=0
    )
    
    wait(1.5)

    release_force(time=0.0)
    release_compliance_ctrl()

    # MoveLNode (REL)
    movel(
        posx(0.00, 0.00, 50.00, 0.00, 0.00, 0.00),
        vel=VEL_L,
        acc=ACC_L,
        ref=0,
        mod=1
    )

def just_twist():
    from DSR_ROBOT2 import (
        task_compliance_ctrl,
        set_stiffnessx,
        set_desired_force,
        release_force,
        release_compliance_ctrl,
        movel,
        posx,
        wait
    )

    task_compliance_ctrl()
    set_stiffnessx([3000.0, 3000.0, 50.0, 200.0, 200.0, 200.0], time=0.0)

    # Z-rotation force (twist open)
    set_desired_force(
        [0.0, 0.0, 0.0, 0.0, 3.0, -5.12],
        [0, 0, 0, 0, 0, 1],
        time=0.0,
        mod=0
    )
    
    wait(1.5)

    release_force(time=0.0)
    release_compliance_ctrl()


def put_cap():
    """DRL: put_cap"""
    from DSR_ROBOT2 import movel, posx, wait, movej, posj, task_compliance_ctrl, set_stiffnessx, set_desired_force, release_force, release_compliance_ctrl

    # MoveLNode (ABS)
    movel(
        posx(571.15, -171.80, 281.59, 177.10, -89.76, 89.52),
        vel=VEL_L,
        acc=ACC_L,
        ref=0,
        mod=0
    )

    # movel(
    # posx(-9.50, 9.75, 0.00, 0.00, 0.00, 0.00),
    # vel=VEL_L,
    # acc=ACC_L,
    # ref=0,
    # mod=1
    # )

    task_compliance_ctrl()
    set_stiffnessx([3000.0, 3000.0, 50.0, 200.0, 200.0, 200.0], time=0.0)

    # Z-rotation force (twist open)
    set_desired_force(
        [0.0, 0.0, 0.0, 0.0, 0.0, 5.00],
        [0, 0, 0, 0, 0, 1],
        time=0.0,
        mod=0
    )
    
    wait(1.5)

    release_force(time=0.0)
    release_compliance_ctrl()

    # MoveLNode (REL)
    movel(
        posx(0.00, 0.00, -95.00, 0.00, 0.00, 0.00),
        vel=VEL_L,
        acc=ACC_L,
        ref=0,
        mod=1
    )

    wait(1.5)
    cap_ungrip()

    movel(
        posx(-8.0, 0.00, 0.00, 0.00, 0.00, 0.00),
        vel=100,
        acc=ACC_L,
        ref=0,
        mod=1
    )


# --------------------
# Sequence
# --------------------
def twist_open_cap_seq():
    from DSR_ROBOT2 import (
        movej,
        movel,
        posj,
        posx,
        wait,
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
    set_velx(VEL_L, 80.625)
    set_accx(ACC_L, 322.5)

    # MoveJNode (approach)
    movej(
        posj(0.19, 27.87, 106.67, 0.85, -44.48, -90.27),
        vel=VEL_J,
        acc=ACC_J
    )

    cap_grip()
    wait(0.5)
    open_cap()
    # just_twist()
    put_cap()

    # MoveJNode (retreat)
    movej(
        posj(-4.47, 23.20, 126.01, -9.30, -55.33, -81.69),
        vel=VEL_J,
        acc=ACC_J
    )




# --------------------
# Main
# --------------------
def main():
    rclpy.init()
    node = rclpy.create_node("m7_twist_open_cap_node", namespace=ROBOT_ID)
    DR_init.__dsr__node = node

    try:
        initialize_robot()
        twist_open_cap_seq()

    except KeyboardInterrupt:
        pass

    finally:
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
