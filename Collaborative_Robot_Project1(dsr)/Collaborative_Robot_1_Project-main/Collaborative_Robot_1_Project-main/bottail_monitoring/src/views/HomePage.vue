<template>
  <div class="home-background">
    <div>
      <img src="../assets/bottail_logo.png" alt="logo-img" class="home-logo-img"/>
    </div>
    <div class="home-order-button" @click="goToOrderPage">
      주문하기
    </div>
  </div>
</template>

<script setup lang="ts">
import router from '@/router';
import palette from '../styles/colors'

const { purple01 } = palette

const goToOrderPage = () => {
  router.push({ name: 'order' });
}

</script>

<style scoped lang="scss">
  .home-background {
    width: 100vw;
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background-image: url('../assets/background.jpg');
    background-size: contain;

    .home-logo-img {
      width: 30vw;
      height: 70vh;
    }

    .home-order-button {
      width: 60vw;
      height: 8vh;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 32px;
      background-color: v-bind(purple01);
      color: #fff;
      text-align: center;
      border: none;
      border-radius: 10px;
      font-family: 'NanumGothicEcoBold', sans-serif;
    }
  }

</style>