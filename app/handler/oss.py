from util import MINIO_CLI


def get_oss_url_by_path_handler(path):
    print("path:", path)
    is_success, res = MINIO_CLI.ls_one_buk("stable-diffusion", path)
    if is_success:
        return res
    return []