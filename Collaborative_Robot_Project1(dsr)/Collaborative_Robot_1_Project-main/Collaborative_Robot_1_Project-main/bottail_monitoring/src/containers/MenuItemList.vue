<template>
  <div class="menu-list-container">
    <div class="menu-list-title">
      {{ getSelectedCategoryName }}
    </div>
    <div class="menu-list">
      <div
        v-for="item, index in filterdData"
        :key="`${item.category}-${index}`"
        >
          <MenuItem :item="item"/>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import useMenuStore from '../store/storeMenuData'
import { storeToRefs } from 'pinia';
import MenuItem from '@/components/MenuItem.vue';

const { menuList} = useMenuStore()
const { menuState } = storeToRefs(useMenuStore())

const filterdData = computed(() => {
    return (
      menuList.find(
        (menu) => menu.category === menuState.value
      )?.item ?? []
    )
})

const getSelectedCategoryName = computed(() => {
    return (
      menuList.find(
        (menu) => menu.category === menuState.value
      )?.name ?? ''
    )
})
</script>

<style scoped lang="scss">
.menu-list-container {
  flex: 1;
  height: 100vh;
  display: flex;
  flex-direction: column;

  .menu-list-title {
    margin-top: 1vh;
    padding: 30px;
    font-size: 40px;
    font-family: 'NanumGothicEcoBold', sans-serif;
    color: #fff;
  }

  .menu-list {
      overflow-y: scroll;
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
    }

  .menu-list::-webkit-scrollbar {
    display: none;
  }
}
</style>