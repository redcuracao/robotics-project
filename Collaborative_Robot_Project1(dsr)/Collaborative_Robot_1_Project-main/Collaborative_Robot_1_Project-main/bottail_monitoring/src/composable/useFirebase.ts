/* eslint-disable @typescript-eslint/no-explicit-any */
import { ref, onValue, get, set, push, update } from 'firebase/database'
import { database } from '@/firebase'
import type { OrderDetailsType } from '../types/menuDataType'
import useOrderDetail from '@/store/storeOrderDetails'
import useRobotStore from '@/store/storeRobot'

// DB 변동이 생길때마다 저장
const subscribeDB = () => {
  const orderDetailsRef = ref(database, 'orderDetails')
  const robotStateRef = ref(database, 'robotStatus')

  const { setOrderDetailsList } = useOrderDetail()
  const { setRobotState } = useRobotStore()

  if (orderDetailsRef) {
    onValue(orderDetailsRef, (snapshot) => {
      const data = snapshot.val()
      const list: OrderDetailsType[] = data ? Object.values(data) : []
      // console.log('주문내역', list)
      setOrderDetailsList(list)
    })
  }

  if (robotStateRef) {
    onValue(robotStateRef, (snapshot) => {
      const data = snapshot.val()

      setRobotState(data)
    })
  }
}

// DB 데이터 가져오기
const getDataBase = async (path: string) => {
  const data = await get(ref(database, path))

  if (data.exists()) {
    console.log('DB data', data.val())
    return data.val()
  } else {
    console.log('데이터가 없습니다.')
  }
}

// DB 데이터 저장
const setDataBase = async (path: string, data: any) => {
  await set(ref(database, path), data)
}

// DB 데이터 추가
const pushDataBase = async (path: string, data: any) => {
  const orderDetailsRef = ref(database, path)

  push(orderDetailsRef, data)
}

// DB 데이터 업데이트
const updateDataBase = (path: string, data: any) => {
  update(ref(database, path), data)
}

export { subscribeDB, getDataBase, setDataBase, pushDataBase, updateDataBase }
