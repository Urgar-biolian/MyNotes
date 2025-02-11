#!/bin/bash

# 进入笔记文件夹
cd /d/GitHub/MyNotes || exit 1

# 添加所有更改
git add . || exit 1

# 提交更改
git commit -m "自动上传笔记 $(date)" || exit 1

# 推送到远程仓库
git push origin main || exit 1

# 输出日志
echo "笔记已上传：$(date)" >> upload.log