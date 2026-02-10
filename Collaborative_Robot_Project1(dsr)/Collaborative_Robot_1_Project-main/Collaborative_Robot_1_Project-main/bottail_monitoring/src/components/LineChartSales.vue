<template>
  <el-card class="line-chart">
    <Line :data="data" :options="options" />
    <template #footer>
      <div class="card-header">
        <span>최근 7일간 판매량</span>
      </div>
    </template>
  </el-card>
</template>

<script setup lang="ts">
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
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
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale
)

const { orderDetailsList } = storeToRefs(useOrderDetail())

/**
 * 오늘 기준 최근 7일 날짜 배열 생성 (YYYY-MM-DD)
 */
function getLast7Days(): string[] {
  const days: string[] = []

  for (let i = 6; i >= 0; i--) {
    const date = new Date()
    date.setDate(date.getDate() - i)

    const yyyy = date.getFullYear()
    const mm = String(date.getMonth() + 1).padStart(2, '0')
    const dd = String(date.getDate()).padStart(2, '0')

    days.push(`${yyyy}-${mm}-${dd}`)
  }

  return days
}

/**
 * 최근 7일간 일자별 판매 수량 집계
 */
function getWeeklySalesCounts(
  orderList: OrderDetailsType[]
): {
  dates: string[]
  counts: number[]
} {
  const dates = getLast7Days()
  const countMap: Record<string, number> = {}

  dates.forEach(date => {
    countMap[date] = 0
  })

  orderList.forEach(order => {
  if (!order.time) return

  const datePart = order.time.split(' ')[0]
  if (!datePart) return

  if (datePart in countMap) {
    countMap[datePart] = (countMap[datePart] ?? 0) + 1
  }
})

  return {
    dates,
    counts: dates.map(date => countMap[date] ?? 0)
  }
}

const { dates, counts } =
  getWeeklySalesCounts(orderDetailsList.value)

const data = {
  labels: dates,
  datasets: [
    {
      label: '판매 수량',
      data: counts,
      borderColor: 'rgb(54, 162, 235)',
      backgroundColor: 'rgba(54, 162, 235, 0.2)',
      tension: 0.3,
      fill: true
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
.line-chart {
  width: 100%;
  height: 100%;
}

.card-header {
  text-align: center;
}
</style>
