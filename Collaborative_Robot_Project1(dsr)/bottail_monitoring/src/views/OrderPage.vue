<template>
  <OrderModal v-show="modalState" />
  <div class="order-container">
    <MenuBar />
    <MenuItemList />
  </div>
</template>

<script setup lang="ts">
import MenuBar from '@/containers/MenuBar.vue';
import MenuItemList from '@/containers/MenuItemList.vue';
import OrderModal from '../components/OrderModal.vue';
import useMenuStore from '../store/storeMenuData';
import { storeToRefs } from 'pinia';
import palette from '../styles/colors'

const { modalState } = storeToRefs(useMenuStore())
const { black01 } = palette

</script>

<style scoped lang="scss">
.order-container {
  display: flex;
  width: 100vw;
  height: 100vh;
  background-color: v-bind(black01);
}
</style>