<template>
<header class="bg-gray-700 p-4" style="padding-left: 4.5vw;">
    <nav>
        <ul class="flex space-x-4" style="align-items: center;">
            <el-button :ref="el => ref1 = el" link :class="{ 'active_2': $route.path === '/txt2imgpro' }" type="primary">
                <router-link to="/txt2imgpro">文生图-专业</router-link>
            </el-button>
            <el-button :ref="el => ref2 = el" link :class="{ 'active_2': $route.path === '/img2imgpro' }" type="primary">
                <router-link to="/img2imgpro">图生图-专业</router-link>
            </el-button>
            <el-button :ref="el => ref3 = el" link :class="{ 'active_2': $route.path === '/txt2img' }" type="primary">
                <router-link to="/txt2img">文生图-入门</router-link>
            </el-button>
            <el-button :ref="el => ref4 = el" link :class="{ 'active_2': $route.path === '/img2img' }" type="primary">
                <router-link to="/img2img">图生图-入门</router-link>
            </el-button>
            <el-button :ref="el => ref5 = el" link :class="{ 'active_2': $route.path === '/avatar' }" type="primary">
                <router-link to="/avatar">动漫头像</router-link>
            </el-button>
            <el-button :ref="el => ref6 = el" link :class="{ 'active_2': $route.path === '/bg' }" type="primary">
                <router-link to="/bg">动漫背景替换</router-link>
            </el-button>
        </ul>
    </nav>
</header>
<div style="margin-top: 2vh; min-height: 80vh">
    <div class="around column">
        <div id="form">
            <el-form :model="form" :label-position="itemLabelPosition" label-width="auto" size="default" style="width: 35vw; max-width: 35vw;">
                <el-form-item label="图片上传">
                    <el-upload class="upload-demo" :action="uploadUrl()" :on-success="handleSuccess" :on-preview="handlePreview" :on-remove="handleRemove" :file-list="fileList" list-type="picture">
                        <el-button size="small" type="primary">点击上传</el-button>
                    </el-upload>
                </el-form-item>
                <el-form-item label="图片风格">
                    <el-select v-model="form.style_name" placeholder="请选择" style="width: 25vw;">
                        <el-option v-for="item in style_options" :key="item.value" :label="item.label" :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="width">
                    <el-slider :max=2560 style="width:25vw;" v-model="width" show-input>
                    </el-slider>
                </el-form-item>
                <el-form-item label="height">
                    <el-slider :max=2560 style="width:25vw;" v-model="height" show-input>
                    </el-slider>
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
        <ImgViewer :showImgViewer="showImgViewer" :imgList="imgList"></ImgViewer>
        <Progress :showProgress="showProgress" :title="title"></Progress>
    </div>
</div>
</template>

  
<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { fetch } from '../service/fetch.js';
import ImgViewer from './ImgViewer.vue';
import Progress from './Progress.vue';
import { useRoute } from 'vue-router';
const route = useRoute();

const showImgViewer = ref(false)
const showProgress = ref(false)
const imgList = ref([])
const itemLabelPosition = ref('right')
const title = ref('生成中,请等待...')
const ref1 = ref(null);
const ref2 = ref(null);
const ref3 = ref(null);
const ref4 = ref(null);
const ref5 = ref(null);
const ref6 = ref(null);

const fileList = ref([]);
const steps_options = ref([{ "label": "粗糙", "value": 10 }, { "label": "中等", "value": 25 }, { "label": "精细", "value": 50 }]);
const form = ref({});
const style_options = ref([]);
const style_config = ref({});
const width = ref(720);
const height = ref(1280);
const is_keep_random_seed = ref(false);
const batch_cnt = ref(1);
const seed = ref(-1);
const img_base64_str = ref('');
const ossUrl = ref("")
const query_config = ref({})

// imgs: ["https://dummyimage.com/1024x2048&text=A"],

const handleSuccess = (file) => {
    var oss_url = file.result.oss_url;
    fileList.value.push({ "filename": file.result.filename, "base64_str": file.result.base64_str, "oss_url": oss_url });
    img_base64_str.value = file.result.base64_str;
    const path = oss_url.substring(39, oss_url.indexOf("?"))
    ossUrl.value = path;
};


const handleRemove = (file, fileList) => {
    console.log("remove file...");
};

const handlePreview = (file) => {
    console.log("preview file...");
};

const uploadUrl = () => {
    return 'http://localhost:5173/api/file/upload?uid=' + localStorage.getItem("uid");
};

const get_style_list = async () => {
    const promise = await fetch("/sd/get_style_list", "POST", null);
    if (promise.status == 200) {
        const style_list = promise.data.result;
        style_list.forEach(style => {
            style_options.value.push({
                value: style.style_config,
                label: style.name,
            });
        });
    }
};

onMounted(() => {
    // this.auto_resize_img()
    get_style_list();
    set_template();
    set_by_arg();
});

const set_by_arg = () => {
    if (route.query.type != null) {
        console.log("加载历史记录...");
        query_config.value = JSON.parse(JSON.stringify(route.query))
        query_config.value.config = JSON.parse(query_config.value.config)

        const q_config = query_config.value
        const template = q_config.config
        
        showImgViewer.value = true


        form.value.steps = template.steps;
        form.value.style_name = "塔罗牌";
        width.value = template.width;
        height.value = template.height;
        style_config.value = template.style_config;

        const reqBody = {
            "path": q_config.path
        }

        var promise = fetch("/oss/path", "POST", reqBody);
        promise.then(resp => {
            if (resp.status == 200) {
                if (resp.data.result.length > 0) {
                    const res = resp.data.result
                    imgList.value = res
                }
            }
        })
        const reqBody2 = {
            "path": template.oss_url
        }
        var promise2 = fetch("/oss/path", "POST", reqBody2);
        promise2.then(resp => {
            if (resp.status == 200) {
                if (resp.data.result.length > 0) {
                    const res = resp.data.result
                    fileList.value = [{"name": "1", "url": res[0]}]
                }
            }
        })

    }
}

const set_template = () => {
    // 设置模板，用于快速填充配置
    const template = {
        "txt2img": true,
        "width": 720,
        "height": 1280,
        "style_name": "塔罗牌",
        "style_config": { "vae_id": "orangemixvaeReupload_v10.pt", "model_id": "anything-v4.5.ckpt", "cfg_scale": 7, "sampler_id": "DPM++ 2M Karras", "lora_config": { "AtdanLora.safetensors": 0.6, "AnimeTaroCard.safetensors": 1.0 }, "negative_prompt": "bad fingers" },
        "steps": 10,
    };

    form.value.steps = template.steps;
    form.value.style_name = template.style_name;
    width.value = template.width;
    height.value = template.height;
    style_config.value = template.style_config;
};

const generate_img = async () => {
    showProgress.value = true
    const reqBody = {
        uid: localStorage.getItem("uid"),
        type: "img2img",
        txt2img: true,
        width: width.value,
        height: height.value,
        negative_prompt: style_config.value.negative_prompt,
        cfg_scale: style_config.value.cfg_scale,
        steps: form.value.steps,
        model_id: style_config.value.model_id,
        lora_config: style_config.value.lora_config,
        sampler_id: style_config.value.sampler_id,
        vae_id: style_config.value.vae_id,
        batch_size: 1,
        seed: seed.value,
        batch_cnt: batch_cnt.value,
        img_base64_str: img_base64_str.value,
        oss_url: ossUrl.value
    };
    console.log(reqBody);
    const promise = await fetch("/infer/generate", "POST", reqBody);
    if (promise.status == 200) {
        var jsonString = promise.data.result;
        var url_list = JSON.parse(jsonString)
        var res = [];
        url_list.forEach(url => {
            res.push(url)
        })
        console.log("res: ");
        console.log(res);
        imgList.value = res
        showProgress.value = false
        showImgViewer.value = true
    }
};

const keep_random_seed = () => {
    if (!is_keep_random_seed.value) {
        seed.value = -1;
    }
};

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
