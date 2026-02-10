<template>
  <div class="admin-container">
    <AdminMenuBar/>
    <OrderDetailsList v-if="adminMenuState === 'orderDetails'"/>
    <OrderChart v-if="adminMenuState === 'statistics'"/>
    <SettingRobot v-if="adminMenuState === 'setting'"/>
  </div>
</template>
<script setup lang="ts">
import AdminMenuBar from '@/containers/AdminMenuBar.vue';
import OrderDetailsList from '@/components/OrderDetailsList.vue';
import OrderChart from '@/containers/OrderChart.vue';
import SettingRobot from '@/containers/SettingRobot.vue';
import useMenuStore from '@/store/storeMenuData';
import { storeToRefs } from 'pinia';

const {adminMenuState } = storeToRefs(useMenuStore())


</script>
<style scoped lang="scss">
.admin-container {
  width: 100vw;
  height: 100vh;
  display: flex;
}
</style>