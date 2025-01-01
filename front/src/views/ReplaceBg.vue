<template>
<header class="bg-gray-700 p-4" style="padding-left: 3vw;">
    <nav>
        <ul class="flex space-x-4" style="align-items: center;">
            <li :class="{ 'active': $route.path === config.index }" v-for="config in create_configs" style="margin-left: 2vw;">
                <router-link :to="config.index">{{ config.title }}</router-link>
            </li>
        </ul>
    </nav>
</header>
<div class="full">
    <h1 class="center">动漫背景替换</h1>
    <div class="around column">
        <div id="form">
            <el-form ref="form" :model="form">
                <el-form-item label="原始动漫图片">
                    <el-upload class="upload-demo" :action="upload_img()" :on-success="handleSrcImgSuccess" :on-preview="handlePreview" :on-remove="handleRemove" :file-list="src_img_file_list" list-type="picture">
                        <el-button size="small" type="primary">点击上传</el-button>
                    </el-upload>
                </el-form-item>
                <el-form-item label="动漫背景">
                    <el-upload class="upload-demo" :action="upload_img()" :on-success="handleBgImgSuccess" :on-preview="handlePreview" :on-remove="handleRemove" :file-list="bg_img_file_list" list-type="picture">
                        <el-button size="small" type="primary">点击上传</el-button>
                    </el-upload>
                </el-form-item>
                <el-form-item>
                    <el-button @click="generate_img">生成图片</el-button>
                </el-form-item>
            </el-form>
        </div>

        <div id="res_img">
            <el-image style="width: 40vw; height: 40vh" :src="res_b64" :fit="fit">
            </el-image>
        </div>
    </div>
</div>
</template>

<script>
import { fetch, fetch_form_data } from '../service/fetch.js'
import axios from 'axios'

export default {
    mounted() {},
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
            fit: "cover",
            alt_str: "未运行",
            src_img_file_list: [],
            bg_img_file_list: [],
            form: {},

            img: {
                height: '100vh',
                width: '10vw',
            },
            // res_b64: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg', 
            res_b64: '',
        }
    },
    methods: {
        handleSrcImgSuccess(file) {
            // 弹框：上传成功    
            this.$message.success("上传成功!");
            this.src_img_file_list.push({ "filename": file.result.filename, "base64_str": file.result.base64_str })
        },
        handleBgImgSuccess(file) {
            // 弹框：上传成功
            this.$message.success("上传成功!");
            this.bg_img_file_list.push({ "filename": file.result.filename, "base64_str": file.result.base64_str })
        },
        handleRemove(file, fileList) {
            console.log("remove file...");
        },
        handlePreview(file) {
            console.log("preview file...");
        },
        upload_img() {
            return 'http://localhost:5173/api/file/upload';
        },
        generate_img() {
            if (this.src_img_file_list.length == 0 || this.bg_img_file_list.length == 0) {
                this.$message.warning("请先上传图片!");
                return
            } else if (this.src_img_file_list.length > 1 || this.bg_img_file_list.length > 1) {
                this.$message.warning("只能上传一张图片!");
                return
            }
            var reqBody = {
                "src_img": this.src_img_file_list[0]['base64_str'],
                "bg_img": this.bg_img_file_list[0]['base64_str'],
            }
            var promise = fetch("/bg/replace", "POST", reqBody)
            promise.then(resp => {
                if (resp.status == 200) {
                    var b64Img = "data:image/jpeg;base64," + resp.data.result;
                    // const jsonArray = JSON.parse(jsonString);
                    this.res_b64 = b64Img;

                }
            })

        },
    },
}
</script>

<style></style>
