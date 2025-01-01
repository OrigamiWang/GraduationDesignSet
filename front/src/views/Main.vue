<template>
<div class="bg-gray-900 text-white full">
    <header class="bg-gray-800 p-4">
        <div class="container mx-auto flex justify-between items-center">
            <h1 class="text-2xl font-bold">ORIGAMI</h1>
            <nav>
                <ul class="flex space-x-4">
                    <li :class="{ 'active': $route.path === '/' }">
                        <router-link to="/">Home</router-link>
                    </li>
                    <li :class="{ 'active': $route.path === '/models' }">
                        <router-link to="/models">Models</router-link>
                    </li>
                    <li :class="{ 'active': $route.path === '/images' }">
                        <router-link to="/images">Images</router-link>
                    </li>
                    <li>
                        <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                            <router-link to="/create">Create</router-link>
                        </button>
                    </li>
                    <!-- <li>
                        <el-button type="primary" @click="showLoginDialog = true">
                            Sign In
                        </el-button>
                    </li> -->
                    <li v-if="!isLoggedIn">
                        <el-button type="primary" @click="showLoginDialog = true">
                            Sign In
                        </el-button>
                    </li>
                    <li v-else>
                        <el-dropdown>
                            <span class="el-dropdown-link">
                                <el-avatar style="cursor: pointer;" @click="showAvatarDropdown = true">
                                    <img src="../assets/avatar/people.png" alt="">
                                </el-avatar>
                            </span>
                            <template #dropdown>
                                <el-dropdown-menu style="background-color: #25262b;">
                                    <el-dropdown-item icon="el-icon-edit">
                                        <el-icon color="#0c72c0">
                                            <User />
                                        </el-icon>
                                        <span style="color: #b3b3b7;">Your Profile</span>
                                    </el-dropdown-item>
                                    <el-dropdown-item icon="el-icon-edit">
                                        <el-icon color="#f28c12">
                                            <Star />
                                        </el-icon>
                                        <span style="color: #b3b3b7;">Liked</span>
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
    <el-dropdown trigger="click" class="avatar-dropdown" v-if="isLoggedIn">
        <span class="el-dropdown-link">
            <i class="el-icon-user"></i>
        </span>
        <el-dropdown-menu slot="dropdown">
            <el-dropdown-item icon="el-icon-user">Profile</el-dropdown-item>
            <el-dropdown-item icon="el-icon-star-on">Stars</el-dropdown-item>
            <el-dropdown-item icon="el-icon-heart">Liked Models</el-dropdown-item>
        </el-dropdown-menu>
    </el-dropdown>
</div>
</template>

<script>
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
            images: [
                { id: 1, url: 'https://example.com/img1.jpg' },
                { id: 2, url: 'https://example.com/img2.jpg' },
                { id: 3, url: 'https://example.com/img3.jpg' },
                { id: 4, url: 'https://example.com/img4.jpg' },
                { id: 5, url: 'https://example.com/img5.jpg' },
                { id: 6, url: 'https://example.com/img6.jpg' },
                { id: 7, url: 'https://example.com/img7.jpg' },
                { id: 8, url: 'https://example.com/img8.jpg' },
                { id: 9, url: 'https://example.com/img9.jpg' },
                { id: 10, url: 'https://example.com/img10.jpg' },
            ],
            itemsPerPage: 8,
            currentPage: 1,
            isLoggedIn: false // 新增，用于控制头像按钮显示隐藏
        };
    },
    computed: {
        totalPages() {
            return Math.ceil(this.images.length / this.itemsPerPage);
        },
        currentPageImages() {
            const start = (this.currentPage - 1) * this.itemsPerPage;
            const end = start + this.itemsPerPage;
            return this.images.slice(start, end);
        }
    },
    methods: {
        prevPage() {
            if (this.currentPage > 1) {
                this.currentPage--;
            }
        },
        nextPage() {
            if (this.currentPage < this.totalPages) {
                this.currentPage++;
            }
        },
        goToPage(page) {
            if (page >= 1 && page <= this.totalPages) {
                this.currentPage = page;
            }
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
            // 这里可以添加实际的登录验证逻辑，比如发送请求到后端验证用户名和密码
            // 暂时假设验证成功，设置登录状态为true并关闭登录窗口、隐藏Sign In按钮
            this.isLoggedIn = true;
            this.showLoginDialog = false;
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
                // 这里简化处理，实际项目中要发送注册请求到后端，成功后再进行登录操作等
                // 假设注册成功后直接设置登录状态相关数据，模拟自动登录
                this.loginForm.username = this.registerForm.username;
                this.loginForm.password = this.registerForm.password;
                this.showRegisterDialog = false;
                this.showLoginDialog = false;
                this.handleLogin();
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
    font-weight: bold;
}

.avatar-dropdown {
    margin-left: 10px;
    /* 根据实际情况调整头像按钮位置 */
}
</style>
