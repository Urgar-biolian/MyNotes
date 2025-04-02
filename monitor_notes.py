import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 配置路径
NOTES_DIR = r"D:\GitHub\MyNotes"
GIT_EXE = r"C:\Program Files\Git\bin\git.exe"

class NotesHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_sync = 0
        
    def on_modified(self, event):
        now = time.time()
        if now - self.last_sync > 5:  # 5秒防抖
            self.last_sync = now
            print(f"检测到文件变化: {event.src_path}")
            self.safe_git_sync()

    def safe_git_sync(self):
        try:
            # 1. 拉取远程变更
            subprocess.run([GIT_EXE, "pull"], 
                         cwd=NOTES_DIR,
                         check=True,
                         capture_output=True,
                         text=True)
            
            # 2. 检查是否有实际变更
            status = subprocess.run([GIT_EXE, "status", "--porcelain"],
                                  cwd=NOTES_DIR,
                                  capture_output=True,
                                  text=True)
            
            if not status.stdout.strip():
                print("无变更需要提交")
                return
                
            # 3. 提交变更
            subprocess.run([GIT_EXE, "add", "."],
                         cwd=NOTES_DIR,
                         check=True,
                         capture_output=True)
            
            commit_result = subprocess.run([GIT_EXE, "commit", "-m", "自动提交"],
                                        cwd=NOTES_DIR,
                                        capture_output=True,
                                        text=True)
            
            if commit_result.returncode != 0:
                if "nothing to commit" in commit_result.stderr:
                    print("无变更需要提交")
                    return
                else:
                    raise subprocess.CalledProcessError(
                        commit_result.returncode,
                        commit_result.args,
                        commit_result.stdout,
                        commit_result.stderr
                    )
            
            # 4. 推送变更
            subprocess.run([GIT_EXE, "push"],
                         cwd=NOTES_DIR,
                         check=True,
                         capture_output=True)
            
            print("同步成功")
            
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr if e.stderr else e.stdout
            print(f"同步失败: {error_msg}")
        except Exception as e:
            print(f"意外错误: {str(e)}")

if __name__ == "__main__":
    handler = NotesHandler()
    observer = Observer()
    observer.schedule(handler, NOTES_DIR, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()