import { createRouter, createWebHistory } from 'vue-router'
import store from '../store';


const routes =
    [
        {
            path: '/',
            name: 'Main',
            component: () => import('../views/Main.vue'),
            children: [
                {
                    path: '/',
                    name: 'Home',
                    component: () => import('../views/Home.vue')
                },
                {
                    path: '/models',
                    name: 'Models',
                    component: () => import('../views/Models.vue')
                },
                {
                    path: '/profile',
                    name: 'Profile',
                    component: () => import('../views/Profile.vue')
                },
                {
                    path: '/txt2imgpro',
                    name: 'txt2imgpro',
                    component: () => import('../views/Txt2ImgPro.vue')
                },
                {
                    path: '/img2imgpro',
                    name: 'img2imgpro',
                    component: () => import('../views/Img2ImgPro.vue')
                },
                {
                    path: '/txt2img',
                    name: 'txt2img',
                    component: () => import('../views/Txt2Img.vue')
                },
                {
                    path: '/img2img',
                    name: 'img2img',
                    component: () => import('../views/Img2Img.vue')
                },
                {
                    path: '/avatar',
                    name: 'avatar',
                    component: () => import('../views/Avatar.vue')
                },
                {
                    path: '/bg',
                    name: 'bg',
                    component: () => import('../views/ReplaceBg.vue')
                },
                {
                    path: '/history',
                    name: 'History',
                    component: () => import('../views/History.vue')
                },
            ] 
        },
        {
            path: '/test',
            name: 'test',
            component: () => import('../views/Test.vue'),
        }
    ]

const router = createRouter({
    // 解决通过转发访问，无法访问js的问题（页面白屏）
    history: createWebHistory(),
    routes
})

router.beforeResolve((to, from, next) => {
    // 记录用户访问的URL
    console.log('用户访问的URL:', to.fullPath);
    // 将参数存入map中
    let path = to.fullPath;
    let parts = path.split('/')
    let paramStr = parts.pop().substring(1)
    let paramArr = paramStr.split('&')
    let paramMap = new Map();
    paramArr.forEach(ele => {
        let key = ele.split('=')[0];
        let value = ele.split('=')[1];
        paramMap[key] = value;
    })
    store.commit('setParamMap', paramMap);
    // 继续导航
    next();
});

export default router