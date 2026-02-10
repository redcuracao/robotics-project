# cocktail_orchestrator_topic.py
import rclpy
import threading
import time
import subprocess
import os
from std_msgs.msg import String

ROBOT_ID = "dsr01"
PACKAGE_PATH = os.path.dirname(os.path.abspath(__file__))

# 상태 관리
robot_state = "IDLE"
current_recipe = None
current_step = 0
current_process = None
running = True

RECIPES = {
    "mojito": [
        'a1_motion_node.py',
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


def stop_current_task():
    global current_process
    if current_process:
        print("[Stop] 현재 스크립트 종료")
        try:
            current_process.terminate()
            current_process.wait(timeout=2)
        except:
            pass
        current_process = None


def run_recovery():
    """복구 실행 (별도 스레드)"""
    global robot_state
    
    try:
        result = subprocess.run(
            ['ros2', 'run', 'cock_bot', 'robot_recovery_auto'],
            capture_output=True,
            text=True,
            timeout=60
        )
        print(result.stdout)
        
        if result.returncode == 0:
            print("[Recovery] ✓ 복구 완료")
            # robot_recovery에서 reset 토픽 발행하므로 여기선 안 해도 됨
        else:
            print("[Recovery] ❌ 복구 실패")
            publish_status("recovery_failed")
    except Exception as e:
        print(f"[Recovery] 에러: {e}")
        publish_status("recovery_error")


def robot_state_callback(msg):
    global robot_state
    
    data = msg.data
    try:
        hw_state = int(data.split(':')[0])
    except:
        return
    
    if robot_state == "RUNNING" and hw_state in [3, 4, 5]:
        print(f"\n[Monitor] ⚠️ 에러 감지! ({data})")
        robot_state = "ERROR"
        stop_current_task()
        publish_status(f"error_detected:{data}")


def command_callback(msg):
    global robot_state, current_recipe, current_step
    command = msg.data.strip()
    
    print(f"\n========== [Command] 수신: {command} ==========")
    print(f"[Command] 현재 상태: {robot_state}")
    
    if command.startswith("order:"):
        recipe = command.split(":", 1)[1]
        
        if robot_state == "RUNNING":
            print("[Command] 이미 제조 중!")
            publish_status("busy")
            return
        if robot_state == "ERROR":
            print("[Command] 에러 상태 - 먼저 recover 필요!")
            publish_status("need_recover")
            return
        if robot_state == "RECOVERING":
            print("[Command] 복구 중!")
            publish_status("recovering")
            return
        if recipe not in RECIPES:
            print(f"[Command] 알 수 없는 레시피: {recipe}")
            publish_status(f"error:unknown_recipe:{recipe}")
            return
        
        current_recipe = recipe
        current_step = 0
        robot_state = "RUNNING"
        print(f"[Command] 주문 접수: {recipe}")
        publish_status(f"ordered:{recipe}")
        
        task_t = threading.Thread(target=execute_recipe, args=(recipe,), daemon=True)
        task_t.start()
    
    elif command == "pause":
        if robot_state == "RUNNING":
            robot_state = "PAUSED"
            print("[Command] 일시정지")
            publish_status("paused")
    
    elif command == "resume":
        if robot_state == "PAUSED":
            robot_state = "RUNNING"
            print("[Command] 재개")
            publish_status("resumed")
    
    elif command == "stop":
        print("[Command] 정지")
        robot_state = "ERROR"
        stop_current_task()
        publish_status("stopped")
    
    elif command == "emergency":
        print("[Command] 긴급 정지")
        robot_state = "ERROR"
        stop_current_task()
        publish_status("emergency_stopped")
    
    elif command == "recover":
        if robot_state == "RECOVERING":
            print("[Command] 이미 복구 중!")
            publish_status("already_recovering")
            return
        
        print("[Command] 복구 시작...")
        robot_state = "RECOVERING"
        publish_status("recovering")
        
        recover_t = threading.Thread(target=run_recovery, daemon=True)
        recover_t.start()
    
    elif command == "reset":
        print("[Command] 리셋")
        robot_state = "IDLE"
        current_recipe = None
        current_step = 0
        publish_status("reset_done")
    
    elif command == "status":
        print(f"[Command] state:{robot_state} | recipe:{current_recipe} | step:{current_step}")
        publish_status(f"state:{robot_state}|recipe:{current_recipe}|step:{current_step}")


def execute_recipe(recipe):
    """레시피 실행 (별도 스레드)"""
    global robot_state, current_recipe, current_step, current_process
    
    steps = RECIPES[recipe]
    print(f"\n[Robot] 🍸 {recipe} 제조 시작 ({len(steps)} 스텝)")
    publish_status(f"making:{recipe}")
    
    success = True
    for i, script in enumerate(steps, 1):
        current_step = i
        
        while robot_state == "PAUSED":
            print("[Robot] ⏸️ 일시정지 중...")
            time.sleep(0.5)
        
        if robot_state == "ERROR":
            print("[Robot] ⚠️ 에러로 중단")
            success = False
            break
        
        print(f"\n[Robot] [{i}/{len(steps)}] {script}")
        publish_status(f"step:{i}:{len(steps)}:{script}")
        
        returncode, stderr = run_script(script)
        
        if robot_state == "ERROR":
            success = False
            break
        
        if returncode != 0:
            print(f"[Robot] ❌ {script} 실패")
            publish_status(f"script_error:{script}")
            robot_state = "ERROR"
            success = False
            break
        
        print(f"[Robot] ✓ {script} 완료")
    
    if success and robot_state == "RUNNING":
        print(f"\n[Robot] 🍸 {recipe} 완성!")
        publish_status(f"done:{recipe}")
    
    robot_state = "IDLE"
    current_recipe = None
    current_step = 0


def run_script(script):
    """모션 스크립트 실행"""
    global current_process, robot_state
    
    script_path = os.path.join(PACKAGE_PATH, script)
    current_process = subprocess.Popen(
        ['python3', script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    while current_process is not None and current_process.poll() is None:
        if robot_state == "ERROR":
            try:
                if current_process:
                    current_process.terminate()
                    current_process.wait(timeout=2)
            except:
                pass
            current_process = None
            return -1, "stopped"
        time.sleep(0.1)
    
    if current_process is None:
        return -1, "stopped"
    
    stdout, stderr = current_process.communicate()
    returncode = current_process.returncode
    current_process = None
    
    if stdout:
        print(f"[Output] {stdout.strip()}")
    
    return returncode, stderr


def sub_thread(sub_node):
    executor = rclpy.executors.SingleThreadedExecutor()
    executor.add_node(sub_node)
    
    while running:
        executor.spin_once(timeout_sec=0.1)


def main():
    global status_pub, running
    
    rclpy.init()
    node = rclpy.create_node("cocktail_orchestrator", namespace=ROBOT_ID)
    
    node.create_subscription(
        String, f"/{ROBOT_ID}/cocktail/command", command_callback, 10)
    
    node.create_subscription(
        String, f"/{ROBOT_ID}/robot/state", robot_state_callback, 10)
    
    status_pub = node.create_publisher(
        String, f"/{ROBOT_ID}/cocktail/status", 10)
    
    sub_t = threading.Thread(target=sub_thread, args=(node,), daemon=True)
    sub_t.start()
    
    print("\n" + "="*60)
    print("  🍸 칵테일 오케스트레이터")
    print("="*60)
    print(f"레시피: {list(RECIPES.keys())}")
    print("-"*60)
    print("명령어:")
    print("  order:레시피  - 주문")
    print("  pause        - 일시정지")
    print("  resume       - 재개")
    print("  stop         - 정지")
    print("  emergency    - 긴급정지")
    print("  recover      - 복구 (홈 포즈까지)")
    print("  reset        - 리셋")
    print("  status       - 상태 확인")
    print("="*60 + "\n")
    
    publish_status("ready")
    
    try:
        while running:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n[Main] Ctrl+C")
        running = False
    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()