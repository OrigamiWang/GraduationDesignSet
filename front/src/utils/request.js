import axios from 'axios'

// 创建axios实例
export function requestService(config) {
    const service = axios.create({
        // axios中请求配置有baseURL选项，表示请求URL公共部分
        baseURL: '/api',
        // 超时
        timeout: "30 * 60 * 1000", // 超时时间：30分钟
    })
    // request拦截器
    service.interceptors.request.use(config => {
        return config
    }, error => {
        console.log(error)
        Promise.reject(error)
    })

    // 响应拦截器
    service.interceptors.response.use(res => {
        return res
    },
        error => {
            return Promise.reject(error)
        }
    )
    return service(config)
}