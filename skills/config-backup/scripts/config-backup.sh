#!/bin/bash
# config-backup.sh - OpenClaw配置自动备份脚本

BACKUP_DIR="/Users/zhouyidan/planb"
CONFIG_PATH="/Users/zhouyidan/.openclaw/openclaw.json"

mkdir -p "$BACKUP_DIR"

function backup() {
    local timestamp=$(date +"%Y-%m-%d_%H:%M:%S")
    local backup_file="${BACKUP_DIR}/openclaw_config_backup_${timestamp}.json"
    
    cp "$CONFIG_PATH" "$backup_file"
    
    if [ -f "$backup_file" ] && [ $(stat -f%z "$backup_file") -gt 0 ]; then
        echo "✅ 配置备份成功"
        echo "备份文件路径: $backup_file"
        echo "$backup_file" > /tmp/last_config_backup.txt
        return 0
    else
        echo "❌ 备份失败，禁止修改配置！"
        return 1
    fi
}

function list_backups() {
    echo "📋 历史备份列表:"
    ls -lt "$BACKUP_DIR"/openclaw_config_backup_*.json 2>/dev/null | grep -v ".DS_Store" | awk '{
        split($NF, arr, "_")
        timestamp = arr[length(arr)-1] "_" substr(arr[length(arr)], 1, length(arr[length(arr)]) - 5)
        print NR ". " timestamp " - " $NF " (" int($5/1024) "KB)"
    }'
}

function rollback() {
    local version="$1"
    local backup_file=""
    
    if [ -f "$version" ]; then
        backup_file="$version"
    else
        backup_file=$(ls "$BACKUP_DIR"/openclaw_config_backup_*"$version"*.json 2>/dev/null | head -1)
    fi
    
    if [ -z "$backup_file" ] || [ ! -f "$backup_file" ]; then
        echo "❌ 找不到指定备份版本: $version"
        return 1
    fi
    
    cp "$backup_file" "$CONFIG_PATH"
    echo "✅ 回滚成功，已回滚到版本: $(basename "$backup_file" .json | sed 's/openclaw_config_backup_//')"
    
    echo "正在重启网关生效..."
    openclaw gateway restart
}

function validate() {
    if python3 -c "import json; json.load(open('$CONFIG_PATH'))" >/dev/null 2>&1; then
        echo "✅ 当前配置语法正确"
        return 0
    else
        echo "❌ 当前配置语法错误！"
        echo "建议回滚到上一个备份版本: $(cat /tmp/last_config_backup.txt 2>/dev/null || echo "无最近备份")"
        return 1
    fi
}

case "$1" in
    backup)
        backup
        ;;
    list)
        list_backups
        ;;
    rollback)
        if [ -z "$2" ]; then
            echo "❌ 请指定要回滚的版本"
            echo "用法: $0 rollback <备份时间戳/文件路径>"
            exit 1
        fi
        rollback "$2"
        ;;
    validate)
        validate
        ;;
    *)
        echo "OpenClaw配置自动备份工具"
        echo "用法:"
        echo "  $0 backup          - 执行备份"
        echo "  $0 list            - 查看历史备份列表"
        echo "  $0 rollback <版本> - 回滚到指定版本"
        echo "  $0 validate        - 校验当前配置语法"
        exit 1
        ;;
esac
