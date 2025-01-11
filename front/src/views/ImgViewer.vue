<template>
<div v-if="props.showImgViewer" class="container mx-auto px-4" style="width: 40vw">
    <div style="display: flex; justify-content: flex-end; align-items: center;">
        <el-button round @click="downloadOriginalImage">
            <el-icon style="margin-right: 1vw;">
                <Download />
            </el-icon>
            <el-text tag="b">下载原图</el-text>
        </el-button>
    </div>
    <el-divider />
    <div class="center" style="flex-direction: column;">
        <div style="user-select: none; display: flex; flex-direction: row; width: 40vw; justify-content: space-around; align-items: center;">
            <div class="arrow" style="cursor: pointer;" @click="prevImg">
                <el-icon style="color: black;" >
                    <Back />
                </el-icon>
            </div>
            <img style="height: 70vh; width: auto" v-bind:src="currentImg" alt="网络不佳">
            <div class="arrow" style="cursor: pointer; " @click="nextImg">
                <el-icon style="color: black;">
                    <Right />
                </el-icon>
            </div>
        </div>

        <div class="flex justify-center mt-4 space-x-2">
            <!-- 使用v-for循环遍历imgList渲染缩略图，绑定点击事件实现跳转 -->
            <img style="cursor: pointer;" v-for="(img, index) in props.imgList" :key="index" v-bind:src="img" alt="网络不佳" class="w-16 h-16 object-cover rounded" :class="{'thumb-blur': img!== currentImg}" @click="showImg(img)">
        </div>
    </div>
</div>
</template>

<script setup>
import { ref, onUpdated } from 'vue';
import { saveAs } from 'file-saver';
const time = ref(0)
const props = defineProps(['imgList', 'showImgViewer'])

// 假设这里是图片路径列表，你可以替换成真实从接口等获取的数据
// const imgList = ref([
// ]);
// 当前显示的图片，初始化为imgList中的第一张
const currentImg = ref(props.imgList[0]);

onUpdated(() => {
    if (time.value == 0) {
        currentImg.value = props.imgList[0]
    }
})

// 点击缩略图切换显示图片的方法
const showImg = (img) => {
    currentImg.value = img;
    time.value += 1
    console.log(time.value);
    
};

// 切换到上一张图片的方法
const prevImg = () => {
    const currentIndex = props.imgList.findIndex(item => item === currentImg.value);
    if (currentIndex > 0) {
        currentImg.value = props.imgList[currentIndex - 1];
    } else {
        currentImg.value = props.imgList[props.imgList.length - 1];
    }
};

// 切换到下一张图片的方法
const nextImg = () => {
    const currentIndex = props.imgList.findIndex(item => item === currentImg.value);
    if (currentIndex < props.imgList.length - 1) {
        currentImg.value = props.imgList[currentIndex + 1];
    } else {
        currentImg.value = props.imgList[0];
    }
};

const downloadOriginalImage = async () => {
    try {
        const response = await fetch(currentImg.value);
        if (!response.ok) {
            console.error(`图片获取失败，状态码：${response.status}`);
            return;
        }
        console.log('返回的Content-Type：', response.headers.get('Content-Type'));
        const blob = await response.blob();
        saveAs(blob, 'original_image.png');
    } catch (error) {
        console.error('下载图片出错：', error);
    }
};
</script>

<style scoped>
.arrow {
    width: 3vw;
    height: 3vw;
    background-color: rgb(249, 250, 251);
    display: flex;
    justify-content: center;
    align-items: center;

    border-radius: 1.5vw;
    box-shadow: 0 0.55vw 1.25vw 0.01vw #d8dcdf;
}

.center {
    display: flex;
    align-items: center;
    justify-items: center;
}

.thumb-blur {
    filter: brightness(80%) blur(2px);
}
</style>
