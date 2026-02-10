import { ref, type Ref } from 'vue'
import { defineStore } from 'pinia'
import type { OrderDetailsType } from '@/types/menuDataType'

const useOrderDetail = defineStore('orderDetails', () => {
  // 주문 내역
  const orderDetailsList: Ref<OrderDetailsType[]> = ref([])

  // 주문 내역 저장
  const setOrderDetailsList = (data: OrderDetailsType[]) => {
    orderDetailsList.value = data
  }

  return {
    orderDetailsList,
    setOrderDetailsList,
  }
})

export default useOrderDetail
