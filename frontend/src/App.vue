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
  <main class="app-shell">
    <header class="page-header">
      <div>
        <p class="eyebrow">DataINC</p>
        <h1>CSV Processing Dashboard</h1>
        <p class="subtitle">
          Seguimiento de órdenes, procesamiento asíncrono y descarga de archivos normalizados.
        </p>
      </div>
    </header>

    <div class="page-grid">
      <UploadSection @uploaded="handleUploaded" />
      <OrdersTable ref="ordersTable" />
    </div>
  </main>
</template>