<template>
  <div class="robot-control-container">
    <div class="robot-control-body">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>Joint Control (MoveJ)</span>
          </div>
        </template>
        <div class="robot-control-slider-wrap">
          <div class="robot-control-slider">
            <span>joint 1 (deg)</span>
            <el-slider v-model="moveState.joint[0]" :min="-170" :max="170" show-input />
          </div>
          <div class="robot-control-slider">
            <span>joint 2 (deg)</span>
            <el-slider v-model="moveState.joint[1]" :min="-120" :max="120" show-input />
          </div>
          <div class="robot-control-slider">
            <span>joint 3 (deg)</span>
            <el-slider v-model="moveState.joint[2]" :min="-170" :max="170" show-input />
          </div>
          <div class="robot-control-slider">
            <span>joint 4 (deg)</span>
            <el-slider v-model="moveState.joint[3]" :min="-190" :max="190" show-input />
          </div>
          <div class="robot-control-slider">
            <span>joint 5 (deg)</span>
            <el-slider v-model="moveState.joint[4]" :min="-120" :max="120" show-input />
          </div>
          <div class="robot-control-slider">
            <span>joint 6 (deg)</span>
            <el-slider v-model="moveState.joint[5]" :min="-360" :max="360" show-input />
          </div>
        </div>
      </el-card>
      <el-card>
        <template #header>
          <div class="card-header">
            <span>Cartesian Control (MoveL)</span>
          </div>
        </template>
        <div class="robot-control-slider-wrap">
          <div class="robot-control-slider">
            <span>X (mm)</span>
            <el-slider v-model="moveState.pos[0]" :min="-900" :max="900" show-input />
          </div>
          <div class="robot-control-slider">
            <span>Y (mm)</span>
            <el-slider v-model="moveState.pos[1]" :min="-900" :max="900" show-input />
          </div>
          <div class="robot-control-slider">
            <span>Z (mm)</span>
            <el-slider v-model="moveState.pos[2]" :min="-200" :max="1000" show-input />
          </div>
          <div class="robot-control-slider">
            <span>A (deg)</span>
            <el-slider v-model="moveState.pos[3]" :min="-180" :max="180" show-input />
          </div>
          <div class="robot-control-slider">
            <span>B (deg)</span>
            <el-slider v-model="moveState.pos[4]" :min="-180" :max="180" show-input />
          </div>
          <div class="robot-control-slider">
            <span>C (deg)</span>
            <el-slider v-model="moveState.pos[5]" :min="-180" :max="180" show-input />
          </div>
        </div>
      </el-card>
    </div>
    <el-card>
      <div class="robot-control-footer">
        <div class="robot-control-footer-left">
          <div class="robot-control-footer-slide">
            <span>Velocity</span>
            <el-slider v-model="moveState.vel" :min="0" :max="100" show-input />
          </div>
          <div class="robot-control-footer-slide">
            <span>Acceleration</span>
            <el-slider v-model="moveState.acc" :min="0" :max="100" show-input />
          </div>
        </div>
        <div class="robot-control-footer-right">
          <el-select v-model="moveState.ref" size="large" style="width: 100%">
            <el-option
              label="BASE"
              :value="0"
            />
            <el-option
              label="TOOL"
              :value="1"
            />
            <el-option
              label="USER"
              :value="2"
            />
          </el-select>
          <div class="robot-control-footer-right-button">
            <el-button
              size="large"
              type="warning"
              @click="movej(moveState.joint, moveState.vel, moveState.acc)"
            >
              Move J
            </el-button>
            <el-button
              size="large"
              type="success"
              @click="movel(moveState.pos, moveState.vel, moveState.acc, moveState.ref)"
            >
              Move L
            </el-button>
          </div>
        </div>
      </div>

    </el-card>
  </div>
</template>

<script setup lang="ts">
import useRobotStore from '@/store/storeRobot';
import { storeToRefs } from 'pinia';
import { onMounted, reactive } from 'vue';
import { movel, movej } from '@/composable/useRobot'

const { robotState } = storeToRefs(useRobotStore())

const moveState = reactive({
  pos: [0, 0, 0, 0, 0, 0],
  joint: [0, 0, 0, 0, 0, 0],
  vel: 60,
  acc: 60,
  ref: 0
})

onMounted(() => {
  moveState.pos = robotState.value?.tcp?.pos ?? [0, 0, 0, 0, 0, 0]
  moveState.joint = robotState.value?.joint?.deg ?? [0, 0, 0, 0, 0, 0]
})
</script>

<style scoped lang="scss">
.robot-control-container {
  display: flex;
  flex-direction: column;
  gap: 10px;

  .robot-control-body {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;

    .card-header {
      font-size: 20px;
      text-align: center;
    }

    .robot-control-slider-wrap {
      display: flex;
      flex-direction: column;
      gap: 3px;

      .robot-control-slider {
        display: flex;
        flex-direction: column;
        gap: 5px;

        span {
          font-size: 16px;
        }
      }
    }
  }

  .robot-control-footer {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 40px;

    .robot-control-footer-left {
      display: flex;
      flex-direction: column;
      gap: 10px;

      .robot-control-footer-slide {
        display: flex;
        flex-direction: column;
      }
    }

    .robot-control-footer-right {
      display: flex;
      flex-direction: column;
      gap: 20px;

      .robot-control-footer-right-button {
        display: flex;
        gap: 10px;

        button {
          width: 100%;
        }
      }
    }
  }
}
</style>