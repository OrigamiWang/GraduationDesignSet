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
<main class="container mx-auto p-8" style="min-height: 80vh;">
    <el-button type="primary" plain @click="open_tour = true">开启二次元生成之旅吧~</el-button>
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

    <el-divider />

    <div class="image-container">
        <el-popover placement="right" :width="400" trigger="click" v-for="(config, oss_url) in historyDict">
            <template #reference>
                <el-image style="cursor: pointer;" :key="oss_url" :src="oss_url" lazy />
            </template>
            <json-viewer :value="config" copyable boxed sort />
        </el-popover>
    </div>

</main>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import type { ButtonInstance } from 'element-plus'
import { fetch } from '../service/fetch.js'
import "vue3-json-viewer/dist/index.css";

const ref1 = ref < ButtonInstance > ()
const ref2 = ref < ButtonInstance > ()
const ref3 = ref < ButtonInstance > ()
const ref4 = ref < ButtonInstance > ()
const ref5 = ref < ButtonInstance > ()
const ref6 = ref < ButtonInstance > ()
const open_tour = ref(false)
const historyDict = ref({})

onMounted(() => {
    get_other_his()
})

const shuffle = (arr) => {
    arr.sort(() => {
        return Math.random() - 0.5;
    })
    return arr
}

const get_other_his = () => {
    const reqBody = {
        "uid": localStorage.getItem("uid")
    }
    var promise = fetch("/history/other", "POST", reqBody);
    // get path and config
    promise.then(resp => {
        if (resp.status == 200) {
            var res = resp.data.result;

            const shuffledRes = shuffle(res)
            let pathDict = {}
            shuffledRes.forEach(ele => {
                pathDict[ele.path] = ele.config
            })

            // get oss url by path
            for (let path in pathDict) {
                const config = JSON.parse(pathDict[path])
                const reqBody2 = {
                    "path": path
                }
                var promise2 = fetch("/oss/path", "POST", reqBody2);
                promise2.then(resp2 => {
                    if (resp2.status == 200) {
                        if (resp2.data.result.length > 0) {
                            const oss_url = resp2.data.result[0]
                            const srcPath = config["oss_url"]
                            const bgImgPath = config["bg_img_path"]
                            const srcImgPath = config["src_img_path"]

                            if (srcPath != null) {
                                // get oss url by path  
                                const reqBody3 = {
                                    "path": srcPath
                                }
                                var promise3 = fetch("/oss/path", "POST", reqBody3);
                                promise3.then(resp3 => {
                                    if (resp3.status == 200) {
                                        if (resp3.data.result.length > 0) {
                                            const src_oss_url = resp3.data.result[0]
                                            config["oss_url"] = src_oss_url;
                                            historyDict.value[oss_url] = config
                                        }
                                    }
                                })

                            } else if (bgImgPath != null && srcImgPath != null) {
                                const reqBody3 = {
                                    "path": bgImgPath
                                }
                                var promise3 = fetch("/oss/path", "POST", reqBody3);
                                promise3.then(resp3 => {
                                    if (resp3.status == 200) {
                                        if (resp3.data.result.length > 0) {
                                            const src_oss_url = resp3.data.result[0]
                                            config["bg_img_path"] = src_oss_url;
                                            historyDict.value[oss_url] = config
                                        }
                                    }
                                })

                                const reqBody4 = {
                                    "path": srcImgPath
                                }
                                var promise4 = fetch("/oss/path", "POST", reqBody4);
                                promise4.then(resp4 => {
                                    if (resp4.status == 200) {
                                        if (resp4.data.result.length > 0) {
                                            const src_oss_url = resp4.data.result[0]
                                            config["src_img_path"] = src_oss_url;
                                            historyDict.value[oss_url] = config
                                        }
                                    }
                                })

                            } else {
                                historyDict.value[oss_url] = config
                            }
                        }
                    }
                })
            }

        }
    })
}
</script>

<style scoped>
.active {
    color: rgb(83, 83, 178);
}

.image-container {
    columns: 4;
    column-gap: 15px;
    width: 100%;
}

.el-image {
    width: 100%;
    margin-bottom: 15px;
    break-inside: avoid;
}
</style>
