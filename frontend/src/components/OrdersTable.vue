<script setup lang="ts">
import { onMounted, onUnmounted, ref } from "vue";
import { getOrders, type Order } from "../api/orders";

const orders = ref<Order[]>([]);
const isLoading = ref(false);

let intervalId: number | undefined;

const activeStatuses = ["CREATED", "VERIFYING", "NORMALIZING"];

const hasActiveOrders = () =>
  orders.value.some((order) => activeStatuses.includes(order.status));

const stopPolling = () => {
  if (intervalId) {
    clearInterval(intervalId);
    intervalId = undefined;
  }
};

const loadOrders = async () => {
  isLoading.value = true;

  try {
    orders.value = await getOrders();

    if (!hasActiveOrders()) {
      stopPolling();
    }
  } finally {
    isLoading.value = false;
  }
};

const startPolling = () => {
  if (intervalId) return;
  intervalId = window.setInterval(loadOrders, 2000);
};

const refreshOrders = async () => {
  await loadOrders();

  if (hasActiveOrders()) {
    startPolling();
  }
};

defineExpose({
  refreshOrders,
});

const formatDateTime = (value: string) =>
  new Date(value).toLocaleString();

const formatDuration = (value: number | null) => {
  if (value === null) return "—";
  return `${value.toFixed(2)}s`;
};

const getStatusClass = (status: string) => {
  return `status status-${status.toLowerCase()}`;
};

onMounted(refreshOrders);
onUnmounted(stopPolling);
</script>

<template>
  <section class="orders-section">
    <div class="section-header">
      <div>
        <h2>Orders Dashboard</h2>
        <p>Historial cronológico de órdenes y timeline de procesamiento.</p>
      </div>

      <button @click="refreshOrders" :disabled="isLoading">
        {{ isLoading ? "Actualizando..." : "Actualizar" }}
      </button>
    </div>

    <div class="orders-list">
      <article
        v-for="order in orders"
        :key="order.id"
        class="order-card"
      >
        <div class="order-main">
          <div>
            <span class="order-id">Order #{{ order.id }}</span>
            <span :class="getStatusClass(order.status)">
              {{ order.status }}
            </span>
          </div>

          <a
            v-if="order.download_url"
            :href="order.download_url"
            target="_blank"
            class="download-link"
          >
            Descargar CSV
          </a>

          <span v-else class="muted">Archivo no disponible</span>
        </div>

        <div class="order-metrics">
          <div>
            <span>Creado</span>
            <strong>{{ formatDateTime(order.created_at) }}</strong>
          </div>

          <div>
            <span>Registros</span>
            <strong>{{ order.records_processed }}</strong>
          </div>

          <div>
            <span>Duración total</span>
            <strong>{{ formatDuration(order.processing_duration_seconds) }}</strong>
          </div>
        </div>

        <div class="timeline">
          <h3>Timeline de procesamiento</h3>

          <div
            v-for="history in order.status_history"
            :key="`${order.id}-${history.status}-${history.timestamp}`"
            class="timeline-item"
          >
            <div class="timeline-dot"></div>

            <div class="timeline-content">
              <span :class="getStatusClass(history.status)">
                {{ history.status }}
              </span>

              <p>{{ formatDateTime(history.timestamp) }}</p>
            </div>

            <span class="timeline-duration">
              {{ formatDuration(history.duration_from_previous_seconds) }}
            </span>
          </div>
        </div>

        <p v-if="order.error_message" class="error-message">
          {{ order.error_message }}
        </p>
      </article>
    </div>
  </section>
</template>