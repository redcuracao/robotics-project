<template>
  <div
    class="menu-button"
    :class="{'selected': isSelectedMenu()}"
  >
    <div class="menu-text">
      {{ props.data.name }}
    </div>
  </div>
</template>

<script setup lang="ts">
import useMenuStore from '../store/storeMenuData'
import { storeToRefs } from 'pinia';
import type { MenuDataType } from '@/types/menuDataType'
import palette from '../styles/colors'

const { menuState } = storeToRefs(useMenuStore())
const { purple02 } = palette

const props = defineProps<{
  data: MenuDataType
}>();

const isSelectedMenu = () => {
  if(menuState.value === props.data.category) {
    return true;
  }
  return false
}


</script>

<style scoped lang="css">
.menu-button {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 45px;
  padding: 15px 20px;
  cursor: pointer;

  .menu-text {
    color: #fff;
    font-size: 28px;
  }

  &.selected {
    background-color: v-bind(purple02);
  }
}
</style>