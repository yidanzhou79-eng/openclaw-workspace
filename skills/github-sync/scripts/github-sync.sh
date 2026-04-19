#!/bin/bash
# github-sync.sh - OpenClaw workspace GitHub同步脚本

WORKSPACE_DIR="/Users/zhouyidan/.openclaw/workspace"
RESUME_FOLDER="resume"  # 简历文件夹名称，根据实际情况修改

cd "$WORKSPACE_DIR" || {
    echo "❌ 无法进入workspace目录: $WORKSPACE_DIR"
    exit 1
}

function check_git_repo() {
    if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        echo "❌ 当前目录不是git仓库"
        echo "请先在workspace目录初始化git仓库"
        exit 1
    fi
}

function check_gitignore() {
    # 检查简历文件夹是否在.gitignore里
    if ! grep -q "^$RESUME_FOLDER/" .gitignore 2>/dev/null; then
        echo "⚠️  简历文件夹不在.gitignore中，正在添加..."
        echo "$RESUME_FOLDER/" >> .gitignore
        git add .gitignore
        git commit -m "添加简历文件夹到.gitignore" >/dev/null 2>&1
        echo "✅ 已将简历文件夹添加到.gitignore"
    fi
}

function show_status() {
    echo "=== Git状态 ==="
    git status
}

function sync_to_github() {
    check_git_repo
    check_gitignore
    
    echo "=== 开始同步到GitHub ==="
    
    # 检查是否有修改
    if git diff --quiet && git diff --cached --quiet; then
        echo "ℹ️  没有需要同步的修改"
        return 0
    fi
    
    # 添加所有修改
    echo "正在添加修改..."
    git add .
    
    # 检查简历文件夹是否被意外添加
    if git status --porcelain | grep -q "^A.*$RESUME_FOLDER/"; then
        echo "❌ 错误：简历文件夹被添加到暂存区！"
        echo "正在移除..."
        git reset HEAD "$RESUME_FOLDER/" >/dev/null 2>&1
        echo "✅ 已移除简历文件夹"
    fi
    
    # Commit
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    echo "正在提交修改..."
    git commit -m "自动同步: $timestamp"
    
    # Push
    echo "正在推送到GitHub..."
    if git push; then
        echo "✅ 同步成功！"
        return 0
    else
        echo "❌ 推送失败，请检查网络或GitHub权限"
        return 1
    fi
}

case "$1" in
    status)
        check_git_repo
        show_status
        ;;
    sync)
        sync_to_github
        ;;
    *)
        echo "OpenClaw GitHub同步工具"
        echo "用法:"
        echo "  $0 status  - 查看git状态"
        echo "  $0 sync    - 同步到GitHub"
        exit 1
        ;;
esac
