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
<div style="margin-top: 2vh; min-height: 80vh">
    <div class="around column">
        <div id="form">
            <el-form :label-position="itemLabelPosition" label-width="auto" size="default" style="width: 30vw; max-width: 30vw;">
                <el-form-item label="图片风格" :label-position="itemLabelPosition">
                    <el-select v-model="style_name" placeholder="请选择">
                        <el-option v-for="item in style_options" :key="item.value" :label="item.label" :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="prompt" :label-position="itemLabelPosition">
                    <el-input type="textarea" autosize placeholder="prompt" v-model="prompt"></el-input>
                </el-form-item>
                <el-form-item label="width" :label-position="itemLabelPosition">
                    <el-slider :max=2560 v-model="width" show-input>
                    </el-slider>
                </el-form-item>
                <el-form-item label="height" :label-position="itemLabelPosition">
                    <el-slider :max=2560 v-model="height" show-input>
                    </el-slider>
                </el-form-item>
                <el-form-item label="图片质量" :label-position="itemLabelPosition">
                    <el-select v-model="steps" placeholder="请选择">
                        <el-option v-for="item in steps_options" :key="item.value" :label="item.label" :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="图片数量" :label-position="itemLabelPosition">
                    <el-slider :max=5 v-model="batch_cnt" show-input>
                    </el-slider>
                </el-form-item>
                <el-form-item label="seed" :label-position="itemLabelPosition">
                    <el-checkbox @click="keep_random_seed" v-model="is_keep_random_seed">保持随机</el-checkbox>
                </el-form-item>
                <el-form-item :label-position="itemLabelPosition">
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
import { fetch } from '../service/fetch.js'
import { ref, onMounted } from 'vue'
import { ElButton, ElForm, ElFormItem, ElSelect, ElOption, ElInput, ElSlider, ElCheckbox, ElCarousel, ElCarouselItem } from 'element-plus'
import ImgViewer from './ImgViewer.vue';
import Progress from './Progress.vue';
import { useRoute } from 'vue-router';
const route = useRoute();

const showImgViewer = ref(false)
const showProgress = ref(false)
const imgList = ref([])
const title = ref('生成中,请等待...')
const steps_options = ref([{ "label": "粗糙", "value": 10 }, { "label": "中等", "value": 25 }, { "label": "精细", "value": 50 }])
const style_name = ref('')
const style_options = ref([])
const style_config = ref({})
const width = ref(720)
const height = ref(1280)
const is_keep_random_seed = ref(false)
const batch_cnt = ref(2)
const prompt = ref('')
const seed = ref(-1)
const steps = ref(10)
const itemLabelPosition = ref('right')
const query_config = ref({})

const get_style_list = () => {
    const promise = fetch("/sd/get_style_list", "POST", null)
    promise.then(resp => {
        if (resp.status == 200) {
            const style_list = resp.data.result
            style_list.forEach(style => {
                style_options.value.push({
                    value: style.style_config,
                    label: style.name,
                })
            })
        }
    })
}

onMounted(() => {
    // this.auto_resize_img()
    get_style_list()
    set_template()
    set_by_arg();
})

const set_by_arg = () => {
    if (route.query.type != null) {
        console.log("加载历史记录...");
        query_config.value = JSON.parse(JSON.stringify(route.query))
        query_config.value.config = JSON.parse(query_config.value.config)

        const q_config = query_config.value
        const template = q_config.config
        
        showImgViewer.value = true


        steps.value = template.steps
        style_name.value = "塔罗牌"
        prompt.value = template.prompt
        width.value = template.width
        height.value = template.height
        style_config.value = template.style_config

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


    }
}

const set_template = () => {
    // 设置模板，用于快速填充配置
    const template = {
        "txt2img": true,
        "width": 720,
        "height": 1280,
        "prompt": "beautiful woman",
        "style_name": "塔罗牌",
        "style_config": { "vae_id": "orangemixvaeReupload_v10.pt", "model_id": "anything-v4.5.ckpt", "cfg_scale": 7, "sampler_id": "DPM++ 2M Karras", "lora_config": { "AtdanLora.safetensors": 0.6, "AnimeTaroCard.safetensors": 1.0 }, "negative_prompt": "bad fingers" },
        "steps": 10,
    }

    steps.value = template.steps
    style_name.value = template.style_name
    prompt.value = template.prompt
    width.value = template.width
    height.value = template.height
    style_config.value = template.style_config
}

const generate_img = () => {
    showProgress.value = true
    const reqBody = {
        uid: localStorage.getItem("uid"),
        type: "txt2img",
        txt2img: true,
        width: width.value,
        height: height.value,
        prompt: prompt.value,
        negative_prompt: style_config.value.negative_prompt,
        cfg_scale: style_config.value.cfg_scale,
        steps: steps.value,
        model_id: style_config.value.model_id,
        lora_config: style_config.value.lora_config,
        sampler_id: style_config.value.sampler_id,
        vae_id: style_config.value.vae_id,
        batch_size: 1,
        seed: seed.value,
        batch_cnt: batch_cnt.value,
    }
    
    
    const promise = fetch("/infer/generate", "POST", reqBody)
    promise.then(resp => {
        if (resp.status == 200) {
            var jsonString = resp.data.result;
            var url_list = JSON.parse(jsonString)
            var res = [];
            url_list.forEach(url => {
                res.push(url)
            })
            imgList.value = res
            showProgress.value = false
            showImgViewer.value = true
        }
    })
}

const keep_random_seed = () => {
    if (!is_keep_random_seed.value) {
        seed.value = -1
    }
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
