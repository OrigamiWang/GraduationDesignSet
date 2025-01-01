<template>
    <div class="full">
        <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
            <el-menu-item v-for="menu in menu_configs" :index="menu.index">{{menu.title}}</el-menu-item>
        </el-menu>
        <keep-alive> 
            <router-view></router-view>
        </keep-alive>
    </div>
</template>

<script>

export default {
    mounted() {
    },
    data() {
        return {
            activeIndex: '/create',
            form: {},
            model_options: [],
            model_base_map: {},
            lora_options: [],
            prompt: '',
            negative_prompt: '',
            menu_configs: [
                {   "index": "/create/txt2imgpro",
                    "title": "文生图-专业"},
                {   "index": "/create/img2imgpro",
                    "title": "图生图-专业"},
                {   "index": "/create/txt2img",
                    "title": "文生图-入门"},
                {   "index": "/create/img2img",
                    "title": "图生图-入门"},
                {   "index": "/create/avatar",
                    "title": "动漫头像"},
                {   "index": "/create/bg",
                    "title": "动漫背景替换"},
            ]
        }
    },
    watch: {
        $route() {
            this.setCurrentRoute();
        },
    },

    created() {
        this.setCurrentRoute();
    },
    methods: {
        setCurrentRoute() {
            this.activeIndex = this.$route.path; // 通过他就可以监听到当前路由状态并激活当前菜单
        },
        handleSelect(key, keyPath) {
            // console.log(key, keyPath);
            this.$router.push(key)
            // // 根据选择的菜单项改变路由
            // if (key === '1') {
            //     this.$router.push('/guide/txt2imgpro');
            // } else if (key === '2') {
            //     this.$router.push('/guide/img2imgpro');
            // } else if (key === '3') {
            //     this.$router.push('/guide/txt2img');
            // } else if (key === '4') {
            //     this.$router.push('/guide/img2img');
            // } else if (key === '5') {
            //     this.$router.push('/guide/avatar');
            // } else if (key === '6') {
            //     this.$router.push('/guide/bg');
            // } 
        },
    },
}
</script>

<style></style>
