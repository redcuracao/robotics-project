import rclpy
import DR_init
import math
import time

# ============================================================
# Robot Config
# ============================================================
ROBOT_ID = "dsr01"
ROBOT_MODEL = "m0609"
ROBOT_TCP = "Tool Weight"
ROBOT_TOOL = "GripperDA_v1"

DR_init.__dsr__id = ROBOT_ID
DR_init.__dsr__model = ROBOT_MODEL


# ============================================================
# Initialize Robot
# ============================================================
def initialize_robot():
    from DSR_ROBOT2 import set_tool, set_tcp

    print("#" * 50)
    print("Initialize Robot")
    print("#" * 50)

    set_tool(ROBOT_TOOL)
    set_tcp(ROBOT_TCP)


# ============================================================
# Safe Math-based Shaking (ros2_control friendly)
# ============================================================
def math_shake(
    cycles=3,
    freq=1.2,          # Hz (낮게)
    z_amp=25.0,        # mm
    y_amp=5.0,         # mm
    dt=0.03            # sec (controller-friendly)
):
    """
    BASE 기준 상대좌표
    상하(Z) + 좌우(Y) 동시 쉐이킹
    ros2_control 안전 버전
    """
    from DSR_ROBOT2 import movel, posx
    from DSR_ROBOT2 import DR_BASE, DR_MV_MOD_REL

    total_time = cycles / freq
    steps = int(total_time / dt)

    t = 0.0
    prev_y = 0.0
    prev_z = 0.0

    for _ in range(steps):
        # 수학적 동시 파형
        y = y_amp * math.sin(2.0 * math.pi * freq * t + math.pi / 2.0)
        z = z_amp * math.sin(2.0 * math.pi * freq * t)

        dy = y - prev_y
        dz = z - prev_z

        movel(
            posx(0.0, dy, dz, 0.0, 0.0, 0.0),
            vel=120,                # 안전한 속도
            acc=200,                # 안전한 가속
            ref=DR_BASE,
            mod=DR_MV_MOD_REL
        )

        prev_y = y
        prev_z = z
        t += dt


# ============================================================
# Motion Sequence
# ============================================================
def shaking_motion():
    from DSR_ROBOT2 import movej, posj

    # ---------------- Pose A ----------------
    movej(
        posj(-22.92, -23.42, 102.94, 18.46, 55.67, -85.95),
        vel=60,
        acc=120
    )
    math_shake(cycles=3)

    # ---------------- Pose B ----------------
    movej(
        posj(-1.49, -26.95, 113.04, 25.20, 45.65, -146.29),
        vel=60,
        acc=120
    )
    math_shake(cycles=3)

    # ---------------- Pose C ----------------
    movej(
        posj(-24.65, -24.51, 104.93, 31.44, 54.92, -124.97),
        vel=60,
        acc=120
    )
    math_shake(cycles=3)


# ============================================================
# Main
# ============================================================
def main():
    rclpy.init()
    node = rclpy.create_node("math_shaker_safe", namespace=ROBOT_ID)
    DR_init.__dsr__node = node

    # controller 안정 대기
    time.sleep(1.0)

    try:
        initialize_robot()
        shaking_motion()
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()