/* eslint-disable @typescript-eslint/no-explicit-any */
import * as ROSLIB from 'roslib'
import { reactive } from 'vue'
import type { RobotState, TopicConfig } from '@/types/robotType'
import { throttle } from '@/utils/dateUtils'
import { setDataBase } from './useFirebase'
import { watch } from 'vue'

const ros = new ROSLIB.Ros({
  url: 'ws://localhost:9090',
})

// ROS 통신 연결
const connectROS = () => {
  ros.on('connection', () => {
    if (ros == null) {
      console.log('ROS is null')
    } else {
      console.log('ROS2 Connected')
    }
  })

  ros.on('error', (error) => {
    console.error('ROS Error', error)
  })
}

/**
 *
 * @param data 토픽 메시지
 * 토픽 발행
 * 주문하기 : order:{메뉴명} // highball, mojito
 * 동작 정지 : pause
 * 동작 재개 : resume
 * 동작 복구 : recover
 */
const publishTopic = (data: string) => {
  const orderTopic = new ROSLIB.Topic({
    ros,
    name: '/dsr01/cocktail/command',
    messageType: 'std_msgs/String',
  })

  orderTopic.publish({ data })
}

// 로봇 상태값 저장
const robotState = reactive<RobotState>({
  joint: {
    deg: [],
    vel: [],
    effort: [],
  },
  tcp: {
    pos: [],
  },
  system: {
    state: 'UNKNOWN',
  },
  timestamp: 0,
})

// robotState 토픽 config
const subscribeTopicConfigs: TopicConfig[] = [
  {
    name: '/dsr01/joint_states',
    messageType: 'sensor_msgs/JointState',
    handler: (msg) => {
      robotState.joint.deg = msg.position.map((r: number) => +((r * 180) / Math.PI)) ?? []
      robotState.joint.vel = msg.velocity ?? []
      robotState.joint.effort = msg.effort ?? []
    },
  },

  {
    name: '/dsr01/cocktail/status',
    messageType: 'std_msgs/String',
    handler: (msg) => {
      robotState.system.state = msg.robot_state
    },
  },
]

// robotState 토픽 subscribe
const subscribeRobotState = () => {
  subscribeTopicConfigs.forEach((cfg) => {
    const topic = new ROSLIB.Topic({
      ros,
      name: cfg.name,
      messageType: cfg.messageType,
      throttle_rate: 50,
    })

    topic.subscribe(cfg.handler)
  })
}

// robotState DB에 저장
const writeRobotStateToDB = throttle(() => {
  setDataBase('robotStatus', {
    ...robotState,
    timestamp: Date.now(),
  })
}, 200)

// moveL 동작
const movel = (pos: number[], vel: number, acc: number, ref: number = 0) => {
  const service = new ROSLIB.Service({
    ros,
    name: '/dsr01/motion/move_line',
    serviceType: 'dsr_msgs/MoveLine',
  })

  return new Promise<{ success: boolean }>((resolve, reject) => {
    service.callService(
      { pos, vel, acc, ref },
      (res: any) => resolve(res),
      (err: any) => reject(err),
    )
  })
}

// moveJ 동작
const movej = (pos: number[], vel: number, acc: number) => {
  const service = new ROSLIB.Service({
    ros,
    name: '/dsr01/motion/move_joint',
    serviceType: 'dsr_msgs/MoveJoint',
  })

  return new Promise((resolve) => {
    service.callService({ pos, vel, acc }, resolve)
  })
}

// robotState 감지해서 writeRobotStateToDB 실행
watch(
  () => robotState,
  () => {
    writeRobotStateToDB()
  },
  { deep: true },
)

export { connectROS, publishTopic, subscribeRobotState, movel, movej }
