<template>
  <div class="menu-item-container" @click="clickItem">
    <div class="menu-item-image-wrap">
      <img
        
        :src="props.item.image"
        :alt="props.item.name"
        class="menu-item-image"
      />
    </div>
    <div class="menu-item-name-wrap">
      <p class="menu-item-name-text">
        {{ props.item.name }}
      </p>
    </div>
    <div class="menu-item-description-wrap">
      <p class="menu-item-description-text">
        {{ props.item.description }}
      </p>
    </div>
    <div class="menu-item-price-wrap">
      <p class="menu-item-price-text">
        {{ getPriceText(props.item.price) }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { MenuItemType } from '@/types/menuDataType'
import palette from '@/styles/colors'
import useMenuStore from '@/store/storeMenuData';
import useModalStore from '@/store/storeModal';

const props = defineProps<{
  item: MenuItemType
}>();

const { setOrderItemInfo } = useMenuStore()
const { openCloseModal } = useModalStore()

const { gray01 } = palette

const clickItem = () => {
  setOrderItemInfo(props.item)
  openCloseModal()
}

const getPriceText = (price: number) => {
  return `${price.toLocaleString()}원`
}
</script>

<style scoped lang="scss">
.menu-item-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  cursor: pointer;

  .menu-item-image-wrap {
    width: 100%;
    height: 300px;
    display: flex;
    justify-content: center;
    align-items: center;

    .menu-item-image {
      width: 100%;
      height: 100%;
      object-fit: fill;
    }
  }

  .menu-item-name-wrap {
    width: 100%;
    display: flex;
    align-items: center;
    padding: 0px 30px;
    box-sizing: border-box;

    .menu-item-name-text {
      font-size: 24px;
      color: #fff;
    }
  }

  .menu-item-description-wrap {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 0px 30px;
    box-sizing: border-box;

    .menu-item-description-text {
      font-size: 16px;
      color: v-bind(gray01);
    }
  }

  .menu-item-price-wrap {
    width: 100%;
    display: flex;
    align-items: center;
    padding: 0px 30px;
    box-sizing: border-box;

    .menu-item-price-text {
      font-size: 22px;
      color: #fff;
    }
  }
}
</style>