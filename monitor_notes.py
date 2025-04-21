import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 配置路径
NOTES_DIR = os.path.abspath(r"D:\GitHub\MyNotes")
SCRIPT_PATH = os.path.abspath(__file__)  # 获取当前脚本绝对路径
GIT_EXE = r"C:\Program Files\Git\bin\git.exe"

class NotesHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_sync = 0
        self.ignored_paths = {
            SCRIPT_PATH.lower(),  # 忽略脚本自身的修改
            os.path.join(NOTES_DIR, ".git").lower()  # 忽略.git目录
        }
        
    def should_ignore(self, path):
        """检查路径是否应该被忽略"""
        path = os.path.abspath(path).lower()
        return any(
            path == ignored or path.startswith(ignored + os.sep)
            for ignored in self.ignored_paths
        )

    def on_modified(self, event):
        if self.should_ignore(event.src_path):
            return
            
        now = time.time()
        if now - self.last_sync > 5:  # 5秒防抖
            self.last_sync = now
            print(f"检测到有效变更: {event.src_path}")
            self.safe_git_sync(event.src_path)

    def safe_git_sync(self, changed_file):
        try:
            env = os.environ.copy()
            env["GIT_PYTHON_UNBUFFERED"] = "1"
            
            # 1. 只添加当前变更的文件
            subprocess.run(
                [GIT_EXE, "add", changed_file],
                cwd=NOTES_DIR,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding='utf-8',
                errors='replace'
            )
            
            # 2. 提交特定文件
            commit_msg = f"自动提交 {os.path.basename(changed_file)}"
            subprocess.run(
                [GIT_EXE, "commit", "-m", commit_msg],
                cwd=NOTES_DIR,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding='utf-8',
                errors='replace'
            )
            
            # 3. 推送变更
            subprocess.run(
                [GIT_EXE, "push"],
                cwd=NOTES_DIR,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding='utf-8',
                errors='replace'
            )
            
            print(f"✅ 已同步: {changed_file}")
            
        except subprocess.CalledProcessError as e:
            if "nothing to commit" in e.stderr:
                print("🟡 无新变更需要提交")
            else:
                print(f"🔴 同步失败: {e.stderr.strip() or e.stdout.strip()}")
        except Exception as e:
            print(f"⚠️ 意外错误: {str(e)}")

if __name__ == "__main__":
    print(f"📁 监控目录: {NOTES_DIR}")
    print(f"🚫 忽略路径: {SCRIPT_PATH}")
    
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