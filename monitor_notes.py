import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

# 笔记文件夹路径
NOTES_DIR = "D:/GitHub/MyNotes"

# 自定义事件处理类
class NotesHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f"检测到文件变化: {event.src_path}")
        try:
            # 调用 Git 上传脚本
            subprocess.run(["D:/GitHub/MyNotes/auto-upload.sh"], shell=True)
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