<template>
<header class="bg-gray-700 p-4" style="padding-left: 4.5vw;">
    <nav>
        <ul class="flex space-x-4" style="align-items: center;">
            <el-button ref="ref1" link :class="{ 'active_2': $route.query.type === 'txt2imgpro' }" type="primary">
                <router-link to="/history?type=txt2imgpro">文生图-专业</router-link>
            </el-button>
            <el-button ref="ref2" link :class="{ 'active_2': $route.query.type === 'img2imgpro' }" type="primary">
                <router-link to="/history?type=img2imgpro">图生图-专业</router-link>
            </el-button>
            <el-button ref="ref3" link :class="{ 'active_2': $route.query.type === 'txt2img' }" type="primary">
                <router-link to="/history?type=txt2img">文生图-入门</router-link>
            </el-button>
            <el-button ref="ref4" link :class="{ 'active_2': $route.query.type === 'img2img' }" type="primary">
                <router-link to="/history?type=img2img">图生图-入门</router-link>
            </el-button>
            <el-button ref="ref5" link :class="{ 'active_2': $route.query.type === 'avatar' }" type="primary">
                <router-link to="/history?type=avatar">动漫头像</router-link>
            </el-button>
            <el-button ref="ref6" link :class="{ 'active_2': $route.query.type === 'bg' }" type="primary">
                <router-link to="/history?type=bg">动漫背景替换</router-link>
            </el-button>
        </ul>
    </nav>
</header>
<main class="container mx-auto p-8" style="margin-top: 2vh; min-height: 80vh">
    <div v-if="$route.query.type != null">
        <div class="grid grid-cols-4 gap-4">
            <div v-for="img in currentPageImages" :key="img.id" class="bg-gray-700 h-64">
              <HistoryBox :query="img.query"></HistoryBox>
            </div>
        </div>

        <div class="mt-4 flex justify-center space-x-2">
            <button @click="prevPage" :disabled="currentPage === 1" style="cursor: pointer;">上一页</button>
            <button v-for="page in totalPages" :key="page" @click="goToPage(page)" :class="{ 'active': currentPage === page }">
                {{ page }}
            </button>
            <button @click="nextPage" :disabled="currentPage === totalPages" style="cursor: pointer;">下一页</button>
        </div>
    </div>
    <div v-else>
      history
    </div>

</main>
</template>

<script setup>
import { ref, computed, onMounted, watchEffect, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { fetch } from '../service/fetch.js';
import HistoryBox from './HistoryBox.vue'


const router = useRouter();
const route = useRoute();

// 定义响应式数据
const images = ref([])
const itemsPerPage = ref(8);
const currentPage = ref(1);

// 计算属性
const totalPages = computed(() => Math.ceil(images.value.length / itemsPerPage.value));
const currentPageImages = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage.value;
    const end = start + itemsPerPage.value;
    return images.value.slice(start, end);
});

onMounted(() => {
  get_all_his()
})

const get_all_his = () => {
  var promise = fetch("/history/all", "POST");
  promise.then(resp => {
    if (resp.status == 200) {
      const res = resp.data.result
      var queryDict = {}
      const titleList = ["txt2imgpro", "txt2img", "img2imgpro", "img2img", "avatar", "bg"]
      titleList.forEach(title => {
        queryDict[title] = []
      })

      for (let i = 0; i < res.length; i++) {
        const type = res[i].type
        queryDict[type].push({"id": i, "query": res[i]})
      }
      images.value = queryDict[route.query.type]
    }
  })

}

watch(
  () => route.query.type,
  (newVal, oldVal) => {
      if (newVal != null) {
        get_all_his()
    }
  }
);



// 方法定义
const prevPage = () => {
    if (currentPage.value > 1) {
        currentPage.value--;
    }
};

const nextPage = () => {
    if (currentPage.value < totalPages.value) {
        currentPage.value++;
    }
};

const goToPage = (page) => {
    if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page;
    }
};



// 原代码中相关变量未在提供部分完整定义（如isLoggedIn等），这里假设后续补充完整对应逻辑
// 示例的点击事件等方法（如logout等），需要补充具体实现逻辑，以下只是保持结构占位
const showLoginDialog = ref(false);
const showAvatarDropdown = ref(false);
const isLoggedIn = ref(false);
const logout = () => {
    // 补充具体的登出逻辑，比如清除token、跳转到登录页等
};
</script>

<style scoped>
.active {
    color: rgb(83, 83, 178);
    /* 这里可以设置高亮的样式，比如颜色等，根据实际需求调整 */
    font-weight: bold;
}

.active_2 {
    color: rgb(90, 222, 255);
}
</style>
