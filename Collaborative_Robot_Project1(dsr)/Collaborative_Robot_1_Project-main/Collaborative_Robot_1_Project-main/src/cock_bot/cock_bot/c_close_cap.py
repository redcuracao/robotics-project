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


# --------------------
# Robot Initialize
# --------------------
def initialize_robot():
    from DSR_ROBOT2 import set_tool, set_tcp

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

def cap_grip_and_move():
    from DSR_ROBOT2 import movej, movel, posj, posx, DR_MV_MOD_REL, wait
    movej(posj(-17.16, 38.61, 49.86, 10.70, 60.10, -107.14), radius=0.00)
    cap_grip()
    wait(1.00)
    movel(posx(0.00, 0.00, 100.00, 0.00, 0.00, 0.00), radius=0.00, ref=0, mod=DR_MV_MOD_REL)
    movel(posx(-1.50, 182.00, 0.00, 0.00, 0.00, 0.00), radius=0.00, ref=0, mod=DR_MV_MOD_REL)
    movel(posx(0.00, 0.00, -18.00, 0.00, 0.00, 0.00), radius=0.00, ref=0, mod=DR_MV_MOD_REL)

def close_cap():
    from DSR_ROBOT2 import (
        task_compliance_ctrl,
        set_stiffnessx,
        set_desired_force,
        release_force,
        release_compliance_ctrl,
        wait
    )
        # Compliance ON
    task_compliance_ctrl()
    set_stiffnessx(
        [3000.0, 3000.0, 30.0, 200.0, 200.0, 200.0],
        time=0.0
    )
    # Z축 방향 힘 제어
    set_desired_force(
        [0.0, 0.0, -20.0, 0.0, 0.0, 0.0],
        [0, 0, 1, 0, 0, 0],
        time=0.0,
        mod=0
    )
    wait(5.0)
    release_force(time=0.0)
    release_compliance_ctrl()


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

def close_cap_seq():
    from DSR_ROBOT2 import set_singular_handling, set_accj, set_velj, set_accx, set_velx, DR_AVOID
    set_singular_handling(DR_AVOID)
    set_velj(30.0)
    set_accj(100.0)
    set_velx(100.0, 68.25)
    set_accx(200.0, 273.0)
    cap_grip_and_move()
    close_cap()
    cap_ungrip()


# --------------------
# Main
# --------------------
def main():

    rclpy.init()
    node = rclpy.create_node("put_shaker_node", namespace=ROBOT_ID)
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
        close_cap_seq()

    except KeyboardInterrupt:
        pass

    finally:
        rclpy.shutdown()

if __name__ == "__main__":
    main()
