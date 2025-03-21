import request from '../utils/request';

// export const fetchData = () => {
//     return request({
//         url: './mock/table.json',
//         method: 'get'
//     });
// };

// export const fetchUserData = () => {
//     return request({
//         url: './mock/user.json',
//         method: 'get'
//     });
// };

// export const fetchRoleData = () => {
//     return request({
//         url: './mock/role.json',
//         method: 'get'
//     });
// };

export const fetchUserPermissions = () => {
    return request({
        url: '/manage/user_permissions',
        method: 'get'
    });
};

export const fetchHomePermissions = () => {
    return request({
        url: '/manage/home_permissions',
        method: 'get'
    });
};

