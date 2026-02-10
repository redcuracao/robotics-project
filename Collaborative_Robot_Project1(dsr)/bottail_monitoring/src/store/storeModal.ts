import { defineStore } from 'pinia'
import { ref } from 'vue'

const useModalStore = defineStore('modal', () => {
  // 모달 오픈 상태
  const modalState = ref(false)

  // 모달 열고 닫기
  const openCloseModal = () => {
    if (modalState.value) {
      modalState.value = false
    } else {
      modalState.value = true
    }
  }

  return {
    modalState,
    openCloseModal,
  }
})

export default useModalStore
