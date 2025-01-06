<template>
<Progress :showProgress="showProgress"></Progress>
</template>

<script setup>
import { ref } from 'vue';
import Progress from './Progress.vue'

const showProgress = ref(true)

</script>
