from time import sleep

from common import POD_CNT_KEY, SS_NAME_KEY, EMPTY_QUEUE_KEY, LOGGER
from dal import get_key, zset_get_with_prefix, zset_get_all
from util import b2str


"""
    pod调度
"""
POD_CNT = get_key(POD_CNT_KEY)
POD_SS_NAME = get_key(SS_NAME_KEY)

def wait_for_pod_name(model_id):
    while True:
        pod_name, is_success = schedule_pod_name(model_id)
        if is_success:
            LOGGER.debug(f'pod_name: {pod_name}')
            return pod_name
        LOGGER.info("Waiting empty_queue for 2 seconds......")
        sleep(2)


# 通过model_id去redis查询，获取对应的pod_name
def schedule_pod_name(model_id):
    print("==========================schedule_pod_name")
    # 前缀匹配找有该model的缓存的pod
    prefix = f'{model_id}*'
    model_list = zset_get_with_prefix(EMPTY_QUEUE_KEY, prefix)
    if len(model_list) == 0:
        # 没有缓存
        all_model = zset_get_all(EMPTY_QUEUE_KEY)
        if len(all_model) == 0:
            # 找不到，等待
            print("empty_queue为空")
            return "", False
        else:
            # 找score最小的(第一个)
            print("没有缓存，但是empty_queue不为空")
            member = b2str(all_model[0])
            # 获取pod_name
            pod_name = member.split(":")[1]
            return pod_name, True

    else:
        # 使用缓存了model的pod
        print("有缓存")
        member = b2str(model_list[0][0])
        pod_name = member.split(":")[1]
        return pod_name, True

