<template>
  <div class="setting-robot-container">
    <div class="setting-robot-title">
      로봇 관리
    </div>
    <div class="setting-robot-body">
      <el-menu
        :default-active="activeIndex"
        mode="horizontal"
        @select="handleSelect"
      >
        <el-menu-item index="state">로봇 상태</el-menu-item>
        <el-menu-item index="control">로봇 조그</el-menu-item>
        <el-menu-item index="recovery">로봇 복구</el-menu-item>
      </el-menu>
      <div>
        <RobotState v-if="activeIndex === 'state'"/>
        <RobotControl v-if="activeIndex === 'control'"/>
        <RobotRecovery v-if="activeIndex === 'recovery'"/>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import RobotState from '@/components/RobotState.vue';
import RobotControl from '@/components/RobotControl.vue';
import RobotRecovery from '@/components/RobotRecovery.vue';

const activeIndex = ref('state')

const handleSelect = (_: string, keyPath: string[]) => {
  activeIndex.value = keyPath[0] ?? 'state'
}

</script>

<style scoped lang="scss">
.setting-robot-container {
  flex: 1;
  padding: 30px;
  display: flex;
  flex-direction: column;
  gap: 20px;

  .setting-robot-title {
    font-size: 28px;
    font-family: 'NanumGothicEcoBold', sans-serif;
  }

  .setting-robot-body {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
}

</style>