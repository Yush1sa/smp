<script setup>
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

</template>

<style scoped>
</style>