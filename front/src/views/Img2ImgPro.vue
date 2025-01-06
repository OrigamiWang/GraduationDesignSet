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
            <el-form ref="form" :label-position="itemLabelPosition" label-width="auto" size="default" style="width: 35vw; max-width: 35vw;">
                <el-form-item label="图片上传">
                    <el-upload class="upload-demo" :action="uploadUrl()" :on-success="handleSuccess" :on-preview="handlePreview" :on-remove="handleRemove" :file-list="fileList" list-type="picture">
                        <el-button size="small" type="primary">点击上传</el-button>
                    </el-upload>
                </el-form-item>
                <el-form-item label="checkpoint">
                    <el-select @change="changeModel" v-model="modelName" placeholder="请选择">
                        <el-option v-for="item in modelOptions" :key="item.value" :label="item.label" :value="item.model_name">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="Lora">
                    <div>
                        <div v-for="(item, index) in loraItems" :key="index" style="margin-top: 5px;">
                            <el-select style="width: 30vw; margin-right: 1vw;" v-model="item.selectedValue" placeholder="请选择">
                                <el-option v-for="option in loraOptions" :key="option.value" :label="option.label" :value="option.value">
                                </el-option>
                            </el-select>
                            <el-input-number style="margin-top: 5px; margin-right: 5px" v-model="item.weight" :min="0" :max="10" :step="0.1"></el-input-number>
                            <el-button style="margin-top: 5px;" @click="removeLoraItem(index)">删除</el-button>
                        </div>
                        <el-button style="margin-top: 5px;" @click="addLoraItem">添加</el-button>
                    </div>
                </el-form-item>
                <el-form-item label="negative">
                    <el-input type="textarea" autosize placeholder="negative_prompt" v-model="negativePrompt"></el-input>
                </el-form-item>
                <el-form-item label="sampling">
                    <el-select v-model="samplingVal" placeholder="请选择">
                        <el-option v-for="item in samplingOptions" :key="item.value" :label="item.label" :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="vae">
                    <el-select v-model="vaeVal" placeholder="请选择">
                        <el-option v-for="item in vaeOptions" :key="item.value" :label="item.label" :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="steps">
                    <el-slider :max=100 v-model="samplingSteps" show-input>
                    </el-slider>
                </el-form-item>
                <el-form-item label="width">
                    <el-slider :max=2560 v-model="width" show-input>
                    </el-slider>
                </el-form-item>
                <el-form-item label="height">
                    <el-slider :max=2560 v-model="height" show-input>
                    </el-slider>
                </el-form-item>
                <el-form-item label="batch cnt">
                    <el-slider :max=5 v-model="batchCnt" show-input>
                    </el-slider>
                </el-form-item>
                <el-form-item label="cfg scale">
                    <el-slider :max=20 v-model="cfgScale" show-input>
                    </el-slider>
                </el-form-item>
                <el-form-item label="seed">
                    <el-input-number style="margin-right: 0.5vw" v-model="seed" controls-position="right" :min="-1" :max="9999999999"></el-input-number>
                    <button class="center" type="image" style="margin-right: 0.5vw; height: 3vh;border: none; cursor: pointer;" @click="getRandomSeed">
                        <el-icon size="large"><Refresh /></el-icon>
                    </button>
                    <el-checkbox @click="keepRandomSeed" v-model="isKeepRandomSeed">保持随机</el-checkbox>
                </el-form-item>
                <el-form-item>
                    <el-button @click="generateImg">生成图片</el-button>
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

<script lang="ts" setup>
import { ref, reactive, onMounted } from 'vue';
import { fetch } from '../service/fetch.js';

const fileList = ref([]);
const img = reactive({
    height: '100vh',
    width: '10vw',
});
const loraItems = ref([{
    selectedValue: '',
    weight: null,
}]);
const itemLabelPosition = ref('right')
const modelName = ref('')
const modelOptions = ref([]);
const modelBaseMap = reactive({});
const loraOptions = ref([]);
const negativePrompt = ref('');
const samplingVal = ref('');
const samplingOptions = ref([{
    value: 'DPM++ 2M Karras',
    label: 'DPM++ 2M Karras'
}]);
const vaeVal = ref('');
const vaeOptions = ref([]);
const samplingSteps = ref(5);
const width = ref(720);
const height = ref(1280);
const cfgScale = ref(7);
const seed = ref(-1);
const batchCnt = ref(1);
const isKeepRandomSeed = ref(false);
const imgs = ref([]);
const imgBase64Str = ref("");
const inputImgUrl = ref("");

// 相当于Vue 2中的mounted生命周期钩子
onMounted(() => {
    getModelList();
    setTemplate();
});

// 原handleSuccess方法转换
const handleSuccess = (file) => {
    fileList.value.push({ "filename": file.result.filename, "base64_str": file.result.base64_str });
    imgBase64Str.value = file.result.base64_str;
};

// 原handleRemove方法转换
const handleRemove = (file, fileList) => {
    console.log("remove file...");
};

// 原handlePreview方法转换
const handlePreview = (file) => {
    console.log("preview file...");
};

const uploadUrl = () => {
    return 'http://localhost:5173/api/file/upload';
};

// 原auto_resize_img方法转换
const autoResizeImg = () => {
    if (imgs.value.length > 0) {
        const img = new Image();
        img.src = imgs.value[0];
        img.onload = () => {
            const ratio = img.height / img.width;
            const widthValue = img.width.substring(0, img.width.length - 2);
            const heightValue = widthValue * ratio;
            img.height = heightValue + "vh";
        }
    }
};

const setTemplate = () => {
    // 设置模板，用于快速填充配置
    const template = {
        "txt2img": false,
        "width": 720,
        "height": 1280,
        "negative_prompt": "bad fingers",
        "cfg_scale": 7,
        "steps": 5,
        "model_name": "anything-v4.5.ckpt",
        "lora_config": {
            "AnimeTaroCard.safetensors": 1.0,
            "AtdanLora.safetensors": 0.6
        },
        "sampler_id": "DPM++ 2M Karras",
        "vae_id": "orangemixvaeReupload_v10.pt",
        "batch_size": 1,
        "seed": -1,
        "batch_cnt": 1,
        "input_img_url": "https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg"
    };

    const model_name = template.model_name;
    const loraItemsTemp = [];
    for (const key in template.lora_config) {
        const val = template.lora_config[key];
        loraItemsTemp.push({
            selectedValue: key,
            weight: val,
        });
    }
    modelName.value = model_name
    loraItems.value = loraItemsTemp;
    negativePrompt.value = template.negative_prompt;
    samplingVal.value = template.sampler_id;
    vaeVal.value = template.vae_id;
    samplingSteps.value = template.steps;
    width.value = template.width;
    height.value = template.height;
    cfgScale.value = template.cfg_scale;
    seed.value = template.seed;
    inputImgUrl.value = template.input_img_url;

    imgBase64Str.value = "";
};

const generateImg = () => {
    const loraConfig = {};
    loraItems.value.forEach(item => {
        loraConfig[item.selectedValue] = item.weight;
    });

    const reqBody = {
        txt2img: false,
        model_name: modelName.value,
        lora_config: loraConfig,
        negative_prompt: negativePrompt.value,
        sampler_id: samplingVal.value,
        vae_id: vaeVal.value,
        steps: samplingSteps.value,
        batch_size: 1,
        batch_cnt: batchCnt.value,
        width: width.value,
        height: height.value,
        cfg_scale: cfgScale.value,
        seed: seed.value,
        img_base64_str: imgBase64Str.value,
    };
    console.log(reqBody);
    const promise = fetch("/infer/generate", "POST", reqBody);
    promise.then(resp => {
        if (resp.status == 200) {
            const jsonString = resp.data.result;
            const jsonArray = JSON.parse(jsonString);
            const decodedArray = jsonArray.map(base64String => {
                return "data:image/png;base64," + base64String;
            });
            console.log(decodedArray);
            imgs.value = decodedArray;
        }
    });
};

const removeLoraItem = (index) => {
    loraItems.value.splice(index, 1);
};

const addLoraItem = () => {
    loraItems.value.push({
        selectedValue: '',
        weight: null,
    });
};

const keepRandomSeed = () => {
    if (!isKeepRandomSeed.value) {
        seed.value = -1;
    }
};

const getRandomSeed = (e) => {
    e.preventDefault();
    seed.value = Math.floor(1000000000 + Math.random() * 9000000000);
    isKeepRandomSeed.value = false;
};

const getModelList = () => {
    const promise = fetch("/sd/get_model_list", "POST", null);
    promise.then(resp => {
        if (resp.status == 200) {
            const modelList = resp.data.result;
            modelList.forEach(model => {
                const baseName = model['base_name'];
                const modelName = model['model_name'];
                modelBaseMap[modelName] = baseName;
                modelOptions.value.push({ 'value': modelName, 'label': modelName });
            });
        }
    });
};

// 原flush_lora_config方法转换
const flushLoraConfig = () => {
    loraOptions.value = [];
    loraItems.value = [{
        selectedValue: '',
        weight: null,
    }];
};

// 原flush_vae_config方法转换
const flushVaeConfig = () => {
    vaeOptions.value = [];
};

// 原change_model方法转换
const changeModel = (newName) => {
    flushLoraConfig();
    flushVaeConfig();
    const baseName = modelBaseMap[newName];

    const promise = fetch("/sd/get_lora_list_by_base_name", "POST", { "base_name": baseName });
    promise.then(resp => {
        if (resp.status == 200) {
            const loraList = resp.data.result;
            loraList.forEach(lora => {
                const loraName = lora['lora_name'];
                loraOptions.value.push({ 'value': loraName, 'label': loraName });
            });
        }
    });

    const promise2 = fetch("/sd/get_vae_list_by_base_name", "POST", { "base_name": baseName });
    promise2.then(resp => {
        if (resp.status == 200) {
            const vaeList = resp.data.result;
            vaeList.forEach(vae => {
                const vaeName = vae['vae_name'];
                vaeOptions.value.push({ 'value': vaeName, 'label': vaeName });
            });
        }
    });
};
</script>

<style scoped>
.active {
    color: rgb(83, 83, 178);
    /* 这里可以设置高亮的样式，比如

<style scoped>
.active {
    color: rgb(83, 83, 178);
    /* 这里可以设置高亮的样式，比如颜色等，根据实际需求调整 */
}

.active_2 {
    color: rgb(90, 222, 255);
}
</style>
