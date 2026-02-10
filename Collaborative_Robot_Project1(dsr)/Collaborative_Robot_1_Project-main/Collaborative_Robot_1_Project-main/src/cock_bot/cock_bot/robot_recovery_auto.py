# cock_bot/robot_recovery.py
import rclpy
import sys
import time
import subprocess

from std_msgs.msg import String
from dsr_msgs2.srv import (
    GetRobotState, 
    SetRobotControl, 
    SetRobotMode,
    MoveStop
)

ROBOT_ID = "dsr01"


def main():
    rclpy.init()
    node = rclpy.create_node('robot_recovery', namespace=ROBOT_ID)
    
    # 서비스 클라이언트
    state_client = node.create_client(
        GetRobotState, f'/{ROBOT_ID}/system/get_robot_state')
    ctrl_client = node.create_client(
        SetRobotControl, f'/{ROBOT_ID}/system/set_robot_control')
    mode_client = node.create_client(
        SetRobotMode, f'/{ROBOT_ID}/system/set_robot_mode')
    stop_client = node.create_client(
        MoveStop, f'/{ROBOT_ID}/motion/move_stop')
    
    # 리셋 토픽 발행용
    reset_pub = node.create_publisher(
        String, f'/{ROBOT_ID}/cocktail/command', 10)
    
    print("[Recovery] 복구 시작...")
    
    # 1. 현재 상태 확인
    print(" -> 1. 상태 확인...")
    if state_client.wait_for_service(timeout_sec=2.0):
        req = GetRobotState.Request()
        future = state_client.call_async(req)
        rclpy.spin_until_future_complete(node, future, timeout_sec=2.0)
        if future.done() and future.result():
            print(f"    robot_state: {future.result().robot_state}")
    
    # 2. 시스템 리셋 (3 -> 2 -> 1)
    print(" -> 2. 시스템 리셋...")
    if ctrl_client.wait_for_service(timeout_sec=2.0):
        
        # Safe Off 해제
        req = SetRobotControl.Request()
        req.robot_control = 3
        future = ctrl_client.call_async(req)
        rclpy.spin_until_future_complete(node, future, timeout_sec=2.0)
        print("    [1/3] Safe Off 해제")
        time.sleep(1.0)
        
        # Safe Stop 해제
        req = SetRobotControl.Request()
        req.robot_control = 2
        future = ctrl_client.call_async(req)
        rclpy.spin_until_future_complete(node, future, timeout_sec=2.0)
        print("    [2/3] Safe Stop 해제")
        time.sleep(1.0)
        
        # Servo On
        req = SetRobotControl.Request()
        req.robot_control = 1
        future = ctrl_client.call_async(req)
        rclpy.spin_until_future_complete(node, future, timeout_sec=2.0)
        print("    [3/3] Servo On")
        time.sleep(2.0)
    
    # 3. 이전 명령 초기화
    print(" -> 3. 명령 초기화...")
    if stop_client.wait_for_service(timeout_sec=2.0):
        req = MoveStop.Request()
        req.stop_mode = 1
        future = stop_client.call_async(req)
        rclpy.spin_until_future_complete(node, future, timeout_sec=2.0)
        time.sleep(0.5)
    
    # 4. 자동 모드 전환
    print(" -> 4. 자동 모드 전환...")
    if mode_client.wait_for_service(timeout_sec=2.0):
        req = SetRobotMode.Request()
        req.robot_mode = 1
        future = mode_client.call_async(req)
        rclpy.spin_until_future_complete(node, future, timeout_sec=2.0)
        print("    robot_mode = 1 (Autonomous)")
        time.sleep(1.0)
    
    # 5. 최종 확인
    print(" -> 5. 최종 확인...")
    req = GetRobotState.Request()
    future = state_client.call_async(req)
    rclpy.spin_until_future_complete(node, future, timeout_sec=2.0)
    robot_state = future.result().robot_state if future.done() and future.result() else -1
    print(f"    robot_state: {robot_state}")
    
    if robot_state not in [1, 2]:
        print("\n[Recovery] ❌ 복구 실패")
        node.destroy_node()
        rclpy.shutdown()
        sys.exit(1)
    
    # 6. 홈 포즈로 이동
    print(" -> 6. 홈 포즈로 이동...")
    try:
        result = subprocess.run(
            ['ros2', 'run', 'cock_bot', 'home'],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print("    ✓ 홈 포즈 완료")
        else:
            print(f"    ⚠️ 홈 포즈 실패: {result.stderr}")
    except Exception as e:
        print(f"    ⚠️ 홈 포즈 에러: {e}")
    
    # 7. 오케스트레이터 리셋
    print(" -> 7. 오케스트레이터 리셋...")
    time.sleep(0.5)
    
    msg = String()
    msg.data = "reset"
    reset_pub.publish(msg)
    print("    reset 토픽 발행 완료")
    
    time.sleep(0.5)
    
    print("\n[Recovery] ✓ 복구 완료!")
    node.destroy_node()
    rclpy.shutdown()
    sys.exit(0)


if __name__ == '__main__':
    main()