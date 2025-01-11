<template>
<header class="bg-gray-700 p-4" style="padding-left: 4.5vw;">
    <nav>
        <ul class="flex space-x-4" style="align-items: center;">
            <el-button :ref="(el) => ref1 = el" link :class="{ 'active_2': $route.path === '/txt2imgpro' }" type="primary">
                <router-link to="/txt2imgpro">文生图-专业</router-link>
            </el-button>
            <el-button :ref="(el) => ref2 = el" link :class="{ 'active_2': $route.path === '/img2imgpro' }" type="primary">
                <router-link to="/img2imgpro">图生图-专业</router-link>
            </el-button>
            <el-button :ref="(el) => ref3 = el" link :class="{ 'active_2': $route.path === '/txt2img' }" type="primary">
                <router-link to="/txt2img">文生图-入门</router-link>
            </el-button>
            <el-button :ref="(el) => ref4 = el" link :class="{ 'active_2': $route.path === '/img2img' }" type="primary">
                <router-link to="/img2img">图生图-入门</router-link>
            </el-button>
            <el-button :ref="(el) => ref5 = el" link :class="{ 'active_2': $route.path === '/avatar' }" type="primary">
                <router-link to="/avatar">动漫头像</router-link>
            </el-button>
            <el-button :ref="(el) => ref6 = el" link :class="{ 'active_2': $route.path === '/bg' }" type="primary">
                <router-link to="/bg">动漫背景替换</router-link>
            </el-button>
        </ul>
    </nav>
</header>
<div style="height: 100vh; min-height: 100vh;">
    <div class="around column">
        <div id="form">
            <el-form :ref="(el) => form = el" :model="form" :label-position="itemLabelPosition" label-width="auto" size="default" style="width: 35vw; max-width: 35vw;">
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
        <ImgViewer :showImgViewer="showImgViewer" :imgList="imgList"></ImgViewer>
        <Progress :showProgress="showProgress" :title="title"></Progress>
    </div>
</div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { fetch } from '../service/fetch.js';
import ImgViewer from './ImgViewer.vue';
import Progress from './Progress.vue';
import { ElMessage } from 'element-plus';
import { useRoute } from 'vue-router';
const route = useRoute();


const showImgViewer = ref(false)
const showProgress = ref(false)
const imgList = ref([])
const title = ref('生成中,请等待...')


const itemLabelPosition = ref('right');
const src_img_file_list = ref([]);
const bg_img_file_list = ref([]);
const form = ref({});
const srcImgOssUrl = ref("");
const bgImgOssUrl = ref("");
const resImgBase64 = ref("");
const resImgOssUrl = ref("");


// const res_b64 = ref('');
const ref1 = ref(null);
const ref2 = ref(null);
const ref3 = ref(null);
const ref4 = ref(null);
const ref5 = ref(null);
const ref6 = ref(null);

onMounted(() => {
    set_by_arg();
})

const set_by_arg = () => {
    if (route.query.type != null) {
        console.log("加载历史记录...");
        const query = JSON.parse(JSON.stringify(route.query))
        const config =  JSON.parse(query.config)
        
        showImgViewer.value = true



        const reqBody = {
            "path": query.path
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
            "path": config['src_img_path']
        }
        var promise2 = fetch("/oss/path", "POST", reqBody2);
        promise2.then(resp => {
            if (resp.status == 200) {
                if (resp.data.result.length > 0) {
                    const res = resp.data.result
                    src_img_file_list.value = [{"name": "1", "url": res[0]}]
                }
            }
        })

        const reqBody3 = {
            "path": config['bg_img_path']
        }
        var promise3 = fetch("/oss/path", "POST", reqBody3);
        promise3.then(resp => {
            if (resp.status == 200) {
                if (resp.data.result.length > 0) {
                    const res = resp.data.result
                    bg_img_file_list.value = [{"name": "1", "url": res[0]}]
                }
            }
        })

    }
}



const handleSrcImgSuccess = (file) => {
    var oss_url = file.result.oss_url;
    src_img_file_list.value.push({ "filename": file.result.filename, "base64_str": file.result.base64_str, "oss_url": oss_url });
    const path = oss_url.substring(39, oss_url.indexOf("?"))
    srcImgOssUrl.value = path;
    ElMessage.success("上传成功!");
};

const handleBgImgSuccess = (file) => {
    var oss_url = file.result.oss_url;
    bg_img_file_list.value.push({ "filename": file.result.filename, "base64_str": file.result.base64_str, "oss_url": oss_url });
    const path = oss_url.substring(39, oss_url.indexOf("?"))
    bgImgOssUrl.value = path;
    ElMessage.success("上传成功!");
};

const handleRemove = (file, fileList) => {
    console.log("remove file...");
};

const handlePreview = (file) => {
    console.log("preview file...");
};

const upload_img = () => {
    return 'http://localhost:5173/api/file/upload?uid=' + localStorage.getItem("uid");
};
const generate_img = () => {
    showProgress.value = true
    if (src_img_file_list.value.length == 0 || bg_img_file_list.value.length == 0) {
        ElMessage.warning("请先上传图片!");
        return;
    } else if (src_img_file_list.value.length > 1 || bg_img_file_list.value.length > 1) {
        ElMessage.warning("只能上传一张图片!");
        return;
    }
    const reqBody = {
        "src_img": src_img_file_list.value[0]['base64_str'],
        "bg_img": bg_img_file_list.value[0]['base64_str'],
    };
    const promise = fetch("/bg/replace", "POST", reqBody);
    promise.then(resp => {
        if (resp.status == 200) {
            resImgBase64.value = resp.data.result
            const b64Img = "data:image/jpeg;base64," + resp.data.result;
            var res = [];
            res.push(b64Img)
            imgList.value = res
            showProgress.value = false
            showImgViewer.value = true



             // upload res img
            var reqBody1 = {
                "uid": localStorage.getItem("uid"),
                "filename": "bg.jpg",
                "type_name": "bg",
                "base64_data": resImgBase64.value,
            }

            const promise1 = fetch("/file/uploadB64", "POST", reqBody1);
            promise1.then(resp => {
                if (resp.status == 200) {
                    var oss_url = resp.data.oss_url
                    const path = oss_url.substring(39, oss_url.indexOf("?"))
                    resImgOssUrl.value = path
                    // add history
                    var reqBody2 = {
                        "uid": localStorage.getItem("uid"),
                        "type": "bg",
                        "buk": "stable-diffusion",
                        "filepath": resImgOssUrl.value,
                        "config": {
                            "src_img_path": srcImgOssUrl.value,
                            "bg_img_path": bgImgOssUrl.value,
                        },
                        "input": {},
                    }
                    const promise2 = fetch("/history/add", "POST", reqBody2);
                    promise2.then(resp => {
                        if (resp.status == 200) {
                            console.log("add his success!");
                            
                        }
                    })

                }
            })



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
