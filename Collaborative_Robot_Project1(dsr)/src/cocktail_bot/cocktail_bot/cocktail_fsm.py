#!/usr/bin/env python3
import rclpy
import subprocess
from rclpy.node import Node
from std_msgs.msg import String


class CocktailFSM(Node):
    def __init__(self):
        super().__init__("cocktail_fsm")

        self.busy = False

        self.create_subscription(
            String,
            "/order",
            self.order_callback,
            10
        )

        self.get_logger().info("🍹 FSM ready. Waiting for order...")

    def run_task(self, exe_name):
        self.get_logger().info(f"▶ START {exe_name}")
        result = subprocess.run(
            ["ros2", "run", "cocktail_bot", exe_name],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            self.get_logger().error(result.stderr)
            raise RuntimeError(f"{exe_name} failed")

        self.get_logger().info(f"✔ END {exe_name}")

    def order_callback(self, msg: String):
        if self.busy:
            self.get_logger().warn("FSM busy, order ignored")
            return

        self.busy = True
        self.get_logger().info(f"주문 수신: {msg.data}")

        try:
            self.run_task("motion")
            self.run_task("close_lid")
            self.run_task("shaker_node")
            self.run_task("open_lid")
            self.run_task("pour")

            self.get_logger().info("✅ Cocktail complete")

        except Exception as e:
            self.get_logger().error(f"FSM error: {e}")

        finally:
            self.busy = False


def main():
    rclpy.init()
    node = CocktailFSM()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
