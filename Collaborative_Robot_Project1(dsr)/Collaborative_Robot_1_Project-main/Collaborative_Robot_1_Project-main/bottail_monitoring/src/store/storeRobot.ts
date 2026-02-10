import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { RobotState } from '@/types/robotType'
import { reorderArray } from '@/utils/mathUtils'

const useRobotStore = defineStore('robot', () => {
  // 로봇 상태값
  const robotState = ref({
    joint: {
      deg: [0, 0, 0, 0, 0, 0],
      vel: [0.000, 0.000, 0.000, 0.000, 0.000, 0.000],
      effort: [0, 0, 0, 0, 0, 0],
    },
    tcp: {
      pos: [0, 0, 0, 0, 0, 0],
    },
    system: {
      state: 'null',
    },
    timestamp: 0,
  })

  const setRobotState = (state: RobotState) => {
    const updatedRobotState = {
      ...state,
      joint: {
        ...state.joint,
        deg: reorderArray(state.joint.deg) as number[]
      }
    };
    robotState.value = updatedRobotState
  }

  return {
    robotState,
    setRobotState,
  }
})

export default useRobotStore
