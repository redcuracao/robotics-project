<template>
  <el-card class="bar-chart">
    <Bar :data="data" :options="options" />
    <template #footer>
      <div class="card-header">
        <span>주종별 금일 판매 금액</span>
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

/**
 * 오늘 날짜 (YYYY-MM-DD)
 */
function getToday(): string {
  const today = new Date()
  const yyyy = today.getFullYear()
  const mm = String(today.getMonth() + 1).padStart(2, '0')
  const dd = String(today.getDate()).padStart(2, '0')

  return `${yyyy}-${mm}-${dd}`
}

/**
 * 금일 주종별 판매 금액 집계
 */
function getTodayCategorySalesAmount(
  orderList: OrderDetailsType[]
): {
  categories: string[]
  amounts: number[]
} {
  const today = getToday()
  const amountMap: Record<string, number> = {}

  orderList.forEach(order => {
    if (!order.time) return

    const parsedDate = new Date(order.time)
    if (Number.isNaN(parsedDate.getTime())) return

    const yyyy = parsedDate.getFullYear()
    const mm = String(parsedDate.getMonth() + 1).padStart(2, '0')
    const dd = String(parsedDate.getDate()).padStart(2, '0')

    const dateKey = `${yyyy}-${mm}-${dd}`
    if (dateKey !== today) return

    const category = order.category
    amountMap[category] =
      (amountMap[category] ?? 0) + (order.price ?? 0)
  })

  return {
    categories: Object.keys(amountMap),
    amounts: Object.values(amountMap)
  }
}

const { categories, amounts } =
  getTodayCategorySalesAmount(orderDetailsList.value)

const data = {
  labels: categories,
  datasets: [
    {
      label: '금일 판매 금액',
      data: amounts,
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
        callback: (tickValue: string | number) => {
          if (typeof tickValue === 'number') {
            return `${tickValue.toLocaleString()}원`
          }
          return tickValue
        }
      }
    }
  },
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      callbacks: {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        label: (context: any) => {
          const value = context.parsed.y
          return typeof value === 'number'
            ? `${value.toLocaleString()}원`
            : value
        }
      }
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
