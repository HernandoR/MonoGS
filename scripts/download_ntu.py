#!/usr/bin/env python3
import os
import requests
import zipfile
from concurrent.futures import ThreadPoolExecutor

# 数据集文件信息数组，格式为：文件名,文件链接
dataset_files = [
    ("eee_01.zip", "https://researchdata.ntu.edu.sg/api/access/datafile/68133"),
    ("eee_02.zip", "https://researchdata.ntu.edu.sg/api/access/datafile/68131"),
    ("eee_03.zip", "https://researchdata.ntu.edu.sg/api/access/datafile/68132"),
    ("nya_01.zip", "https://researchdata.ntu.edu.sg/api/access/datafile/68144"),
    ("nya_02.zip", "https://researchdata.ntu.edu.sg/api/access/datafile/68138"),
    ("nya_03.zip", "https://researchdata.ntu.edu.sg/api/access/datafile/68142"),
    ("sbs_01.zip", "https://researchdata.ntu.edu.sg/api/access/datafile/68139"),
    ("sbs_02.zip", "https://researchdata.ntu.edu.sg/api/access/datafile/68140"),
    ("sbs_03.zip", "https://researchdata.ntu.edu.sg/api/access/datafile/68143"),
    ("rtp_01.zip", "https://researchdata.ntu.edu.sg/api/access/datafile/98194"),
    ("rtp_02.zip", "https://researchdata.ntu.edu.sg/api/access/datafile/98191"),
    ("rtp_03.zip", "https://researchdata.ntu.edu.sg/api/access/datafile/98193"),
    ("tnp_01.zip", "https://researchdata.ntu.edu.sg/api/access/datafile/98195"),
    ("tnp_02.zip", "https://researchdata.ntu.edu.sg/api/access/datafile/98196"),
    ("tnp_03.zip", "https://researchdata.ntu.edu.sg/api/access/datafile/98189"),
    ("spms_01.zip", "https://researchdata.ntu.edu.sg/api/access/datafile/98192"),
    ("spms_02.zip", "https://researchdata.ntu.edu.sg/api/access/datafile/98190"),
    ("spms_03.zip", "https://researchdata.ntu.edu.sg/api/access/datafile/98188"),
    ("calib_stereo.zip", "https://researchdata.ntu.edu.sg/api/access/datafile/58998"),
    (
        "calib_stereo_imu.bag",
        "https://researchdata.ntu.edu.sg/api/access/datafile/58978",
    ),
]

# 创建目标目录
os.makedirs("datasets/ntu_viral", exist_ok=True)


def download_file(file_info):
    file_name, file_url = file_info
    local_file_path = os.path.join("datasets/ntu_viral", file_name)
    if os.path.exists(local_file_path):
        print(f"Skipping: {file_name}")
        return

    def download_with_request(file_url, local_file_path):
        response = requests.get(file_url)
        response.raise_for_status()  # 检查请求是否成功

        with open(local_file_path, "wb") as f:
            f.write(response.content)

        print(f"Downloaded: {local_file_path}")
        return True

    def download_with_wget(file_url, local_file_path):
        os.system(f"wget -O {local_file_path} {file_url}")
        print(f"Downloaded: {local_file_path}")
        return True

    def download_with_axel(file_url, local_file_path):
        os.system(f"axel -p -c -o {local_file_path} {file_url}")
        print(f"Downloaded: {local_file_path}")
        return True

    # 使用 download_with_request 函数下载文件
    download_with_axel(file_url, local_file_path)

    # 如果是 zip 文件，进行解压
    if file_name.endswith(".zip"):
        with zipfile.ZipFile(local_file_path, "r") as zip_ref:
            zip_ref.extractall(os.path.join("datasets/ntu_viral", file_name[:-4]))
        # os.remove(local_file_path)  # 删除 zip 文件
        print(f"Unzipped and removed: {file_name}")


# 使用线程池进行并行下载
with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(download_file, dataset_files)

print("All downloads completed.")
