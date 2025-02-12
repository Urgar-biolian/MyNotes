#!/bin/bash
set -euo pipefail  # 启用严格模式

echo "Git 版本: $(git --version)"
echo "初始目录: $(pwd)"

# 存储初始目录路径
initial_dir=$(pwd)

# 检查 Git 用户配置
if [ -z "$(git config user.email)" ] || [ -z "$(git config user.name)" ]; then
  echo "错误：Git 用户信息未配置！"
  exit 1
fi

# 进入笔记文件夹
cd "/d/GitHub/MyNotes" || { echo "错误：无法进入目录 /d/GitHub/MyNotes"; exit 1; }

# 同步前拉取远程更新
current_branch=$(git branch --show-current)
git pull origin "$current_branch"

# 提交更改
git add .
git commit -m "自动上传笔记 $(date +'%Y-%m-%d %H:%M:%S')"
git push origin "$current_branch"

# 在原目录记录日志
echo "笔记已上传：$(date +'%Y-%m-%d %H:%M:%S')" >> "$initial_dir/upload.log"
echo "同步完成！"