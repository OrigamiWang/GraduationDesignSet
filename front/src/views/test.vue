<template>
<el-upload class="upload-demo" :action="uploadUrl()" :on-success="handleSuccess" :on-preview="handlePreview" :on-remove="handleRemove" :file-list="fileList" list-type="picture">
    <el-button size="small" type="primary">点击上传</el-button>
</el-upload>
</template>

<script>
export default {
    data() {
        return {
            fileList: []
        };
    },
    methods: {
        handleSuccess(file) {
            console.log(file.result.filename);
            console.log(file.result.base64_str);
        },
        handleRemove(file, fileList) {
            console.log(file, fileList);
        },
        handlePreview(file) {
            console.log(file);
        },
        uploadUrl() {
            return 'http://localhost:5173/api/file/upload';
        }
    },
}
</script>
