<template>
  <div class="order-chart-container">
    <div class="setting-robot-title">
      데이터 통계
    </div>
    <div class="order-chart-body">
      <PieChart/>
      <BarChartTodaySales/>
      <BarChartSales/>
      <LineChartSales/>
      <LineChartPrice/>
    </div>
  </div>
</template>

<script setup lang="ts">
import PieChart from '@/components/PieChart.vue';
import BarChartSales from '@/components/BarChartSales.vue';
import LineChartSales from '@/components/LineChartSales.vue';
import LineChartPrice from '@/components/LineChartPrice.vue';
import BarChartTodaySales from '@/components/BarChartTodaySales.vue';

</script>

<style scoped lang="scss">
.order-chart-container {
  flex: 1;
  padding: 30px;
  display: flex;
  flex-direction: column;
  gap: 30px;
  box-sizing: border-box;

  .setting-robot-title {
    font-size: 28px;
    font-family: 'NanumGothicEcoBold', sans-serif;
  }

  .order-chart-body {
    height: 650px;
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    grid-template-rows: 1fr 1fr;
    gap: 10px;
  }
}
</style>