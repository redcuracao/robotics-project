import rclpy
import DR_init
import time

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
# Motion Parameters
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
    print("Initializing robot for m5_shaking (Z periodic + delayed Y async)")
    print(f"ROBOT_ID    : {ROBOT_ID}")
    print(f"ROBOT_MODEL : {ROBOT_MODEL}")
    print("#" * 50)

    set_tool(ROBOT_TOOL)
    set_tcp(ROBOT_TCP)


# --------------------
# Y Async 2x2 Reach (with wait)
# --------------------
def y_async_reach_2x2(A):
    """
    Y축 좌/우 도달 2회씩 (비동기)
    상대좌표 누적을 고려한 dy 시퀀스
    """
    from DSR_ROBOT2 import amovel, posx, DR_TOOL, DR_MV_MOD_REL

    # 0 → +A → -A → +A → -A
    for dy in (A, -2*A, 2*A, -2*A):
        amovel(
            posx(0.0, dy, 0.0, 0.0, 0.0, 0.0),
            vel=120,
            acc=180,
            ref=DR_TOOL,
            mod=DR_MV_MOD_REL
        )


# --------------------
# DSR Motion Functions
# --------------------
def shaking_motion():
    from DSR_ROBOT2 import movej, move_periodic, posj

    # --------------------
    # Start Pose
    # --------------------
    movej(
        posj(-22.92, -23.42, 102.94, 18.46, 55.67, -85.95),
        vel=100.0,
        acc=200.0
    )

    # --------------------
    # Parameters
    # --------------------
    Z_AMP = 32.0
    Z_PERIOD = 0.80
    CYCLES = 5

    Y_REACH = 4.0          # 좌우 도달 (mm)
    Y_DELAY = 0.12         # ★ 핵심: Z 시작 후 Y 합류 지연 (sec)

    # --------------------
    # Cycle-based Shaking
    # --------------------
    for _ in range(CYCLES):

        # 1) Z periodic 먼저 시작 (1사이클)
        move_periodic(
            amp=[0.0, 0.0, Z_AMP, 0.0, 0.0, 0.0],
            period=[0.0, 0.0, Z_PERIOD, 0.0, 0.0, 0.0],
            atime=0.0,
            repeat=1,
            ref=0
        )

        # 2) 짧은 웨이트 (타이밍 맞추기)
        time.sleep(Y_DELAY)

        # 3) Y 비동기 합류 (좌/우 2번씩)
        y_async_reach_2x2(Y_REACH)

    # --------------------
    # Middle Pose
    # --------------------
    movej(
        posj(-1.49, -26.95, 113.04, 25.20, 45.65, -146.29),
        vel=100.0,
        acc=200.0
    )

    # --------------------
    # Second Shaking Block
    # --------------------
    for _ in range(CYCLES):

        move_periodic(
            amp=[0.0, 0.0, Z_AMP, 0.0, 0.0, 0.0],
            period=[0.0, 0.0, Z_PERIOD, 0.0, 0.0, 0.0],
            atime=0.0,
            repeat=1,
            ref=0
        )

        time.sleep(Y_DELAY)
        y_async_reach_2x2(Y_REACH)


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
        DR_AVOID
    )

    set_singular_handling(DR_AVOID)
    set_velj(VEL_J)
    set_accj(ACC_J)
    set_velx(VEL_L, 80.0)
    set_accx(ACC_L, 400.0)

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