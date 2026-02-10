<template>
  <div class="order-details-container">
    <div class="order-details-title">
      주문 내역
    </div>
    <div class="order-details-body">
      <el-table :data="pagedList" border style="width: 100%">
        <el-table-column type="index" sortable width="50" />
        <el-table-column prop="category" sortable label="종류" />
        <el-table-column prop="name" sortable label="상품명" />
        <el-table-column prop="price" sortable label="상품 가격" />
        <el-table-column prop="time" sortable label="주문 시간" />
      </el-table>
      <div class="order-detail-pagination">
        <el-pagination
        v-model:current-page="currentPage"
        background
        :page-size="pageSize"
        :pager-count="11"
        layout="prev, pager, next"
        :total="orderDetailsList.length"
      />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import useOrderDetail from '@/store/storeOrderDetails'
import { storeToRefs } from 'pinia';
import { computed, ref } from 'vue';

const { orderDetailsList } = storeToRefs(useOrderDetail())
const currentPage = ref(1)
const pageSize = ref(10)

const pagedList = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return orderDetailsList.value.slice(start, end)
})

</script>

<style scoped lang="scss">
.order-details-container {
  padding: 30px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 50px;
  flex: 1;

  .order-details-title {
    font-size: 28px;
    font-family: 'NanumGothicEcoBold', sans-serif;
  }

  .order-details-body {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;

    .order-detail-pagination {
      width: 100%;
      display: flex;
      justify-content: center;
      margin-bottom: 30px;
    }
  }
}
</style>