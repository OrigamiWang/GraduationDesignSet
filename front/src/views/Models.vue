<template>
<main class="container mx-auto p-8 full">
    <div class="grid grid-cols-4 gap-4">
        <div v-for="img in currentPageImages" :key="img.id" class="bg-gray-700 h-64">
            <!-- 这里可以根据实际情况添加图片展示的具体内容，比如img标签等 -->
            <ImgBox :url="img.url" :title="img.title"></ImgBox>
        </div>
    </div>
    <div class="mt-4 flex justify-center space-x-2">
        <button @click="prevPage" :disabled="currentPage === 1" style="cursor: pointer;">上一页</button>
        <button v-for="page in totalPages" :key="page" @click="goToPage(page)" :class="{ 'active': currentPage === page }">
            {{ page }}
        </button>
        <button @click="nextPage" :disabled="currentPage === totalPages" style="cursor: pointer;">下一页</button>
    </div>
</main>
</template>

<script setup>
import { ref, computed, onMounted} from 'vue';
import { fetch } from '../service/fetch.js';
import ImgBox from './ImgBox.vue';

const images = ref([
]);
const itemsPerPage = ref(8);
const currentPage = ref(1);

onMounted(() => {
    get_model_imgs_list();
});

// 计算属性
const totalPages = computed(() => {
    return Math.ceil(images.value.length / itemsPerPage.value);
});
const currentPageImages = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage.value;
    const end = start + itemsPerPage.value;
    return images.value.slice(start, end);
});

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

const get_model_imgs_list = () => {
    const reqBody = {
      "buk": "stable-diffusion",
      "path": "models"
    }
    var promise = fetch("/sd/get_model_img_list", "POST", reqBody);
    promise.then(resp => {
        if (resp.status == 200) {
            var imgs_list = resp.data.result;
            for(var i = 0; i < imgs_list.length; i++) {
                var url = imgs_list[i]
                var title = url.substring(0, url.indexOf("?"))
                title = title.substring(title.lastIndexOf("/") + 1, title.lastIndexOf("."))
                images.value.push({"id": i, "url": url, "title": title})
            }

        }
    });
};

</script>

<style scoped>
.active {
    color: rgb(83, 83, 178);
    /* 这里可以设置高亮的样式，比如颜色等，根据实际需求调整 */
    font-weight: bold;
}
</style>
