import subprocess
import time
import os


def open_applications(app_list, delay=5):
    """
    按顺序打开多个应用程序，并在每次打开后等待指定的时间

    参数:
    app_list -- 包含应用程序路径的列表
    delay -- 每个应用程序打开后的等待时间(秒)
    """
    for app_path in app_list:
        try:
            # 检查文件是否存在
            if not os.path.exists(app_path):
                print(f"错误: 找不到应用程序 '{app_path}'")
                continue

            print(f"正在打开: {os.path.basename(app_path)}")

            # 判断文件类型并使用适当的方法启动
            if app_path.lower().endswith(".lnk"):
                # 对于快捷方式，使用os.startfile
                os.startfile(app_path)
            else:
                # 对于其他可执行文件，使用subprocess
                subprocess.Popen(app_path)

            # 等待指定的时间
            print(f"等待 {delay} 秒...")
            time.sleep(delay)

        except Exception as e:
            print(f"打开 '{app_path}' 时出错: {e}")


if __name__ == "__main__":
    # 在这里添加你想要打开的软件路径
    applications = [
        r"C:\Users\weina\Desktop\BAAH_GUI.lnk",
        r"C:\Users\weina\Desktop\Alas.lnk",
        r"C:\\Users\\weina\\Desktop\\MuMu.lnk",
        # 添加更多应用程序路径...
    ]

    # 设置打开应用程序之间的延迟时间(秒)
    delay_time = 3

    print("开始启动应用程序...")
    open_applications(applications, delay_time)
    print("所有应用程序已启动完成!")
# pyinstaller --noconfirm --onefile --icon="C:\Users\weina\Downloads\favicon.ico" --name="启动！！！" script.py
