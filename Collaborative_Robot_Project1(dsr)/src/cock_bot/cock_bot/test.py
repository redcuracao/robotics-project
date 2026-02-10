#!/usr/bin/env python3
import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool
from sensor_msgs.msg import JointState


class DSRCollisionMonitor(Node):
    """
    충돌 여부 판단 후
    복구 대기 상태로 전환
    + ROS2 콘솔에 상태 문구 출력
    """

    def __init__(self):
        super().__init__("dsr_collision_monitor")

        # ===== 파라미터 =====
        self.joint_timeout = 1.0
        self.confirm_sec = 2.0

        # ===== 상태 =====
        self.last_joint_rx = None
        self.disconnect_since = None
        self.collision_detected = False
        self.state = "BOOT"

        # ===== Publisher =====
        self.pub = self.create_publisher(
            String, "/robot/safety_state", 10
        )

        # ===== Subscribers =====
        self.create_subscription(
            JointState,
            "/dsr01/joint_states",
            self.on_joint,
            10
        )

        self.create_subscription(
            Bool,
            "/dsr01/robot_disconnection",
            self.on_disconnect,
            10
        )

        self.create_timer(0.1, self.tick)

        self.get_logger().info("DSR Collision Monitor started")

    # ---------- Callbacks ----------
    def on_joint(self, msg):
        self.last_joint_rx = time.monotonic()

        if not self.collision_detected:
            self.set_state("RUNNING")

        self.disconnect_since = None

    def on_disconnect(self, msg: Bool):
        if msg.data and not self.collision_detected:
            self.mark_collision("DSR robot_disconnection")

    # ---------- Logic ----------
    def tick(self):
        if self.collision_detected:
            return  # 복구 대기 중

        if self.last_joint_rx is None:
            return

        if time.monotonic() - self.last_joint_rx > self.confirm_sec:
            self.mark_collision("joint_states timeout")

    def mark_collision(self, reason):
        self.collision_detected = True
        self.set_state("COLLISION_DETECTED")
        self.get_logger().error(f"[충돌 감지] 원인: {reason}")
        self.set_state("RECOVERY_WAIT")

    # ---------- State Handling ----------
    def set_state(self, new_state):
        if new_state == self.state:
            return

        self.state = new_state
        self.pub.publish(String(data=new_state))

        # 사람용 콘솔 메시지
        if new_state == "RUNNING":
            self.get_logger().info("[정상] 로봇 정상 동작 중")

        elif new_state == "COLLISION_DETECTED":
            self.get_logger().warn("[경고] 충돌 감지됨")

        elif new_state == "RECOVERY_WAIT":
            self.get_logger().warn("[대기] 안전 해제 및 복구 승인 대기 중")

        else:
            self.get_logger().info(f"[상태] {new_state}")


def main():
    rclpy.init()
    node = DSRCollisionMonitor()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
