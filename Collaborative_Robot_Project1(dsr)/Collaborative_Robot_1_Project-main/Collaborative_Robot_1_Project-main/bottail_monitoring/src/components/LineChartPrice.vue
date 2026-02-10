<template>
  <el-card class="line-chart">
    <Line :data="data" :options="options" />
    <template #footer>
      <div class="card-header">
        <span>최근 7일간 총 판매 금액</span>
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
 * 오늘 포함 최근 7일 (YYYY-MM-DD)
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
 * 최근 7일간 일자별 판매 금액 합계
 */
function getWeeklySalesAmounts(
  orderList: OrderDetailsType[]
): {
  dates: string[]
  amounts: number[]
} {
  const dates = getLast7Days()
  const amountMap: Record<string, number> = {}

  // 날짜 초기화
  dates.forEach(date => {
    amountMap[date] = 0
  })

  orderList.forEach(order => {
    if (!order.time) return

    const parsedDate = new Date(order.time)
    if (Number.isNaN(parsedDate.getTime())) return

    const yyyy = parsedDate.getFullYear()
    const mm = String(parsedDate.getMonth() + 1).padStart(2, '0')
    const dd = String(parsedDate.getDate()).padStart(2, '0')

    const dateKey = `${yyyy}-${mm}-${dd}`

    if (dateKey in amountMap) {
      amountMap[dateKey] =
        (amountMap[dateKey] ?? 0) + (order.price ?? 0)
    }
  })

  return {
    dates,
    amounts: dates.map(date => amountMap[date] ?? 0)
  }
}

const { dates, amounts } =
  getWeeklySalesAmounts(orderDetailsList.value)

const data = {
  labels: dates,
  datasets: [
    {
      label: '총 판매 금액',
      data: amounts,
      borderColor: 'rgb(255, 159, 64)',
      backgroundColor: 'rgba(255, 159, 64, 0.2)',
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
        callback: (tickValue: string | number) => {
          if (typeof tickValue === 'number') {
            return `${tickValue.toLocaleString()} ₩`
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
        label: (context: any) =>
          `${context.parsed.y.toLocaleString()}원`
      }
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
