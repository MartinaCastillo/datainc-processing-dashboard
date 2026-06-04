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
    message.value = "Seleccioná un archivo CSV antes de continuar.";
    return;
  }

  try {
    isUploading.value = true;
    await uploadFile(file.value);

    message.value = "Orden creada correctamente.";
    file.value = null;

    if (fileInput.value) {
      fileInput.value.value = "";
    }

    emit("uploaded");
  } catch {
    message.value = "No se pudo subir el archivo. Revisá el formato o intentá nuevamente.";
  } finally {
    isUploading.value = false;
  }
};
</script>

<template>
  <section class="panel upload-panel">
    <div class="panel-header">
      <div>
        <h2>Nueva orden</h2>
        <p>Subí un archivo CSV para iniciar el procesamiento.</p>
      </div>
    </div>

    <div class="upload-box">
      <input
        ref="fileInput"
        type="file"
        accept=".csv"
        @change="onFileChange"
      />

      <div v-if="file" class="selected-file">
        Archivo seleccionado: <strong>{{ file.name }}</strong>
      </div>
    </div>

    <button
      class="primary-button"
      @click="processFile"
      :disabled="isUploading"
    >
      {{ isUploading ? "Creando orden..." : "Procesar archivo" }}
    </button>

    <p v-if="message" class="helper-message">
      {{ message }}
    </p>
  </section>
</template>