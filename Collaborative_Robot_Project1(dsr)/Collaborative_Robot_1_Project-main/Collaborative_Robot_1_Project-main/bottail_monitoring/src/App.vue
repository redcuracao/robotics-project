<template>
  <RouterView />
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import { connectROS, subscribeRobotState } from './composable/useRobot';
import { onMounted } from 'vue';
import { subscribeDB } from './composable/useFirebase';


onMounted(() => {
  connectROS() // ROS 연결
  subscribeDB() // DB 구독
  subscribeRobotState() // robot state DB 저장
})
</script>

<style scoped lang="scss">

</style>
