import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import os
import sys

# 动态获取脚本目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
NOTES_DIR = os.path.join(SCRIPT_DIR, "notes")  # 笔记文件夹路径
UPLOAD_SCRIPT = os.path.join(SCRIPT_DIR, "auto-upload.sh")  # 上传脚本路径

# 自定义事件处理类
class NotesHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_modified = time.time()

    def on_modified(self, event):
        current_time = time.time()
        if current_time - self.last_modified < 5:  # 5 秒防抖
            return
        self.last_modified = current_time

        # 忽略临时文件
        if event.src_path.endswith(".tmp") or event.src_path.endswith("~"):
            return

        print(f"检测到文件变化: {event.src_path}")
        try:
            # 调用 Git 上传脚本
            result = subprocess.run(
                ["C:/Program Files/Git/bin/bash.exe", UPLOAD_SCRIPT],
                capture_output=True,
                text=True,
                encoding="utf-8",  # 指定编码
                errors="replace"    # 替换无法解码的字符
            )
            print("脚本返回码:", result.returncode)
            print("脚本输出:", result.stdout)
            if result.stderr:
                print("脚本错误:", result.stderr)
        except Exception as e:
            print(f"调用脚本时出错: {e}")

if __name__ == "__main__":
    # 检查脚本是否存在
    print(f"脚本路径: {UPLOAD_SCRIPT}")
    if not os.path.exists(UPLOAD_SCRIPT):
        print(f"错误：上传脚本不存在 - {UPLOAD_SCRIPT}")
        sys.exit(1)

    event_handler = NotesHandler()
    observer = Observer()
    observer.schedule(event_handler, path=NOTES_DIR, recursive=True)
    observer.start()

    try:
        
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("程序被用户中断")
    except Exception as e:
        print(f"程序运行时出错: {e}")
    finally:
        observer.stop()
        observer.join()