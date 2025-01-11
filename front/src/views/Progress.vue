<template>
<el-dialog :title="props.title" v-model="props.showProgress" style="width: 30vw">
    <el-progress :percentage="100" status="success" :indeterminate="true" :duration="5" />
</el-dialog>
</template>

<script setup>
// import { ElMessage } from 'element-plus';

const props = defineProps(['showProgress', 'title'])

// const handleClose = () => {
//     ElMessage.info("图像正在生成,请等待...")
// }
</script>
