<template>
<div style="height: 100%; width: 100%; position: relative;">
    <span style="position: absolute; top: 12vw; left: 1vw; color: white; z-index: 1; font-size: 1vw; font-weight: bold;">{{ props.title }}</span>
    <el-image style="width: 100%; height: 100%; position: relative; z-index: 0;" :src="props.url" :fit="fit" />
</div>
</template>

<script setup>
import { ref } from 'vue';
const props = defineProps(['url', 'title'])
const fit = ref('contain')

</script>

<style lang="css" scoped>
</style>
