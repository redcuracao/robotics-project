import rclpy
import DR_init
# from std_msgs.msg import String

# def command_cb(msg):
#     if msg.data != "START":
#         return

#     shaking_motion()
#     put_shaker()
#     done_pub.publish(String(data="DONE"))

# 로봇 설정 상수
ROBOT_ID = "dsr01"
ROBOT_MODEL = "m0609"
ROBOT_TOOL = "Tool Weight"
ROBOT_TCP = "GripperDA"

# DR_init 설정
DR_init.__dsr__id = ROBOT_ID
DR_init.__dsr__model = ROBOT_MODEL


def initialize_robot():
    """로봇의 Tool과 TCP를 설정"""
    from DSR_ROBOT2 import set_tool, set_tcp

    print("#" * 50)
    print("Initializing robot with the following settings:")
    print(f"ROBOT_ID: {ROBOT_ID}")
    print(f"ROBOT_MODEL: {ROBOT_MODEL}")
    print(f"ROBOT_TCP: {ROBOT_TCP}")
    print(f"ROBOT_TOOL: {ROBOT_TOOL}")
    print("#" * 50)

    set_tool(ROBOT_TOOL)
    set_tcp(ROBOT_TCP)


def shaking_motion():
    """원본 DRL shaker_node 동작을 ROS2 DSR 포맷으로 변환"""

    from DSR_ROBOT2 import (
        set_singular_handling,
        set_velj,
        set_accj,
        set_velx,
        set_accx,
        movej,
        move_periodic,
        posj,
        DR_AVOID,
        DR_MV_RA_DUPLICATE,
    )

    REF_BASE = 0
    # -----------------------------
    # 원본 DRL 세팅 부분
    # -----------------------------
    set_singular_handling(DR_AVOID)
    set_velj(60.0)
    set_accj(150.0)
    set_velx(250.0, 80.625)
    set_accx(1000.0, 400.0)

    gLoop103502587 = 0
    while gLoop103502587 < 1:

        # MoveJ #1
        movej(
            posj(-22.92, -23.42, 102.94, 18.46, 55.67, -85.95),
            vel=100.0,
            acc=200.0,
            radius=0.0,
            ra=DR_MV_RA_DUPLICATE,
        )

        # MovePeriodic #1
        move_periodic(
            amp=[40.0, 0.0, 40.0, 0.0, 0.0, 0.0],
            period=[0.8, 0.0, 0.8, 0.0, 0.0, 0.0],
            atime=2.0,
            repeat=5,
            ref=0,
        )

        # MoveJ #2
        movej(
            posj(-1.49, -26.95, 113.04, 25.20, 45.65, -146.29),
            vel=100.0,
            acc=200.0,
            radius=0.0,
            ra=DR_MV_RA_DUPLICATE,
        )

        # MovePeriodic #2
        move_periodic(
            amp=[40.0, 15.0, 40.0, 0.0, 0.0, 0.0],
            period=[0.8, 0.8, 0.8, 0.0, 0.0, 0.0],
            atime=1.5,
            repeat=5,
            ref=0,
        )

        # MoveJ #3
        movej(
            posj(-24.65, -24.51, 104.93, 31.44, 54.92, -124.97),
            vel=100.0,
            acc=200.0,
            radius=0.0,
            ra=DR_MV_RA_DUPLICATE,
        )

        # MovePeriodic #3
        move_periodic(
            amp=[40.0, 0.0, 40.0, 0.0, 0.0, 0.0],
            period=[0.8, 0.0, 0.8, 0.0, 0.0, 0.0],
            atime=1.5,
            repeat=5,
            ref=0,
        )

        gLoop103502587 += 1

def shaker_ungrip():
    from DSR_ROBOT2 import set_digital_output, wait
    ON = 1
    OFF = 0

    set_digital_output(1, OFF)
    wait(0.20)
    set_digital_output(2, ON)
    wait(0.50)

def put_shaker():
    from DSR_ROBOT2 import posx, posj, movej, movel, DR_MV_MOD_REL

    # MoveJ #1
    movej(posj(-24.65, -24.51, 104.93, 31.44, 54.92, -124.97), radius=0.0)

    # MoveJ #2
    movej(posj(-0.4, 38.91, 106.59, -0.81, -53.22, -89.25), radius=0.0)

    # MoveL (REL)
    movel(
        posx(0.0, 0.0, -100.0, 0.0, 0.0, 0.0),
        radius=0.0,
        ref=0,
        mod=DR_MV_MOD_REL
    )

    shaker_ungrip()


def main(args=None):
    # global done_pub

    """메인 함수: ROS2 노드 초기화 및 동작 수행"""
    rclpy.init(args=args)
    node = rclpy.create_node("shaker_node", namespace=ROBOT_ID)

    DR_init.__dsr__node = node

    try:
        initialize_robot()
        shaking_motion()
        put_shaker()
        # done_pub = node.create_publisher(String, '/shaker/done', 10)
        # node.create_subscription(String, '/shaker/command', command_cb, 10)

    except KeyboardInterrupt:
        print("\nNode interrupted by user. Shutting down...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        rclpy.shutdown()


if __name__ == "__main__":
    main()
