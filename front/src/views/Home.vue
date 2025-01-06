<template>
<header class="bg-gray-700 p-4" style="padding-left: 4.5vw;">
    <nav>
        <ul class="flex space-x-4" style="align-items: center;">
            <el-button ref="ref1" link :class="{ 'active_2': $route.path === '/txt2imgpro' }" type="primary">
                <router-link to="/txt2imgpro">文生图-专业</router-link>
            </el-button>
            <el-button ref="ref2" link :class="{ 'active_2': $route.path === '/img2imgpro' }" type="primary">
                <router-link to="/img2imgpro">图生图-专业</router-link>
            </el-button>
            <el-button ref="ref3" link :class="{ 'active_2': $route.path === '/txt2img' }" type="primary">
                <router-link to="/txt2img">文生图-入门</router-link>
            </el-button>
            <el-button ref="ref4" link :class="{ 'active_2': $route.path === '/img2img' }" type="primary">
                <router-link to="/img2img">图生图-入门</router-link>
            </el-button>
            <el-button ref="ref5" link :class="{ 'active_2': $route.path === '/avatar' }" type="primary">
                <router-link to="/avatar">动漫头像</router-link>
            </el-button>
            <el-button ref="ref6" link :class="{ 'active_2': $route.path === '/bg' }" type="primary">
                <router-link to="/bg">动漫背景替换</router-link>
            </el-button>
        </ul>
    </nav>
</header>
<main class="container mx-auto p-8 full">
    <el-button type="primary" plain @click="open_tour = true">开启二次元生成之旅吧~</el-button>

    <el-divider />

    <el-tour v-model="open_tour">
        <el-tour-step :target="ref1?.$el" title="文生图-专业">
            <div>面向
                <el-text tag="mark">专业</el-text>
                用户，输入
                <el-text tag="b">文字</el-text>
                生成
                <el-text tag="b">图片</el-text>
                ，需要手动设置参数
            </div>
        </el-tour-step>
        <el-tour-step :target="ref2?.$el" title="图生图-专业">
            <div>面向
                <el-text tag="mark">专业</el-text>
                用户，输入
                <el-text tag="b">图片</el-text>
                生成
                <el-text tag="b">图片</el-text>
                ，需要手动设置参数
            </div>
        </el-tour-step>
        <el-tour-step :target="ref3?.$el" title="文生图-入门">
            <div>面向
                <el-text tag="mark">小白</el-text>
                用户，输入
                <el-text tag="b">文字</el-text>
                生成
                <el-text tag="b">图片</el-text>
                ，无需自己设置参数
            </div>
        </el-tour-step>
        <el-tour-step :target="ref4?.$el" title="图生图-入门">
            <div>面向
                <el-text tag="mark">小白</el-text>
                用户，输入
                <el-text tag="b">图片</el-text>
                生成
                <el-text tag="b">图片</el-text>
                ，无需自己设置参数
            </div>
        </el-tour-step>
        <el-tour-step :target="ref5?.$el" title="动漫头像">
            <div>上传自己的一张
                <el-text tag="b">单人照</el-text>
                ，生成专属于你的
                <el-text tag="mark">二次元形象</el-text>
            </div>
        </el-tour-step>
        <el-tour-step :target="ref6?.$el" title="动漫背景替换">
            <div>上传一张
                <el-text tag="b">背景图</el-text>
                和
                <el-text tag="b">动漫图</el-text>
                ，
                <el-text tag="mark">自动替换</el-text>
                动漫图的背景
            </div>
        </el-tour-step>
    </el-tour>
</main>
</template>

<script lang="ts">
import { ref } from 'vue';
import { MoreFilled } from '@element-plus/icons-vue'
import type { ButtonInstance } from 'element-plus'

const ref1 = ref < ButtonInstance > ()
const ref2 = ref < ButtonInstance > ()
const ref3 = ref < ButtonInstance > ()
const ref4 = ref < ButtonInstance > ()
const ref5 = ref < ButtonInstance > ()
const ref6 = ref < ButtonInstance > ()

const open_tour = ref(false)

export default {
    setup() {
        return {
            MoreFilled,
            open_tour,
            ref1,
            ref2,
            ref3,
            ref4,
            ref5,
            ref6
        };
    }
}
</script>

<style scoped>
.active {
    color: rgb(83, 83, 178);
}
</style>
