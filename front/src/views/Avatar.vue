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
<div>
    <div class="around column">
        <div id="form">
            <el-form ref="form" :model="form">
                <el-form-item label="图片上传">
                    <el-upload class="upload-demo" :before-upload="handle_before_upload" :action="upload_img()" :on-success="handleSuccess" :on-preview="handlePreview" :on-remove="handleRemove" :file-list="fileList" list-type="picture">
                        <el-button size="small" type="primary">点击上传</el-button>
                    </el-upload>
                </el-form-item>
                <el-form-item label="图片风格">
                    <el-select v-model="form.style_name" placeholder="请选择" style="width: 25vw;">
                        <el-option v-for="item in style_options" :key="item.value" :label="item.label" :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="图片质量">
                    <el-select v-model="form.steps" placeholder="请选择" style="width: 25vw;">
                        <el-option v-for="item in steps_options" :key="item.value" :label="item.label" :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="图片数量">
                    <el-slider :max=5 style="width:25vw;" v-model="batch_cnt" show-input>
                    </el-slider>
                </el-form-item>
                <el-form-item label="seed">
                    <el-checkbox @click="keep_random_seed" v-model="is_keep_random_seed">保持随机</el-checkbox>
                </el-form-item>
                <el-form-item>
                    <el-button @click="generate_img">生成图片</el-button>
                </el-form-item>
            </el-form>
        </div>
        <!-- <div id="imgs" style="height: 100vh; width: 10vw" > -->
        <div id="imgs" :style="{width: img.width, height: img.height}">
            <el-carousel :interval="5000" arrow="always" style="width: 100%; height: 100%;">
                <el-carousel-item v-for="(img, index) in imgs" :key="index">
                    <img :src="img" style="width: 100%; height: 100%; object-fit: cover;" />
                </el-carousel-item>
            </el-carousel>
        </div>
    </div>
</div>
</template>

<script>
import { fetch, fetch_form_data } from '../service/fetch.js'
import axios from 'axios'

export default {
    mounted() {
        // this.auto_resize_img()
        this.get_style_list()
        this.set_template()
    },
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
            fileList: [],
            steps_options: [{ "label": "粗糙", "value": 10 }, { "label": "中等", "value": 25 }, { "label": "精细", "value": 50 }],
            img: {
                height: '100vh',
                width: '10vw',
            },
            form: {},
            style_options: [],
            style_config: {},
            width: 720,
            height: 1280,
            is_keep_random_seed: false,
            imgs: [],
            batch_cnt: 1,
            seed: -1,
            img_base64_str: '',
            // imgs: ["https://dummyimage.com/1024x2048&text=A"],
        }
    },
    methods: {
        async handle_before_upload(file) {
            const formData = new FormData();
            formData.append('file', file);
            console.log("before upload...");
            var res = null
            await axios.post("http://localhost:5173/api/file/upload/check", formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }).then(response => {
                var data = response.data.result
                if (data.code == -1) {
                    // 弹框上传失败
                    this.$message.error("上传失败: " + data.msg);
                    res = false
                } else {
                    this.$message.success("上传成功");
                    res = true
                }

            }).catch(error => {
                console.log(error);
                res = false
            });
            console.log("res: " + res);
            return res
            // return false
        },
        handleSuccess(file) {
            this.fileList.push({ "filename": file.result.filename, "base64_str": file.result.base64_str })
            this.img_base64_str = file.result.base64_str
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
        get_style_list() {
            var promise = fetch("/sd/get_style_list", "POST", null)
            promise.then(resp => {
                if (resp.status == 200) {
                    var style_list = resp.data.result
                    style_list.forEach(style => {
                        this.style_options.push({
                            value: style.style_config,
                            label: style.name,
                        })
                    })
                }
            })
        },
        auto_resize_img() {
            if (this.imgs.length > 0) {
                const img = new Image();
                img.src = this.imgs[0];
                img.onload = () => {
                    const ratio = img.height / img.width
                    const width = this.img.width.substring(0, this.img.width.length - 2)
                    const height = width * ratio
                    this.img.height = height + "vh"
                }
            }
        },
        set_template() {
            // 设置模板，用于快速填充配置
            var template = {
                "txt2img": true,
                "width": 720,
                "height": 720,
                "style_name": "塔罗牌",
                "style_config": { "vae_id": "orangemixvaeReupload_v10.pt", "model_id": "anything-v4.5.ckpt", "cfg_scale": 7, "sampler_id": "DPM++ 2M Karras", "lora_config": { "AtdanLora.safetensors": 0.6, "AnimeTaroCard.safetensors": 1.0 }, "negative_prompt": "bad fingers" },
                "steps": 10,
            }

            this.form.steps = template.steps
            this.form.style_name = template.style_name
            this.width = template.width
            this.height = template.height
            this.style_config = template.style_config
        },
        generate_img() {
            if (this.fileList.length == 0) {
                this.$message.warning("请先上传图片!");
                return
            } else if (this.fileList.length > 1) {
                this.$message.warning("只能上传一张图片!");
                return
            }
            var reqBody = {
                txt2img: true,
                width: this.width,
                height: this.height,
                negative_prompt: this.style_config.negative_prompt,
                cfg_scale: this.style_config.cfg_scale,
                steps: this.form.steps,
                model_id: this.style_config.model_id,
                lora_config: this.style_config.lora_config,
                sampler_id: this.style_config.sampler_id,
                vae_id: this.style_config.vae_id,
                batch_size: 1,
                seed: this.seed,
                batch_cnt: this.batch_cnt,
                img_base64_str: this.img_base64_str,
            }
            console.log(reqBody);
            var promise = fetch("/infer/generate", "POST", reqBody)
            promise.then(resp => {
                if (resp.status == 200) {
                    var jsonString = resp.data.result;
                    const jsonArray = JSON.parse(jsonString);
                    const decodedArray = jsonArray.map(base64String => {
                        return "data:image/png;base64," + base64String;
                        // const decodedString = atob(base64String);
                        // return decodedString;
                    });
                    this.imgs = decodedArray;
                }
            })

        },
        keep_random_seed() {
            if (!this.is_keep_random_seed) {
                this.seed = -1
            }
        },
    },
}
</script>

<style scoped>
.active {
    color: rgb(83, 83, 178);
    /* 这里可以设置高亮的样式，比如颜色等，根据实际需求调整 */
}
.active_2 {
    color: rgb(90, 222, 255);
}
</style>
