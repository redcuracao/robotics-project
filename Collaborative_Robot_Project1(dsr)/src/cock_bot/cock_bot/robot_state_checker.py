# cock_bot/robot_state_monitor.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from dsr_msgs2.srv import GetRobotState
import time

ROBOT_ID = "dsr01"


class RobotStateMonitor(Node):
    def __init__(self):
        super().__init__('robot_state_monitor', namespace=ROBOT_ID)
        
        # 상태 발행 토픽
        self.state_pub = self.create_publisher(
            String, f'/{ROBOT_ID}/robot/state', 10)
        
        # 서비스 클라이언트
        self.state_client = self.create_client(
            GetRobotState, f'/{ROBOT_ID}/system/get_robot_state')
        
        # 이전 상태 저장 (변화 감지용)
        self.prev_state = None
        
        # 타이머 (500ms마다 체크)
        self.timer = self.create_timer(0.5, self.check_state)
        
        self.get_logger().info('로봇 상태 모니터 시작')
    
    def check_state(self):
        if not self.state_client.wait_for_service(timeout_sec=1.0):
            return
        
        request = GetRobotState.Request()
        future = self.state_client.call_async(request)
        future.add_done_callback(self.state_callback)
    
    def state_callback(self, future):
        try:
            result = future.result()
            if result is None:
                return
            
            state = result.robot_state
            
            # 상태 메시지
            STATE_MSG = {
                1: "normal",
                2: "moving",
                3: "protective_stop",
                4: "emergency_stop",
                5: "error"
            }
            
            state_str = STATE_MSG.get(state, f"unknown:{state}")
            
            # 상태 변화 감지
            if state != self.prev_state:
                self.get_logger().info(f'상태 변화: {self.prev_state} → {state} ({state_str})')
                self.prev_state = state
                
                # 에러 상태 감지 (3, 4, 5)
                if state in [3, 4, 5]:
                    self.get_logger().warn(f'⚠️ 에러 감지: {state_str}')
            
            # 상태 발행
            msg = String()
            msg.data = f"{state}:{state_str}"
            self.state_pub.publish(msg)
            
        except Exception as e:
            self.get_logger().error(f'상태 확인 에러: {e}')


def main():
    rclpy.init()
    node = RobotStateMonitor()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()