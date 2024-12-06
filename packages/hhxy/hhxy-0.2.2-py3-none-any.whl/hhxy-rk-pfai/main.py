import os
import subprocess


def install_and_run():
    # 下载shell脚本
    subprocess.run(["wget", "https://hhxy01.oss-cn-beijing.aliyuncs.com/PFAI.sh"])

    # 赋予执行权限
    subprocess.run(["chmod", "+x", "PFAI.sh"])

    # 执行shell脚本
    subprocess.run(["./PFAI.sh"])


if __name__ == "__main__":
    install_and_run()