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
            <el-form ref="form" :model="form" :label-position="itemLabelPosition" label-width="auto" size="default" style="width: 30vw; max-width: 35vw;">
                <el-form-item label="checkpoint" :label-position="itemLabelPosition">
                    <el-select @change="change_model" v-model="form.model_name" placeholder="请选择">
                        <el-option v-for="item in modelOptions" :key="item.value" :label="item.label" :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="Lora" :label-position="itemLabelPosition">
                    <div style="width: 35vw">
                        <div v-for="(item, index) in loraItems" style="margin-top: 5px;" :key="index">
                            <el-select v-model="item.selectedValue" placeholder="请选择">
                                <el-option v-for="option in loraOptions" :key="option.value" :label="option.label" :value="option.value">
                                </el-option>
                            </el-select>
                            <el-input-number style="margin-top: 5px; margin-right: 5px;" v-model="item.weight" :min="0" :max="10" :step="0.1"></el-input-number>
                            <el-button style="margin-top: 5px;" @click="remove_lora_item(index)">删除</el-button>
                        </div>
                        <el-button style="margin-top: 5px;" @click="add_lora_item">添加</el-button>
                    </div>
                </el-form-item>
                <el-form-item label="prompt" :label-position="itemLabelPosition">
                    <el-input type="textarea" autosize placeholder="prompt" v-model="prompt"></el-input>
                </el-form-item>
                <el-form-item label="negative" :label-position="itemLabelPosition">
                    <el-input type="textarea" autosize placeholder="negative_prompt" v-model="negativePrompt"></el-input>
                </el-form-item>
                <el-form-item label="sampling" :label-position="itemLabelPosition">
                    <el-select v-model="samplingVal" placeholder="请选择">
                        <el-option v-for="item in sapmlingOptions" :key="item.value" :label="item.label" :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="vae" :label-position="itemLabelPosition">
                    <el-select v-model="vaeVal" placeholder="请选择">
                        <el-option v-for="item in vaeOptions" :key="item.value" :label="item.label" :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="steps" :label-position="itemLabelPosition">
                    <el-slider :max=100 v-model="samplingSteps" show-input>
                    </el-slider>
                </el-form-item>
                <el-form-item label="width" :label-position="itemLabelPosition">
                    <el-slider :max=2560 v-model="width" show-input>
                    </el-slider>
                </el-form-item>
                <el-form-item label="height" :label-position="itemLabelPosition">
                    <el-slider :max=2560 v-model="height" show-input>
                    </el-slider>
                </el-form-item>
                <el-form-item label="batch cnt" :label-position="itemLabelPosition">
                    <el-slider :max=5 v-model="batchCnt" show-input>
                    </el-slider>
                </el-form-item>
                <el-form-item label="cfg scale" :label-position="itemLabelPosition">
                    <el-slider :max=20 v-model="cfgScale" show-input>
                    </el-slider>
                </el-form-item>
                <el-form-item label="seed" :label-position="itemLabelPosition">
                    <el-input-number v-model="seed" controls-position="right" :min="-1" :max="9999999999"></el-input-number>
                    <button class="center" type="image" style="cursor: pointer; margin-left: 10px; margin-right: 10px;" @click="get_random_seed">
                        <el-icon size="large"><Refresh /></el-icon>
                    </button>
                    <el-checkbox @click="keep_random_seed" v-model="isKeepRandomSeed">保持随机</el-checkbox>
                </el-form-item>
                <el-form-item>
                    <el-button @click="temp_generate_img">生成图片</el-button>
                </el-form-item>
            </el-form>
        </div>
        <ImgViewer :imgList="imgList"></ImgViewer>
        <Progress :showProgress="showProgress"></Progress>
    </div>
</div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { fetch } from '../service/fetch.js';
import ImgViewer from './ImgViewer.vue';
import Progress from './Progress.vue';

const loraItems = ref([{
    selectedValue: '',
    weight: null,
}]);
const form = ref({});
const lora_items = ref({})
const modelOptions = ref([]);
const modelBaseMap = ref({});
const loraOptions = ref([]);
const prompt = ref('');
const negativePrompt = ref('');
const samplingVal = ref('');
const sapmlingOptions = ref([{
    value: 'DPM++ 2M Karras',
    label: 'DPM++ 2M Karras'
}]);

const vaeVal = ref('');
const vaeOptions = ref([]);
const samplingSteps = ref(50);
const width = ref(720);
const height = ref(1280);
const cfgScale = ref(7);
const seed = ref(-1);
const isKeepRandomSeed = ref(false);
const imgs = ref([]);
const batchCnt = ref(1);
const itemLabelPosition = ref('right')
const showProgress = ref(false)
const imgList = ref([])

onMounted(() => {
    // this.auto_resize_img()
    get_model_list();
    set_template();
});

const auto_resize_img = () => {
    if (imgs.value.length > 0) {
        const img = new Image();
        img.src = imgs.value[0];
        img.onload = () => {
            const ratio = img.height / img.width;
            const width = img.width.value.substring(0, img.width.value.length - 2);
            const height = width * ratio;
            img.height.value = height + "vh";
        }
    }
};

const set_template = () => {
    // 设置模板，用于快速填充配置
    var template = {
        "txt2img": true,
        "width": 720,
        "height": 1280,
        "prompt": "beautiful woman",
        "negative_prompt": "bad fingers",
        "cfg_scale": 7,
        "steps": 5,
        "model_id": "anything-v4.5.ckpt",
        "lora_config": {
            "AnimeTaroCard.safetensors": 1.0,
            "AtdanLora.safetensors": 0.6
        },
        "sampler_id": "DPM++ 2M Karras",
        "vae_id": "orangemixvaeReupload_v10.pt",
        "batch_size": 1,
        "seed": -1,
        "batch_cnt": 1
    };

    form.value.model_name = template.model_id;
    var loraItemsTemp = [];
    for (let key in template.lora_config) {
        var val = template.lora_config[key];
        loraItemsTemp.push({
            selectedValue: key,
            weight: val,
        });
    }
    loraItems.value = loraItemsTemp;
    prompt.value = template.prompt;
    negativePrompt.value = template.negative_prompt;
    samplingVal.value = template.sampler_id;
    vaeVal.value = template.vae_id;
    samplingSteps.value = template.steps;
    width.value = template.width;
    height.value = template.height;
    cfgScale.value = template.cfg_scale;
    seed.value = template.seed;
};
const temp_generate_img = () => {
    showProgress.value = true
    // generate
    generate_img()
    showProgress.value = false

}
const generate_img = () => {
    var lora_config = {};
    loraItems.value.forEach(item => {
        lora_config[item.selectedValue] = item.weight;
    });

    var reqBody = {
        uid: localStorage.getItem("uid"),
        type: "txt2imgpro",
        txt2img: true,
        model_id: form.value.model_name,
        lora_config: lora_config,
        prompt: prompt.value,
        negative_prompt: negativePrompt.value,
        sampler_id: samplingVal.value,
        vae_id: vaeVal.value,
        steps: samplingSteps.value,
        batch_size: 1,
        batch_cnt: 1,
        width: width.value,
        height: height.value,
        cfg_scale: cfgScale.value,
        seed: seed.value,
        batch_cnt: batchCnt.value,
    };
    var promise = fetch("/infer/generate", "POST", reqBody);
    promise.then(resp => {
        if (resp.status == 200) {
            var jsonString = resp.data.result;
            var url_list = JSON.parse(jsonString)
            var res = [];   
            url_list.forEach(url => {
                res.push(url)
            })
            console.log("res: ");
            console.log(res);
            imgList.value = res
            // imgs.value = decodedArray;
        }
    });
};

const remove_lora_item = (index) => {
    loraItems.value.splice(index, 1);
};

const add_lora_item = () => {
    loraItems.value.push({
        selectedValue: '',
        weight: null,
    });
};

const keep_random_seed = () => {
    if (!isKeepRandomSeed.value) {
        seed.value = -1;
    }
};

const get_random_seed = (e) => {
    e.preventDefault();
    seed.value = Math.floor(1000000000 + Math.random() * 9000000000);
    isKeepRandomSeed.value = false;
};

const get_model_list = () => {
    var promise = fetch("/sd/get_model_list", "POST", null);
    promise.then(resp => {
        if (resp.status == 200) {
            var model_list = resp.data.result;
            model_list.forEach(model => {
                var base_name = model['base_name'];
                var model_name = model['model_name'];
                modelBaseMap.value[model_name] = base_name;
                modelOptions.value.push({ 'value': model_name, 'label': model_name });
            });
        }
    });
};

const flush_lora_config = () => {
    loraOptions.value = [];
    form.value.lora_name = '';
    loraItems.value = [{
        selectedValue: '',
        weight: null,
    }];
};

const flush_vae_config = () => {
    vaeOptions.value = [];
};

const change_model = (new_name) => {
    flush_lora_config();
    flush_vae_config();
    var base_name = modelBaseMap.value[new_name];

    var promise = fetch("/sd/get_lora_list_by_base_name", "POST", { "base_name": base_name });
    promise.then(resp => {
        if (resp.status == 200) {
            var lora_list = resp.data.result;
            lora_list.forEach(lora => {
                var lora_name = lora['lora_name'];
                loraOptions.value.push({ 'value': lora_name, 'label': lora_name });
            });
        }
    });

    var promise = fetch("/sd/get_vae_list_by_base_name", "POST", { "base_name": base_name });
    promise.then(resp => {
        if (resp.status == 200) {
            var vae_list = resp.data.result;
            vae_list.forEach(vae => {
                var vae_name = vae['vae_name'];
                vaeOptions.value.push({ 'value': vae_name, 'label': vae_name });
            });
        }
    });
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
