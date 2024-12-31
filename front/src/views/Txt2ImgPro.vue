<template>
<div class="full">
    <h1 class="center">文生图-专业</h1>
    <div class="around column">
        <div id="form">
            <el-form ref="form" :model="form">
                <el-form-item label="Stable Diffusion checkpoint">
                    <el-select @change="change_model" v-model="form.model_name" placeholder="请选择" style="width: 25vw;">
                        <el-option v-for="item in model_options" :key="item.value" :label="item.label" :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="Lora">
                    <div style="width: 50vw;">
                        <div v-for="(item, index) in lora_items" :key="index">
                            <el-select style="width: 30vw; margin-right: 1vw;" v-model="item.selectedValue" placeholder="请选择">
                                <el-option v-for="option in lora_options" :key="option.value" :label="option.label" :value="option.value">
                                </el-option>
                            </el-select>
                            <el-input-number v-model="item.weight" :min="0" :max="10" :step="0.1"></el-input-number>
                            <el-button @click="remove_lora_item(index)">删除</el-button>
                        </div>
                        <el-button @click="add_lora_item">添加</el-button>
                    </div>
                </el-form-item>
                <el-form-item label="prompt">
                    <el-input type="textarea" style="width:25vw;" autosize placeholder="prompt" v-model="prompt"></el-input>
                </el-form-item>
                <el-form-item label="negative_prompt">
                    <el-input type="textarea" style="width:25vw;" autosize placeholder="negative_prompt" v-model="negative_prompt"></el-input>
                </el-form-item>
                <el-form-item label="sampling_method">
                    <el-select style="width:15vw;" v-model="sampling_val" placeholder="请选择">
                        <el-option v-for="item in sapmling_options" :key="item.value" :label="item.label" :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="vae_method">
                    <el-select style="width:15vw;" v-model="vae_val" placeholder="请选择">
                        <el-option v-for="item in vae_options" :key="item.value" :label="item.label" :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="sampling_steps">
                    <el-slider :max=100 style="width:25vw;" v-model="sampling_steps" show-input>
                    </el-slider>
                </el-form-item>
                <el-form-item label="width">
                    <el-slider :max=2560 style="width:25vw;" v-model="width" show-input>
                    </el-slider>
                </el-form-item>
                <el-form-item label="height">
                    <el-slider :max=2560 style="width:25vw;" v-model="height" show-input>
                    </el-slider>
                </el-form-item>
                <el-form-item label="batch_cnt">
                    <el-slider :max=5 style="width:25vw;" v-model="batch_cnt" show-input>
                    </el-slider>
                </el-form-item>
                <el-form-item label="cfg_scale">
                    <el-slider :max=20 style="width:25vw;" v-model="cfg_scale" show-input>
                    </el-slider>
                </el-form-item>
                <el-form-item label="seed">
                    <el-input-number style="margin-right: 0.5vw" v-model="seed" controls-position="right" :min="-1" :max="9999999999"></el-input-number>
                    <button class="center" type="image" style="margin-right: 0.5vw; height: 3vh; width: 2vw; border: none; cursor: pointer;" @click="get_random_seed">
                        <img style="height: 3vh; width: 2vw;" src="../assets/icon/dice.jpg" alt="random seed">
                    </button>
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
import { fetch } from '../service/fetch.js'

export default {
    mounted() {
        // this.auto_resize_img()
        this.get_model_list()
        this.set_template()
    },
    data() {
        return {
            img: {
                height: '100vh',
                width: '10vw',
            },
            lora_items: [{
                selectedValue: '',
                weight: null,
            }, ],
            form: {},
            model_options: [],
            model_base_map: {},
            lora_options: [],
            prompt: '',
            negative_prompt: '',
            sampling_val: '',
            sapmling_options: [{
                value: 'DPM++ 2M Karras',
                label: 'DPM++ 2M Karras'
            }, ],
            vae_val: '',
            vae_options: [],
            sampling_steps: 50,
            width: 720,
            height: 1280,
            cfg_scale: 7,
            seed: -1,
            is_keep_random_seed: false,
            imgs: [],
            batch_cnt: 1,
            // imgs: ["https://dummyimage.com/1024x2048&text=A"],
        }
    },
    methods: {
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
            }

            this.form.model_name = template.model_id
            var lora_items = []
            for (let key in template.lora_config) {
                var val = template.lora_config[key]
                lora_items.push({
                    selectedValue: key,
                    weight: val,
                })
            }
            this.lora_items = lora_items
            this.prompt = template.prompt
            this.negative_prompt = template.negative_prompt
            this.sampling_val = template.sampler_id
            this.vae_val = template.vae_id
            this.sampling_steps = template.steps
            this.width = template.width
            this.height = template.height
            this.cfg_scale = template.cfg_scale
            this.seed = template.seed

        },
        generate_img() {
            var lora_config = {}
            this.lora_items.forEach(item => {
                lora_config[item.selectedValue] = item.weight
            })

            var reqBody = {
                txt2img: true,
                model_id: this.form.model_name,
                lora_config: lora_config,
                prompt: this.prompt,
                negative_prompt: this.negative_prompt,
                sampler_id: this.sampling_val,
                vae_id: this.vae_val,
                steps: this.sampling_steps,
                batch_size: 1,
                batch_cnt: 1,
                width: this.width,
                height: this.height,
                cfg_scale: this.cfg_scale,
                seed: this.seed,

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
                    console.log(decodedArray);

                    this.imgs = decodedArray;
                }
            })

        },
        remove_lora_item(index) {
            this.lora_items.splice(index, 1);
        },
        add_lora_item() {
            this.lora_items.push({
                selectedValue: '',
                weight: null,
            });
        },
        keep_random_seed() {
            if (!this.is_keep_random_seed) {
                this.seed = -1
            }
        },
        get_random_seed(e) {
            e.preventDefault();
            this.seed = Math.floor(1000000000 + Math.random() * 9000000000);
            this.is_keep_random_seed = false
        },
        handleSelect(key, keyPath) {
            console.log(key, keyPath);
        },
        get_model_list() {
            var promise = fetch("/sd/get_model_list", "POST", null)
            promise.then(resp => {
                if (resp.status == 200) {
                    var model_list = resp.data.result
                    model_list.forEach(model => {
                        var base_name = model['base_name']
                        var model_name = model['model_name']
                        this.model_base_map[model_name] = base_name
                        this.model_options.push({ 'value': model_name, 'label': model_name })
                    })
                }
            })
        },
        flush_lora_config() {
            this.lora_options = []
            this.form.lora_name = ''
            this.lora_items = [{
                selectedValue: '',
                weight: null,
            }, ]
        },
        flush_vae_config() {
            this.vae_options = []
        },
        change_model(new_name) {
            this.flush_lora_config()
            this.flush_vae_config()
            var base_name = this.model_base_map[new_name]

            var promise = fetch("/sd/get_lora_list_by_base_name", "POST", { "base_name": base_name })
            promise.then(resp => {
                if (resp.status == 200) {
                    var lora_list = resp.data.result
                    lora_list.forEach(lora => {
                        var lora_name = lora['lora_name']
                        this.lora_options.push({ 'value': lora_name, 'label': lora_name })
                    })
                }
            })

            var promise = fetch("/sd/get_vae_list_by_base_name", "POST", { "base_name": base_name })
            promise.then(resp => {
                if (resp.status == 200) {
                    var vae_list = resp.data.result
                    vae_list.forEach(vae => {
                        var vae_name = vae['vae_name']
                        this.vae_options.push({ 'value': vae_name, 'label': vae_name })
                    })
                }
            })
        },
    },
}
</script>

<style></style>
