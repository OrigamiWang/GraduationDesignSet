<template>
<main class="container mx-auto p-8" style="min-height: 90vh">
    <el-descriptions border>
        <el-descriptions-item :rowspan="2" :width="140" label="Photo" align="center">
            <img src="../assets/avatar/male.jpg">
        </el-descriptions-item>
        <el-descriptions-item label="Uid">{{ id }}</el-descriptions-item>
        <el-descriptions-item label="Username">{{ user_name }}</el-descriptions-item>
        <el-descriptions-item label="Password">{{ pswd }}</el-descriptions-item>
        <el-descriptions-item label="Place">Shenzhen</el-descriptions-item>
        <el-descriptions-item label="Remarks">
            <el-tag size="small">School</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="Address">
          3688 Nanhai Avenue, Nanshan District, Shenzhen, Guangdong, China, 518060.
        </el-descriptions-item>
    </el-descriptions>
</main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
const id = ref(0)
const user_name = ref("")
const pswd = ref("")

onMounted(() => {
    getUserProfile()
})

const getUserProfile = () => {
    const uid = localStorage.getItem("uid")
    const username = localStorage.getItem("username")
    const password = localStorage.getItem("password")
    id.value = uid
    user_name.value = username
    pswd.value = password

}
</script>

<style scoped>
</style>
