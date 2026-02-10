# fast
import rclpy
import DR_init
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
# Robot Initialize
# ============================================================
def initialize_robot():
    from DSR_ROBOT2 import set_tool, set_tcp
    print("#" * 50)
    print("Initialize Robot")
    print("#" * 50)
    set_tool(ROBOT_TOOL)
    set_tcp(ROBOT_TCP)


# ============================================================
# Periodic shaker
# Z : 상하 (주동작)
# Y : 좌우 반복 (보조)
# RZ: 손목 비틀기 (6번 관절처럼 보이게)
# ============================================================
def shaker_periodic(
    y_amp=4,        # mm
    z_amp=60.0,       # mm (기존 35 → 안정 영역)
    rz_amp=4.0,       # deg (J6 위주 반응)
    period=0.7,       # sec (기존 0.6 → 가속 감소)
    atime=0.6,        # sec (period보다 약간 작게)
    repeat=4
):
    from DSR_ROBOT2 import move_periodic

    move_periodic(
        amp=[
            0.0,        # X
            y_amp,      # Y
            z_amp,      # Z
            0.0,        # RX
            0.0,        # RY
            rz_amp      # RZ (손목 까딱)
        ],
        period=[
            0.0,
            period / 2.0,
            period,
            0.0,
            0.0,
            period / 2.0
        ],
        atime=atime,
        repeat=repeat,
        ref=0           # BASE 기준
    )


# ============================================================
# Motion Sequence
# ============================================================
def shaking_motion():
    from DSR_ROBOT2 import movej, posj

    # ---------- Pose A ----------
    movej(
        posj(-22.92, -23.42, 102.94, 18.46, 55.67, -85.95),
        vel=80, acc=150
    )
    shaker_periodic()

    # ---------- Pose B ----------
    movej(
        posj(-1.49, -26.95, 113.04, 25.20, 45.65, -146.29),
        vel=80, acc=150
    )
    shaker_periodic()

    # ---------- Pose C ----------
    movej(
        posj(-24.65, -24.51, 104.93, 31.44, 54.92, -124.97),
        vel=80, acc=150
    )
    shaker_periodic()


# ============================================================
# Main
# ============================================================
def main():
    rclpy.init()
    node = rclpy.create_node(
        "cocktail_shaker_human_like",
        namespace=ROBOT_ID
    )
    DR_init.__dsr__node = node

    time.sleep(1.0)

    try:
        initialize_robot()
        shaking_motion()
    finally:
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
    