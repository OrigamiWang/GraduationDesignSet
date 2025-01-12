<template>
<json-viewer :value="jsonData" copyable boxed sort />
</template>

  
<script setup>

import { ref } from "vue";
import "vue3-json-viewer/dist/index.css";

const jsonData = ref({
    name: "qiu", //字符串
    age: 18, //数组
    isMan: false, //布尔值
    date: new Date(),
    fn: () => {},
    arr: [1, 2, 5]
})
</script>

  
<style></style>
