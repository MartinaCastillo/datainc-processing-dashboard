<script setup lang="ts">
import { ref } from "vue";
import UploadSection from "./components/UploadSection.vue";
import OrdersTable from "./components/OrdersTable.vue";

const ordersTable = ref<InstanceType<typeof OrdersTable> | null>(null);

const handleUploaded = () => {
  ordersTable.value?.refreshOrders();
};
</script>

<template>
  <div class="container">
    <h1>DataINC Processing Dashboard</h1>

    <UploadSection @uploaded="handleUploaded" />

    <OrdersTable ref="ordersTable" />
  </div>
</template>