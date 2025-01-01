<template>
<header class="bg-gray-700 p-4" style="padding-left: 3vw;">
    <nav>
        <ul class="flex space-x-4" style="align-items: center;">
            <li :class="{ 'active': $route.path === config.title }" v-for="config in create_configs" style="margin-left: 2vw;">
                <router-link :to="config.index">{{ config.title }}</router-link>
            </li>
        </ul>
    </nav>
</header>
</template>

<script>
export default {
    data() {
        return {
            create_configs: [{
                    "index": "/txt2imgpro",
                    "title": "文生图-专业"
                },
                {
                    "index": "/img2imgpro",
                    "title": "图生图-专业"
                },
                {
                    "index": "/txt2img",
                    "title": "文生图-入门"
                },
                {
                    "index": "/img2img",
                    "title": "图生图-入门"
                },
                {
                    "index": "/avatar",
                    "title": "动漫头像"
                },
                {
                    "index": "/bg",
                    "title": "动漫背景替换"
                },
            ],
            images: [],
            itemsPerPage: 8,
            currentPage: 1
        };
    },
    computed: {
        totalPages() {
            return Math.ceil(this.images.length / this.itemsPerPage);
        },
        currentPageImages() {
            const start = (this.currentPage - 1) * this.itemsPerPage;
            const end = start + this.itemsPerPage;
            return this.images.slice(start, end);
        }
    },
    methods: {
        prevPage() {
            if (this.currentPage > 1) {
                this.currentPage--;
            }
        },
        nextPage() {
            if (this.currentPage < this.totalPages) {
                this.currentPage++;
            }
        },
        goToPage(page) {
            if (page >= 1 && page <= this.totalPages) {
                this.currentPage = page;
            }
        }
    },
};
</script>

<style scoped>
.active {
    color: rgb(83, 83, 178);
    /* 这里可以设置高亮的样式，比如颜色等，根据实际需求调整 */
}
</style>
