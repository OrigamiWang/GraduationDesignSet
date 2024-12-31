import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router';
import { usePermissStore } from '../store/permiss';
import { fetchHomePermissions } from '@/api';
import Home from '../views/home.vue';
import NProgress from 'nprogress';
import 'nprogress/nprogress.css';


const data = await fetchHomePermissions();
const home_permissions = data.data.result;

var chids = [];


var componentMap = {
    "dashboard": () => import(/* webpackChunkName: "dashboard" */ '../views/dashboard.vue'),
    "system-user": () => import(/* webpackChunkName: "system-user" */ '../views/system/user.vue'),
    "system-role": () => import(/* webpackChunkName: "system-role" */ '../views/system/role.vue'),
    "system-menu": () => import(/* webpackChunkName: "system-menu" */ '../views/system/menu.vue'),
    "basetable": () => import(/* webpackChunkName: "table" */ '../views/table/basetable.vue'),
    "table-editor": () => import(/* webpackChunkName: "table-editor" */ '../views/table/table-editor.vue'),
    "schart": () => import(/* webpackChunkName: "schart" */ '../views/chart/schart.vue'),
    "echarts": () => import(/* webpackChunkName: "echarts" */ '../views/chart/echarts.vue'),
    "icon": () => import(/* webpackChunkName: "icon" */ '../views/pages/icon.vue'),
    "ucenter": () => import(/* webpackChunkName: "ucenter" */ '../views/pages/ucenter.vue'),
    "editor": () => import(/* webpackChunkName: "editor" */ '../views/pages/editor.vue'),
    "markdown": () => import(/* webpackChunkName: "markdown" */ '../views/pages/markdown.vue'),
    "export": () => import(/* webpackChunkName: "export" */ '../views/table/export.vue'),
    "import": () => import(/* webpackChunkName: "import" */ '../views/table/import.vue'),
    "theme": () => import(/* webpackChunkName: "theme" */ '../views/pages/theme.vue'),
    "calendar": () => import(/* webpackChunkName: "calendar" */ '../views/element/calendar.vue'),
    "watermark": () => import(/* webpackChunkName: "watermark" */ '../views/element/watermark.vue'),
    "carousel": () => import(/* webpackChunkName: "carousel" */ '../views/element/carousel.vue'),
    "tour": () => import(/* webpackChunkName: "tour" */ '../views/element/tour.vue'),
    "steps": () => import(/* webpackChunkName: "steps" */ '../views/element/steps.vue'),
    "form": () => import(/* webpackChunkName: "form" */ '../views/element/form.vue'),
    "upload": () => import(/* webpackChunkName: "upload" */ '../views/element/upload.vue'),
    "statistic": () => import(/* webpackChunkName: "statistic" */ '../views/element/statistic.vue'),
};

home_permissions.forEach((item, index) => {
    var id = item['id'];
    var name = item['name'];
    var path = item['path'];
    var title = item['title'];
    var no_auth = item['no_auth'];

    var d = {}
    d['path'] = path;
    d['name'] = name;
    d['meta'] = { 'title': title }
    if (no_auth == 1) {
        d['meta']['noAuth'] = true;
    } else {
        d['meta']['permiss'] = id.toString();
    }
    d['component'] = componentMap[name]
    chids.push(d);
});


const routes: RouteRecordRaw[] = [
    {
        path: '/',
        redirect: '/dashboard',
    },
    {
        path: '/',
        name: 'Home',
        component: Home,
        children: chids,
    },
    {
        path: '/login',
        meta: {
            title: '登录',
            noAuth: true,
        },
        component: () => import(/* webpackChunkName: "login" */ '../views/pages/login.vue'),
    },
    {
        path: '/register',
        meta: {
            title: '注册',
            noAuth: true,
        },
        component: () => import(/* webpackChunkName: "register" */ '../views/pages/register.vue'),
    },
    {
        path: '/reset-pwd',
        meta: {
            title: '重置密码',
            noAuth: true,
        },
        component: () => import(/* webpackChunkName: "reset-pwd" */ '../views/pages/reset-pwd.vue'),
    },
    {
        path: '/403',
        meta: {
            title: '没有权限',
            noAuth: true,
        },
        component: () => import(/* webpackChunkName: "403" */ '../views/pages/403.vue'),
    },
    {
        path: '/404',
        meta: {
            title: '找不到页面',
            noAuth: true,
        },
        component: () => import(/* webpackChunkName: "404" */ '../views/pages/404.vue'),
    },
    { path: '/:path(.*)', redirect: '/404' },
];

const router = createRouter({
    history: createWebHashHistory(),
    routes,
});

router.beforeEach((to, from, next) => {
    NProgress.start();
    const role = localStorage.getItem('vuems_name');
    const permiss = usePermissStore();
    if (!role && to.meta.noAuth !== true) {
        next('/login');
    } else if (typeof to.meta.permiss == 'string' && !permiss.key.includes(to.meta.permiss)) {
        // 如果没有权限，则进入403
        next('/403');
    } else {
        next();
    }
});

router.afterEach(() => {
    NProgress.done();
});

export default router;
