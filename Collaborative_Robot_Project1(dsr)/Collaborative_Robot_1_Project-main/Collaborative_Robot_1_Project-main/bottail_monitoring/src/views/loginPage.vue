<template>
  <div class="login-container">
    <h1 class="login-title">
      Admin 페이지
    </h1>
    <div class="login-input-container">
      <el-input
        v-model="loginInfo.id"
        style="width: 360px"
        placeholder="아이디를 입력해주세요."
        size="large"
        />
      <el-input
        v-model="loginInfo.pw"
        placeholder="비밀번호를 입력해주세요."
        style="width: 360px"
        size="large"
        type="password"
        show-password
        @keyup.enter="confirmButton"
        />
    </div>
    <div>
      <el-button type="danger" size="large" @click="cancelButton">
        취소
      </el-button>
      <el-button type="primary" size="large" @click="confirmButton">
        로그인
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import router from '@/router';
import { reactive } from 'vue';
import { ElMessage } from 'element-plus'
import palette from '@/styles/colors';

const loginInfo = reactive({
  id: 'admin',
  pw: ''
})

const { black01 } = palette

const cancelButton = () => {
  router.back()
}

const confirmButton = () => {
  if(loginInfo.id === 'admin' && loginInfo.pw === '1234') {
    ElMessage({
      message: '로그인에 성공하였습니다.',
      type: 'success',
    })
    router.push({name: 'admin'})
  }else {
    ElMessage({
      message: '로그인에 실패하였습니다. 로그인 정보를 확인해주세요.',
      type: 'error',
    })
  }
}
</script>

<style scoped lang="scss">
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  gap: 20px;
  background-color: v-bind(black01);

  .login-title {
    color: #fff;
    font-family: 'NanumGothicEcoBold', sans-serif;
  }

  .login-input-container {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

}
</style>