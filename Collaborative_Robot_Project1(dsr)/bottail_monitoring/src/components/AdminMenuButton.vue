<template>
  <div
    class="admin-menu-button"
    :class="{'selected': isSelectedMenu()}"
  >
    <div class="admin-menu-text">
      {{ props.data.title }}
    </div>
  </div>
</template>

<script setup lang="ts">
import useMenuStore from '../store/storeMenuData'
import { storeToRefs } from 'pinia';
import type { AdminMenuType } from '@/types/menuDataType'

const { adminMenuState } = storeToRefs(useMenuStore())

const props = defineProps<{
  data: AdminMenuType
}>();

const isSelectedMenu = () => {
  if(adminMenuState.value === props.data.category) {
    return true;
  }
  return false
}


</script>

<style scoped lang="css">
.admin-menu-button {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 45px;
  padding: 15px 20px;

  .admin-menu-text {
    color: #fff;
    font-size: 22px;
  }

  &.selected {
    background-color: #999;
  }
}
</style>