<template>
  <div class="admin-menu-container">
    <div class="admin-menu-title">
      관리자 모드
    </div>
    <div class="admin-menu-list-container">
      <div>
        <AdminMenuButton
          v-for="menu in menuList"
          :key="menu.category"
          :data="menu"
          @click="clickAdminMenu(menu.category)"
        />
      </div>
      <div class="admin-menu-back-button" @click="goBackOrderPage">
        되돌아가기
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import palette from '@/styles/colors';
import AdminMenuButton from '@/components/AdminMenuButton.vue';
import type { AdminMenuType } from '@/types/menuDataType';
import useMenuStore from '@/store/storeMenuData';
import router from '@/router';
import { ElMessageBox } from 'element-plus'

const { black01 } = palette
const { setAdminMenuState } = useMenuStore()
const menuList: AdminMenuType[] = [
  {
    title: '주문내역',
    category: 'orderDetails'
  },
  {
    title: '통계',
    category: 'statistics'
  },
  {
    title: '로봇관리',
    category: 'setting'
  },
]

const clickAdminMenu = (category: string) => {
  setAdminMenuState(category)
}

const goBackOrderPage = () => {
  ElMessageBox.confirm(
    '주문페이지로 돌아가시겠습니까?',
    '돌아가기',
    {
      confirmButtonText: '확인',
      cancelButtonText: '취소',
      type: 'warning',
    }
  )
    .then(() => {
      router.push({name: 'order'})
    })
}

</script>
<style scoped lang="scss">
.admin-menu-container {
  display: flex;
  flex-direction: column;
  background-color: v-bind(black01);
  width: 240px;

  .admin-menu-title {
    padding: 50px 30px;
    font-size: 32px;
    font-family: 'NanumGothicEcoBold', sans-serif;
    color: #fff;
    text-align: center;
  }

  .admin-menu-list-container {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .admin-menu-back-button {
    font-size: 22px;
    color: #fff;
    padding: 20px 10px;
    text-align: center;
    background-color: #6639CE;
  }
}

</style>