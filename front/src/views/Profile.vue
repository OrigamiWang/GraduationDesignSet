<template>
  <main class="container mx-auto p-8">
    <div class="grid grid-cols-4 gap-4">
      <div v-for="img in currentPageImages" :key="img.id" class="bg-gray-700 h-64">
      </div>
    </div>
    <div class="mt-4 flex justify-center space-x-2">
      <button @click="prevPage" :disabled="currentPage === 1">上一页</button>
      <button v-for="page in totalPages" :key="page" @click="goToPage(page)" :class="{ 'active': currentPage === page }">
        {{ page }}
      </button>
      <button @click="nextPage" :disabled="currentPage === totalPages">下一页</button>
    </div>
  </main>
</template>

<script>

const routes = [
  { path: '/', component: { template: '<div>Home Page</div>' } },
  { path: '/models', component: { template: '<div>Models Page</div>' } },
  { path: '/images', component: { template: '<div>Images Page</div>' } },
  { path: '/guide', component: { template: '<div>Create Guide Page</div>' } },
];


export default {
  data() {
    return {
      images: [
        { id: 1, url: 'https://example.com/img1.jpg' },
        { id: 2, url: 'https://example.com/img2.jpg' },
      ],
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
  color: rgb(83, 83, 178); /* 这里可以设置高亮的样式，比如颜色等，根据实际需求调整 */
  font-weight: bold;
}
</style>