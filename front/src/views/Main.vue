<template>
<div class="bg-gray-900 text-white">
  <header class="bg-gray-800 p-4">
    <div class="container mx-auto flex justify-between items-center">
      <h1 class="text-2xl font-bold">CIVITAI</h1>
      <nav>
        <ul class="flex space-x-4">
          <li><a href="#" class="hover:underline">Home</a></li>
          <li><a href="#" class="hover:underline">Models</a></li>
          <li><a href="#" class="hover:underline">Images</a></li>
          <li><a href="#" class="hover:underline">Videos</a></li>
          <li><a href="#" class="hover:underline">Posts</a></li>
          <li><a href="#" class="hover:underline">Articles</a></li>
          <li><a href="#" class="hover:underline">Bounties</a></li>
          <li><a href="#" class="hover:underline">Tools</a></li>
          <li><a href="#" class="hover:underline">Challenges</a></li>
          <li><a href="#" class="hover:underline">Events</a></li>
          <li><a href="#" class="hover:underline">Shop</a></li>
          <li><button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Create</button></li>
          <li><button class="bg-gray-600 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded">Sign In</button></li>
        </ul>
      </nav>
    </div>
  </header>

  <main class="container mx-auto p-8">
    <section class="mb-8">
      <h2 class="text-xl font-bold mb-4">Featured Images</h2>
      <p class="text-gray-400 mb-4">All sorts of cool pictures, created by our community, from simple shapes to detailed landscapes or human faces. A virtual canvas where you can unleash your creativity or get inspired.</p>
      <a href="#" class="bg-gray-700 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded">Explore all images</a>
    </section>

    <div class="grid grid-cols-4 gap-4">
      <!-- Image Grid -  Replace with your actual images and links -->
      <div class="bg-gray-700 h-64"></div>
      <div class="bg-gray-700 h-64"></div>
      <div class="bg-gray-700 h-64"></div>
      <div class="bg-gray-700 h-64"></div>
      <div class="bg-gray-700 h-64"></div>
      <div class="bg-gray-700 h-64"></div>
      <div class="bg-gray-700 h-64"></div>
      <div class="bg-gray-700 h-64"></div>
    </div>
  </main>

  <footer class="bg-gray-800 p-4 text-center text-gray-500">
  </footer>
</div>
</template>

<script>

export default {
    methods: {
    },
    mounted() {
    },
}

</script>

<style scoped></style>
