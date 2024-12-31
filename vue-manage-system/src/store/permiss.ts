import { defineStore } from 'pinia';
import { fetchUserPermissions } from '@/api';

interface ObjectList {
    [key: string]: string[];
}

var userPermissionMap = {}
// FIXME: test
const data = await fetchUserPermissions()

data.data.result.forEach(element => {
    var permissionList = element['permissions']
    // transfer permissionList array(int[]) to string[]
    permissionList.forEach((item, index) => {
        permissionList[index] = item.toString()
    });
    userPermissionMap[element['name']] = permissionList
});


export const usePermissStore = defineStore('permiss', {
    state: () => {
        const defaultList: ObjectList = userPermissionMap;
        const username = localStorage.getItem('vuems_name');
        console.log(username);
        return {
            key: (username == 'admin' ? defaultList.admin : defaultList.user) as string[],
            defaultList,
        };
    },
    actions: {
        handleSet(val: string[]) {
            this.key = val;
        },
    },
});
