<template>
<div class="bg-gray-900 text-white">
    <header class="bg-gray-800 p-4">
        <div class="container flex justify-between items-center">
            <h1 class="text-2xl font-bold" style="margin-left: 3.7vw">
                <router-link to="/">ORIGAMI</router-link>
            </h1>
            <nav>
                <ul class="flex space-x-4" style="align-items: center;">
                    <li :class="{ 'active': $route.path === '/' }">
                        <router-link to="/">Home</router-link>
                    </li>
                    <li :class="{ 'active': $route.path === '/models' }">
                        <router-link to="/models">Models</router-link>
                    </li>
                    <li v-if="!isLoggedIn">
                        <el-button type="primary" @click="showLoginDialog = true">
                            Sign In
                        </el-button>
                    </li>
                    <li v-else>
                        <el-dropdown>
                            <span class="el-dropdown-link">
                                <el-avatar style="cursor: pointer; height: 4vh; width: 4vh" @click="showAvatarDropdown = true">
                                    <img src="../assets/avatar/male.jpg" alt="">
                                </el-avatar>
                            </span>
                            <template #dropdown>
                                <el-dropdown-menu style="background-color: #25262b;">
                                    <router-link to="/profile">
                                        <el-dropdown-item icon="el-icon-edit">
                                            <el-icon color="#0c72c0">
                                                <User />
                                            </el-icon>
                                            <span style="color: #b3b3b7;">Your Profile</span>
                                        </el-dropdown-item>
                                    </router-link>
                                    <router-link to="/history">
                                        <el-dropdown-item icon="el-icon-edit">
                                            <el-icon color="#f28c12">
                                                <Clock />
                                            </el-icon>
                                            <span style="color: #b3b3b7;">History</span>
                                        </el-dropdown-item>
                                    </router-link>
                                    <el-dropdown-item icon="el-icon-edit" divided @click="logout">
                                        <el-icon color="#ff3d57">
                                            <el-icon>
                                                <SwitchButton />
                                            </el-icon>
                                        </el-icon>
                                        <span style="color: #b3b3b7;">Logout</span>
                                    </el-dropdown-item>
                                </el-dropdown-menu>
                            </template>
                        </el-dropdown>
                    </li>
                </ul>
            </nav>
        </div>
    </header>

    <el-dialog title="登录" v-model="showLoginDialog" width="30vw" height="30vh" :before-close="handleLoginDialogClose">
        <el-form :model="loginForm" ref="loginForm" label-width="80px">
            <el-form-item label="用户名">
                <el-input v-model="loginForm.username"></el-input>
            </el-form-item>
            <el-form-item label="密码">
                <el-input v-model="loginForm.password" type="password"></el-input>
            </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
            <el-button @click="handleLogin">登录</el-button>
            <el-button @click="showLoginDialog = false">取消</el-button>
            <el-button type="text" @click="showRegisterDialog = true; showLoginDialog = false">注册</el-button>
        </span>
    </el-dialog>
    <!-- 注册对话框 -->
    <el-dialog title="注册" v-model="showRegisterDialog" width="30vw" height="30vh" :before-close="handleRegisterDialogClose">
        <el-form :model="registerForm" ref="registerForm" label-width="80px">
            <el-form-item label="用户名">
                <el-input v-model="registerForm.username"></el-input>
            </el-form-item>
            <el-form-item label="密码">
                <el-input v-model="registerForm.password" type="password">
                    <template slot="suffix">
                        <el-icon v-if="showPassword1" class="el-icon-view" @click="showPassword1 = false"></el-icon>
                        <el-icon v-else class="el-icon-view-off" @click="showPassword1 = true"></el-icon>
                    </template>
                </el-input>
            </el-form-item>
            <el-form-item label="相同密码">
                <el-input v-model="registerForm.passwordConfirm" type="password">
                    <template slot="suffix">
                        <el-icon v-if="showPassword2" class="el-icon-view" @click="showPassword2 = false"></el-icon>
                        <el-icon v-else class="el-icon-view-off" @click="showPassword2 = true"></el-icon>
                    </template>
                </el-input>
            </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
            <el-button @click="handleRegister">注册</el-button>
            <el-button @click="showRegisterDialog = false">取消</el-button>
        </span>
    </el-dialog>
    <keep-alive>
        <router-view></router-view>
    </keep-alive>
    <footer class="bg-gray-800 p-4 text-center text-gray-500"></footer>
    <!-- 头像按钮及下拉框 -->
    <!-- <el-dropdown trigger="click" class="avatar-dropdown" v-if="isLoggedIn">
        <span class="el-dropdown-link">
            <i class="el-icon-user"></i>
        </span>
        <el-dropdown-menu slot="dropdown">
            <el-dropdown-item icon="el-icon-user">Profile</el-dropdown-item>
            <el-dropdown-item icon="el-icon-star-on">Stars</el-dropdown-item>
        </el-dropdown-menu>
    </el-dropdown> -->
</div>
</template>

<script>
import { fetch } from '../service/fetch.js'

export default {
    data() {
        return {
            showAvatarDropdown: false,
            showLoginDialog: false,
            loginForm: {
                username: '',
                password: ''
            },
            showRegisterDialog: false,
            registerForm: {
                username: '',
                password: '',
                passwordConfirm: ''
            },
            showPassword1: false,
            showPassword2: false,
            itemsPerPage: 8,
            currentPage: 1,
            isLoggedIn: false // 新增，用于控制头像按钮显示隐藏
        };
    },
    computed: {},
    mounted() {
        this.check_login()
    },
    methods: {
        logout() {
            localStorage.removeItem("uid")
            localStorage.removeItem("username")
            localStorage.removeItem("password")
            // 刷新页面
            this.refresh()
        },
        refresh() {
            location.reload();
        },
        check_login() {
            var requestBody = {
                "username": localStorage.getItem("username"),
                "password": localStorage.getItem("password")
            }
            var promise = fetch("/user/check", "POST", requestBody)
            promise.then(resp => {
                if (resp.status == 200) {
                    var res = resp.data.result
                    if (res.length != 0) {
                        this.isLoggedIn = true
                    }
                }
            })
        },
        handleLoginDialogClose() {
            this.showLoginDialog = false;
        },
        handleLogin() {
            // 检查用户名是否为空
            if (!this.loginForm.username.trim()) {
                this.$message.warning('请输入用户名');
                return;
            }
            // 检查密码是否为空
            if (!this.loginForm.password.trim()) {
                this.$message.warning('请输入密码');
                return;
            }
            // 查询数据库，用户名和密码是否正确，正确就把用户名和user-id, 保存到localStorage
            var requestBody = {
                "username": this.loginForm.username,
                "password": this.loginForm.password
            }

            var promise = fetch("/user/check", "POST", requestBody)
            promise.then(resp => {
                if (resp.status == 200) {
                    var res = resp.data.result
                    if (res.length != 0) {
                        var user_detail = res[0]
                        this.$message.success('登录成功！');
                        localStorage.setItem("uid", user_detail.id)
                        localStorage.setItem("username", user_detail.name)
                        localStorage.setItem("password", user_detail.password)
                        this.isLoggedIn = true;
                        this.showLoginDialog = false;
                    } else {
                        this.$message.warning('用户名或密码错误！');
                        this.isLoggedIn = false;
                        this.showLoginDialog = true;
                    }
                }
            })
        },
        handleRegisterDialogClose() {
            this.showRegisterDialog = false;
        },
        handleRegister() {
            if (!this.registerForm.username.trim()) {
                this.$message.warning('请输入用户名');
                return;
            }
            if (!this.registerForm.password.trim()) {
                this.$message.warning('请输入密码');
                return;
            }
            if (!this.registerForm.passwordConfirm.trim()) {
                this.$message.warning('请再次输入密码');
                return;
            }
            if (this.registerForm.password === this.registerForm.passwordConfirm) {
                var requestBody = {
                    "username": this.registerForm.username,
                    "password": this.registerForm.password
                }
                var promise = fetch("/user/register", "POST", requestBody)
                promise.then(resp => {
                    if (resp.status == 200) {
                        var res = resp.data.result
                        console.log(res.code);
                        if (res.code == 0) {
                            this.loginForm.username = this.registerForm.username;
                            this.loginForm.password = this.registerForm.password;
                            this.showRegisterDialog = false;
                            this.showLoginDialog = false;
                            this.handleLogin();
                        } else {
                            this.$message.warning('用户名已存在,请重新输入!');
                        }
                    }
                })

            } else {
                this.$message.error('两次输入密码不一致，请重新输入');
            }
        },

    }
};
</script>

<style scoped>
.active {
    color: rgb(83, 83, 178);
}

.avatar-dropdown {
    margin-left: 10px;
    /* 根据实际情况调整头像按钮位置 */
}
</style>
