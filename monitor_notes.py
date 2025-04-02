import time
import re
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 配置区域
NOTES_DIR = r"D:\GitHub\MyNotes"
GIT_BASH_PATH = r"C:\Program Files\Git\bin\bash.exe"
UPLOAD_SCRIPT = r"D:\GitHub\MyNotes\auto-upload.sh"
MIN_INTERVAL = 5  # 最小触发间隔(秒)

class NotesHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_trigger_time = 0
        self.ignore_patterns = [
            r"\.git($|\\|/)",
            r"~$",
            r"\.tmp($|\\|/)",
            r"\.swp$",
            r"\.DS_Store$"
        ]

    def should_ignore(self, path):
        return any(re.search(pattern, path) for pattern in self.ignore_patterns)

    def on_modified(self, event):
        current_time = time.time()
        
        if current_time - self.last_trigger_time < MIN_INTERVAL:
            return
            
        if self.should_ignore(event.src_path):
            return
            
        self.last_trigger_time = current_time
        
        print(f"检测到有效文件变化: {event.src_path}")
        self.run_upload_script()

    def run_upload_script(self):
        try:
            # 显式指定UTF-8编码
            result = subprocess.run(
                [GIT_BASH_PATH, UPLOAD_SCRIPT],
                cwd=NOTES_DIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=60,  # 延长超时时间
                encoding='utf-8',  # 强制使用UTF-8
                errors='replace'  # 替换无法解码的字符
            )
            
            if result.returncode == 0:
                print("自动上传成功！")
                if result.stdout:
                    print(f"输出: {result.stdout}")
            else:
                print(f"上传失败，错误信息:\n{result.stderr}")
                
        except subprocess.TimeoutExpired:
            print("警告：上传脚本执行超时，但可能仍在后台运行")
        except Exception as e:
            print(f"执行上传脚本时出错: {str(e)}")

def main():
    print(f"启动笔记目录监控: {NOTES_DIR}")
    print(f"使用Git Bash路径: {GIT_BASH_PATH}")
    print(f"上传脚本路径: {UPLOAD_SCRIPT}")
    print("按Ctrl+C停止监控...")
    
    event_handler = NotesHandler()
    observer = Observer()
    observer.schedule(event_handler, path=NOTES_DIR, recursive=True)
    
    try:
        observer.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n正在停止监控...")
        observer.stop()
    finally:
        observer.join()
        print("监控已停止")

if __name__ == "__main__":
    main()