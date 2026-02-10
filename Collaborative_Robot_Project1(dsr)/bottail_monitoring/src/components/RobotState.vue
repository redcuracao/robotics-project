<template>
  <div class="robot-state-container">
    <el-card>
        <template #header>
          <div class="card-header">
            <span>로봇 상태</span>
          </div>
        </template>
        <div class="robot-state-card">
          <div class="robot-state-card-body">
            <span>상태 :</span>
            <el-tag size="large">{{ robotState?.system?.state }}</el-tag>
          </div>
          <div class="robot-state-card-body">
            <span>시간 :</span>
            <span>{{ formatTimestamp(robotState?.timestamp) }}</span>
          </div>
        </div>
    </el-card>
    <el-card>
      <template #header>
        <div class="card-header">
          <span>TCP 좌표 (Base 기준)</span>
        </div>
      </template>
      <div class="robot-tcp-card">
        <div class="robot-tcp-card-body">
          <div class="robot-tcp-card-item">
            <span>X :</span>
            <span>{{ robotState?.tcp?.pos[0] }} mm</span>
          </div>
          <div class="robot-tcp-card-item">
            <span>Y :</span>
            <span>{{ robotState?.tcp?.pos[1] }} mm</span>
          </div>
          <div class="robot-tcp-card-item">
            <span>Z :</span>
            <span>{{ robotState?.tcp?.pos[2] }} mm</span>
          </div>
        </div>
        <el-divider />
        <div class="robot-tcp-card-body">
          <div class="robot-tcp-card-item">
            <span>A :</span>
            <span>{{ robotState?.tcp?.pos[3] }} deg</span>
          </div>
          <div class="robot-tcp-card-item">
            <span>B :</span>
            <span>{{ robotState?.tcp?.pos[4] }} deg</span>
          </div>
          <div class="robot-tcp-card-item">
            <span>C :</span>
            <span>{{ robotState?.tcp?.pos[5] }} deg</span>
          </div>
        </div>
      </div>
    </el-card>
    <el-card>
      <template #header>
        <div class="card-header">
          <span>관절 각도 (deg)</span>
        </div>
      </template>
      <div class="robot-joint-card">
        <div class="robot-joint-card-body">
          <span>J1 :</span>
          <div class="robot-joint-item">
            <span>{{ robotState?.joint?.deg[0]?.toFixed(3) }} deg</span>
            <span>{{ robotState?.joint?.vel[0]?.toFixed(3) }} mm/s</span>
          </div>
        </div>
        <div class="robot-joint-card-body">
          <span>J2 :</span>
          <div class="robot-joint-item">
            <span>{{ robotState?.joint?.deg[1]?.toFixed(3) }} deg</span>
            <span>{{ robotState?.joint?.vel[1]?.toFixed(3) }} mm/s</span>
          </div>
        </div>
        <div class="robot-joint-card-body">
          <span>J3 :</span>
          <div class="robot-joint-item">
            <span>{{ robotState?.joint?.deg[2]?.toFixed(3) }} deg</span>
            <span>{{ robotState?.joint?.vel[2]?.toFixed(3) }} mm/s</span>
          </div>
        </div>
        <div class="robot-joint-card-body">
          <span>J4 :</span>
          <div class="robot-joint-item">
            <span>{{ robotState?.joint?.deg[3]?.toFixed(3) }} deg</span>
            <span>{{ robotState?.joint?.vel[3]?.toFixed(3) }} mm/s</span>
          </div>
        </div>
        <div class="robot-joint-card-body">
          <span>J5 :</span>
          <div class="robot-joint-item">
            <span>{{ robotState?.joint?.deg[4]?.toFixed(3) }} deg</span>
            <span>{{ robotState?.joint?.vel[4]?.toFixed(3) }} mm/s</span>
          </div>
        </div>
        <div class="robot-joint-card-body">
          <span>J6 :</span>
          <div class="robot-joint-item">
            <span>{{ robotState?.joint?.deg[5]?.toFixed(3) }} deg</span>
            <span>{{ robotState?.joint?.vel[5]?.toFixed(3) }} mm/s</span>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import useRobotStore from '@/store/storeRobot';
import { storeToRefs } from 'pinia';
import { formatTimestamp } from '@/utils/dateUtils'

const { robotState } = storeToRefs(useRobotStore())

</script>

<style scoped lang="scss">
.robot-state-container {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 10px;

  .card-header {
    font-size: 20px;
    text-align: center;
  }

  .robot-state-card {
    display: flex;
    gap: 20px;
    flex-direction: column;

    .robot-state-card-body {
      display: flex;
      gap: 10px;
      align-items: center;
    }
  }

  .robot-tcp-card {
    display: flex;
    flex-direction: column;

    .robot-tcp-card-body {
      display: flex;
      flex-direction: column;
      gap: 20px;

      .robot-tcp-card-item {
        display: flex;
        gap: 10px;
      }
    }
  }

  .robot-joint-card {
    display: flex;
    flex-direction: column;
    gap: 20px;

    .robot-joint-card-body {
      display: flex;
      gap: 10px;

      .robot-joint-item {
        flex: 1;
        display: grid;
        grid-template-columns: 1fr 1fr;
      }
    }
  }
}
</style>