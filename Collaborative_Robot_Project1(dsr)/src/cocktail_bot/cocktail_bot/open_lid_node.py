#!/usr/bin/env python3
import rclpy
import DR_init
# from std_msgs.msg import String

ROBOT_ID = "dsr01"
ROBOT_MODEL = "m0609"
ROBOT_TOOL = "Tool Weight"
ROBOT_TCP = "GripperDA"

DR_init.__dsr__id = ROBOT_ID
DR_init.__dsr__model = ROBOT_MODEL


# ------------------------------
# Init
# ------------------------------
def initialize_robot():
    from DSR_ROBOT2 import set_tool, set_tcp
    set_tool(ROBOT_TOOL)
    set_tcp(ROBOT_TCP)


# ------------------------------
# Gripper
# ------------------------------
def cap_grip():
    from DSR_ROBOT2 import set_digital_output, wait
    set_digital_output(1, 1)
    wait(0.2)
    set_digital_output(2, 1)


def cap_ungrip():
    from DSR_ROBOT2 import set_digital_output, wait
    set_digital_output(1, 0)
    wait(0.2)
    set_digital_output(2, 1)


# ==================================================
# OPEN CAP (기존 lid_node 기능)
# ==================================================
def open_cap():
    from DSR_ROBOT2 import (
        set_singular_handling, set_velj, set_accj,
        set_velx, set_accx, movel, posx, wait,
        move_periodic, task_compliance_ctrl,
        release_compliance_ctrl, set_desired_force,
        release_force, set_stiffnessx,
        DR_AVOID, DR_MV_MOD_ABS, DR_MV_MOD_REL,
    )

    set_singular_handling(DR_AVOID)
    set_velj(60.0)
    set_accj(100.0)
    set_velx(250.0, 80.625)
    set_accx(1000.0, 322.5)

    movel(
        posx(361.57, -1.16, 438.91, 17.08, -177.91, 6.09),
        radius=0.0, ref=0, mod=DR_MV_MOD_ABS,
    )

    cap_grip()
    wait(1.0)

    task_compliance_ctrl()
    set_stiffnessx([3000, 3000, 20, 200, 200, 200], time=0.0)
    set_desired_force([0, 0, -3, 0, 0, 0], [0, 0, 1, 0, 0, 0], time=0.0)

    move_periodic(
        amp=[0, 0, 0, 0, 0, 15],
        period=[0, 0, 0, 0, 0, 2],
        atime=0.5,
        repeat=2,
        ref=0,
    )

    release_compliance_ctrl()
    release_force(time=0.0)

    movel(
        posx(0, 0, 30, 0, 0, 0),
        vel=[50, 64.13],
        acc=[1000, 256.5],
        ref=0,
        mod=DR_MV_MOD_REL,
    )


# ==================================================
# CLOSE CAP (추가된 기능)
# ==================================================
def close_cap():
    from DSR_ROBOT2 import (
        movej, movel, posj, posx, wait,
        task_compliance_ctrl, release_compliance_ctrl,
        set_stiffnessx, set_desired_force, release_force,
        set_singular_handling, set_velj, set_accj,
        set_velx, set_accx,
        DR_MV_MOD_REL, DR_AVOID, DR_FC_MOD_ABS
    )

    set_singular_handling(DR_AVOID)
    set_velj(30.0)
    set_accj(100.0)
    set_velx(100.0, 68.25)
    set_accx(200.0, 273.0)

    movej(posj(-17.16, 38.61, 49.86, 10.70, 60.10, -107.14))
    cap_grip()
    wait(1.0)

    movel(posx(0, 0, 100, 0, 0, 0), mod=DR_MV_MOD_REL)
    movel(posx(-1.5, 182, 0, 0, 0, 0), mod=DR_MV_MOD_REL)
    movel(posx(0, 0, -18, 0, 0, 0), mod=DR_MV_MOD_REL)

    task_compliance_ctrl()
    set_stiffnessx([3000, 3000, 30, 200, 200, 200], time=0.0)
    set_desired_force([0, 0, -25, 0, 0, 0], [0, 0, 1, 0, 0, 0], time=0.0, mod=DR_FC_MOD_ABS)

    wait(5.0)

    release_force(time=0.0)
    release_compliance_ctrl()
    cap_ungrip()


# ------------------------------
# ROS2 Node
# ------------------------------
def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node("lid_node", namespace=ROBOT_ID)
    DR_init.__dsr__node = node
    
    try:
        initialize_robot()
        open_cap()
        # close_cap()
    except KeyboardInterrupt:
        print("\nUser interrupted. Shutting down...")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        rclpy.shutdown()

    # done_pub = node.create_publisher(String, "/lid/done", 10)
    # busy = {"flag": False}

    # def command_cb(msg: String):
    #     if busy["flag"]:
    #         node.get_logger().warn("lid_node busy")
    #         return

    #     busy["flag"] = True
    #     try:
    #         if msg.data == "OPEN":
    #             node.get_logger().info("LID OPEN start")
    #             open_cap()
    #         elif msg.data == "CLOSE":
    #             node.get_logger().info("LID CLOSE start")
    #             close_cap()
    #         else:
    #             node.get_logger().warn(f"Unknown command: {msg.data}")
    #             return

    #         done_pub.publish(String(data="DONE"))
    #     finally:
    #         busy["flag"] = False

    # node.create_subscription(String, "/lid/command", command_cb, 10)
    # rclpy.spin(node)
    # rclpy.shutdown()


if __name__ == "__main__":
    main()
