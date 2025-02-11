import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import os

# 笔记文件夹路径
NOTES_DIR = "D:/GitHub/MyNotes"

# 自定义事件处理类
class NotesHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_modified = time.time()

    def on_modified(self, event):
        current_time = time.time()
        if current_time - self.last_modified < 2:  # 2 秒内不重复处理
            return
        self.last_modified = current_time

        print(f"检测到文件变化: {event.src_path}")
        try:
            # 检查脚本权限
            if not os.access("D:/GitHub/MyNotes/auto-upload.sh", os.X_OK):
                print("脚本没有执行权限")
                return

            # 调用 Git 上传脚本
            result = subprocess.run(
                ["D:/GitHub/MyNotes/auto-upload.sh"],
                shell=True,
                capture_output=True,
                text=True
            )
            print("脚本输出:", result.stdout)
            print("脚本错误:", result.stderr)
        except Exception as e:
            print(f"调用脚本时出错: {e}")

if __name__ == "__main__":
    event_handler = NotesHandler()
    observer = Observer()
    observer.schedule(event_handler, path=NOTES_DIR, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    except Exception as e:
        print(f"程序运行时出错: {e}")
    finally:
        observer.join()