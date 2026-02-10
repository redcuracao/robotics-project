# cocktail_orchestrator_simple.py
import rclpy
import threading
import time
import subprocess
import os
from std_msgs.msg import String

ROBOT_ID = "dsr01"
PACKAGE_PATH = os.path.dirname(os.path.abspath(__file__))

robot_state = "IDLE"
current_recipe = None
current_step = 0
current_process = None
state_lock = threading.Lock()
pause_event = threading.Event()
pause_event.set()

RECIPES = {
    "mojito": [
        'a_motion_node.py',
        'b_put_shaker.py',
        'c_close_cap.py',
        'd_get_shaker.py',
        'e_shaking.py',
        'f_put_shaker.py',
        'g_twist_open_cap.py',
        'h_pour_drink.py',
    ],
    "highball": [
        'a_motion_node.py',
        'b_put_shaker.py',
        'i_spoon.py',
        'h_pour_drink.py',
    ],
}

status_pub = None


def publish_status(status):
    global status_pub
    if status_pub:
        msg = String()
        msg.data = status
        status_pub.publish(msg)
        print(f"[Status] {status}")


def command_callback(msg):
    global robot_state, current_recipe, current_step
    command = msg.data.strip()
    
    print(f"\n[Command] {command}")
    
    with state_lock:
        if command.startswith("order:"):
            recipe = command.split(":", 1)[1]
            if robot_state == "RUNNING":
                publish_status("busy")
                return
            if recipe in RECIPES:
                current_recipe = recipe
                current_step = 0
                robot_state = "RUNNING"
                pause_event.set()
                publish_status(f"ordered:{recipe}")
        
        elif command == "pause":
            if robot_state == "RUNNING":
                robot_state = "PAUSED"
                pause_event.clear()
                publish_status("paused")
        
        elif command == "resume":
            if robot_state == "PAUSED":
                robot_state = "RUNNING"
                pause_event.set()
                publish_status("resumed")
        
        elif command == "stop":
            robot_state = "STOPPED"
            pause_event.set()
            if current_process:
                current_process.terminate()
            publish_status("stopped")
            # IDLE로 복귀
            robot_state = "IDLE"
            current_recipe = None


def sub_thread(sub_node):
    executor = rclpy.executors.SingleThreadedExecutor()
    executor.add_node(sub_node)
    executor.spin()


def run_script(script):
    global current_process
    
    script_path = os.path.join(PACKAGE_PATH, script)
    current_process = subprocess.Popen(
        ['python3', script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = current_process.communicate()
    returncode = current_process.returncode
    current_process = None
    
    return returncode, stderr


def robot_task_thread():
    global robot_state, current_recipe, current_step
    
    publish_status("ready")
    
    while True:
        with state_lock:
            state = robot_state
            recipe = current_recipe
        
        if state == "STOPPED":
            break
        
        if state == "IDLE" or recipe is None:
            time.sleep(0.3)
            continue
        
        if state == "RUNNING" and recipe:
            steps = RECIPES[recipe]
            print(f"\n[Robot] 🍸 {recipe} 제조 시작")
            publish_status(f"making:{recipe}")
            
            success = True
            for i, script in enumerate(steps, 1):
                current_step = i
                
                with state_lock:
                    state = robot_state
                
                if state == "PAUSED":
                    print("[Robot] ⏸️ 일시정지")
                    pause_event.wait()
                
                with state_lock:
                    state = robot_state
                
                if state != "RUNNING":
                    success = False
                    break
                
                print(f"[Robot] [{i}/{len(steps)}] {script}")
                publish_status(f"step:{i}:{len(steps)}:{script}")
                
                returncode, stderr = run_script(script)
                
                if returncode != 0:
                    print(f"[Robot] ❌ 실패: {stderr}")
                    publish_status(f"error:{script}")
                    success = False
                    break
                
                print(f"[Robot] ✓ 완료")
            
            with state_lock:
                if success:
                    print(f"[Robot] 🍸 {recipe} 완성!")
                    publish_status(f"done:{recipe}")
                robot_state = "IDLE"
                current_recipe = None


def main():
    global status_pub
    
    rclpy.init()
    node = rclpy.create_node("cocktail_orchestrator", namespace=ROBOT_ID)
    
    node.create_subscription(String, f"/{ROBOT_ID}/cocktail/command", command_callback, 10)
    status_pub = node.create_publisher(String, f"/{ROBOT_ID}/cocktail/status", 10)
    
    sub_t = threading.Thread(target=sub_thread, args=(node,), daemon=True)
    sub_t.start()
    
    robot_t = threading.Thread(target=robot_task_thread, daemon=False)
    robot_t.start()
    
    print("\n" + "="*50)
    print("  🍸 칵테일 오케스트레이터 (간소화)")
    print("="*50)
    print("명령: order:레시피 / pause / resume / stop")
    print("="*50 + "\n")
    
    try:
        robot_t.join()
    except KeyboardInterrupt:
        with state_lock:
            robot_state = "STOPPED"
        pause_event.set()
    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()