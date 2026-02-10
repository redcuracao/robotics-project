# cock_bot/home_pose.py
import rclpy
import DR_init

ROBOT_ID = "dsr01"
ROBOT_MODEL = "m0609"

def main():
    DR_init.__dsr__id = ROBOT_ID
    DR_init.__dsr__model = ROBOT_MODEL
    
    rclpy.init()
    node = rclpy.create_node('home_pose', namespace=ROBOT_ID)
    DR_init.__dsr__node = node
    
    from DSR_ROBOT2 import movej, set_robot_mode, ROBOT_MODE_AUTONOMOUS
    
    print("[Home] 홈 포즈로 이동 중...")
    
    set_robot_mode(ROBOT_MODE_AUTONOMOUS)
    
    home = [0, 0, 90, 0, 90, 0]
    movej(home, vel=30, acc=30)
    
    print("[Home] ✓ 홈 포즈 완료")
    
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()