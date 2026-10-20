<script setup>
import axios from "axios";
import {onBeforeMount, ref} from "vue";
import Cookies from 'js-cookie';

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

const projects = ref([]);

async function fetchProjects() {
  const r = await axios.get("/api/projects/");
  console.log(r.data)
  projects.value = r.data;
}

async function onLoadClick() {
  await fetchProjects()
}

onBeforeMount(async () => {
  await fetchProjects()
})

</script>

<template>
  <div v-for="item in projects">
      {{ item.title }}
  </div>
  <button @click="onLoadClick()">Загрузить</button>




</template>

<style scoped>

</style>
