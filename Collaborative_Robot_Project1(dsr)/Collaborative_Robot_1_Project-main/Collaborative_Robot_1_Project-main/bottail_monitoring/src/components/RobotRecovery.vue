<template>
  <el-card>
    <div class="robot-recovery-container">
      <div class="robot-recovery-body">
        <div class="robot-recovery-body-title">로봇 정지</div>
        <span>로봇을 일시 정지합니다.</span>
        <el-button
          type="danger"
          size="large"
          :icon="VideoPause"
          @click="clickButton('pause')"
        >
          정지하기
        </el-button>
      </div>
      <div class="robot-recovery-body">
        <div class="robot-recovery-body-title">로봇 재개</div>
        <span>일시 정지 중인 로봇의 작업을 재개합니다.</span>
        <el-button
          type="success"
          size="large"
          :icon="VideoPlay"
          @click="clickButton('resume')"
        >
          재개하기
      </el-button>
      </div>
      <div class="robot-recovery-body">
        <div class="robot-recovery-body-title">로봇 복구</div>
        <span>로봇 동작 오류 발생시 복구를 진행합니다.</span>
        <el-button
          type="warning"
          size="large"
          :icon="RefreshRight"
          @click="clickButton('recover')"
        >
          복구하기
        </el-button>
      </div>
      <div class="robot-recovery-body">
        <div class="robot-recovery-body-title">로봇 홈위치</div>
        <span>첫 시작위치로 복귀시킵니다.</span>
        <el-button
          size="large"
          :icon="Sort"
          @click="movej([0, 0, 90, 0, 90, 0], 60, 60)"
        >
          홈 위치 이동
        </el-button>
      </div>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { VideoPause, VideoPlay, RefreshRight, Sort } from '@element-plus/icons-vue'
import palette from '@/styles/colors';
import { publishTopic, movej } from '@/composable/useRobot'
import { ElMessage, ElMessageBox } from 'element-plus';

const { gray01 } = palette

const clickButton = (type :string) => {
  ElMessageBox.confirm(
    '진행하시겠습니까??',
    '경고',
    {
      confirmButtonText: '확인',
      cancelButtonText: '취소',
      type: 'warning',
    }
  )
    .then(() => {
      publishTopic(type)
    })
}

</script>

<style scoped lang="scss">
.robot-recovery-container {
  display: flex;
  flex-direction: column;
  gap: 30px;
  padding: 10px;

  .robot-recovery-body {
    display: flex;
    flex-direction: column;
    gap: 5px;

    .robot-recovery-body-title {
      font-size: 24px;
      font-family: 'NanumGothicEcoBold', sans-serif;
    }

    span {
      font-size: 16px;
      color: v-bind(gray01);
      margin-bottom: 10px;
    }

    button {
      width: 200px;
    }
  }
}
</style>