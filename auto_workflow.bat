@echo off
setlocal

REM Step 1: 确保当前路径是脚本所在路径（即项目根目录）
cd /d %~dp0

REM Step 2: 运行 Python 项目
echo Running Python script...
uv run stock-positions-backend\main.py

REM Step 3: 等待文件生成（根据项目执行时间可加长）
timeout /t 2 /nobreak >nul

REM Step 4: Git 添加所有新文件（不包含已删除）
echo Adding new files...
git add .

REM Step 5: 提交更改
echo Committing changes...
git commit -m "Auto: update generated files"

REM Step 6: 推送到远端 master 分支
echo Pushing to remote...
git push origin master

echo Done.
endlocal
pause
