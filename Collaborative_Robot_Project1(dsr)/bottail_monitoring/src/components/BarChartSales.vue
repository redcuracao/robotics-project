<template>
  <el-card class="bar-chart">
    <Bar :data="data" :options="options" />
    <template #footer>
      <div class="card-header">
        <span>주종별 총 판매 수량</span>
      </div>
    </template>
  </el-card>
</template>

<script setup lang="ts">
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'
import useOrderDetail from '@/store/storeOrderDetails'
import { storeToRefs } from 'pinia'
import type { OrderDetailsType } from '@/types/menuDataType'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
)

const { orderDetailsList } = storeToRefs(useOrderDetail())

function getCategoryAndCountArrays(
  orderList: OrderDetailsType[]
): {
  categories: string[]
  counts: number[]
} {
  const countMap: Record<string, number> = {}

  orderList.forEach(order => {
    countMap[order.category] = (countMap[order.category] ?? 0) + 1
  })

  const categories: string[] = []
  const counts: number[] = []

  for (const category in countMap) {
    categories.push(category)
    counts.push(countMap[category] ?? 0)
  }

  return {
    categories,
    counts
  }
}

const { categories, counts } =
  getCategoryAndCountArrays(orderDetailsList.value)

const data = {
  labels: categories,
  datasets: [
    {
      label: '판매 수량',
      data: counts,
      backgroundColor: [
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
        'rgb(255, 205, 86)',
        'rgb(75, 192, 192)',
        'rgb(153, 102, 255)',
        'rgb(255, 159, 64)'
      ]
    }
  ]
}

const options = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        stepSize: 1
      }
    }
  },
  plugins: {
    legend: {
      display: false
    }
  }
}
</script>

<style scoped lang="scss">
.bar-chart {
  width: 100%;
  height: 100%;
}

.card-header {
  text-align: center;
}
</style>
