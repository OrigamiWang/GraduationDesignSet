import { createStore } from 'vuex'

export default createStore({
    state: {
        paramMap: null,
    },
    getters: {},
    mutations: {
        setParamMap(state, paramMap) {
            state.paramMap = paramMap
        }
    },
    actions: {},
    modules: {
    }
})
