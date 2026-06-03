<script setup lang="ts">
import { ref } from "vue";
import { uploadFile } from "../api/orders";

const emit = defineEmits<{
  uploaded: [];
}>();

const file = ref<File | null>(null);
const message = ref("");
const isUploading = ref(false);
const fileInput = ref<HTMLInputElement | null>(null);

const onFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;

  if (target.files?.length) {
    file.value = target.files[0];
    message.value = "";
  }
};

const processFile = async () => {
  if (!file.value) {
    message.value = "Seleccione un archivo CSV";
    return;
  }

  try {
    isUploading.value = true;

    await uploadFile(file.value);

    message.value = "Archivo enviado correctamente";
    file.value = null;

    if (fileInput.value) {
      fileInput.value.value = "";
    }

    emit("uploaded");
  } catch {
    message.value = "Error al subir archivo";
  } finally {
    isUploading.value = false;
  }
};
</script>

<template>
  <section class="upload-card">
    <div>
      <h2>Upload CSV</h2>
      <p>Subí un archivo para crear una nueva orden de procesamiento.</p>
    </div>

    <div class="upload-actions">
      <input
        ref="fileInput"
        type="file"
        accept=".csv"
        @change="onFileChange"
      />

      <button
        @click="processFile"
        :disabled="isUploading"
      >
        {{ isUploading ? "Procesando..." : "Procesar Archivo" }}
      </button>
    </div>

    <p v-if="message" class="upload-message">
      {{ message }}
    </p>
  </section>
</template>