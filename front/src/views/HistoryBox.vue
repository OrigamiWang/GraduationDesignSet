<template>
<div style="height: 15vw; width: 20vw;">
    <router-link :to="{ path: toPath, query: props.query}">
        <el-image style="width: 100%; height: 100%;" :src="url" :fit="fit" />
    </router-link>
</div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { fetch } from '../service/fetch.js';

const fit = ref('contain')
const url = ref("")
// const type = ref("img2imgpro")
const props = defineProps(['query'])
const toPath = ref("")


onMounted(() => {
    update()
})

const update = () => {
    // update path
    toPath.value = "/" + props.query.type

    // update img
    const path = props.query.path
    const reqBody = {
        "path": path
    }
    var promise = fetch("/oss/path", "POST", reqBody);
    promise.then(resp => {
        if (resp.status == 200) {
            if (resp.data.result.length > 0) {
                const res = resp.data.result
                url.value = res[0]
            }
        }
    })
}

</script>

<style lang="css" scoped>
</style>
