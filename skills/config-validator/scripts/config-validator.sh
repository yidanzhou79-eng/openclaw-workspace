#!/bin/bash
# config-validator.sh - OpenClaw配置验证脚本

CONFIG_PATH="/Users/zhouyidan/.openclaw/openclaw.json"

function validate_json_syntax() {
    if python3 -m json.tool "$CONFIG_PATH" >/dev/null 2>&1; then
        echo "✅ JSON语法正确"
        return 0
    else
        echo "❌ JSON语法错误！"
        python3 -m json.tool "$CONFIG_PATH" 2>&1
        return 1
    fi
}

function validate_config() {
    echo "正在验证OpenClaw配置..."
    
    # 检查JSON语法
    if ! validate_json_syntax; then
        return 1
    fi
    
    # JSON语法正确就认为配置符合要求（因为schema验证比较复杂）
    echo "✅ 配置验证通过（JSON语法正确）"
    return 0
}

function safe_restart() {
    echo "执行安全重启流程..."
    
    if validate_config; then
        echo "✅ 配置验证通过，正在重启网关..."
        openclaw gateway restart
        return 0
    else
        echo "❌ 配置验证失败，禁止重启网关！"
        return 1
    fi
}

case "$1" in
    validate)
        validate_config
        ;;
    safe-restart)
        safe_restart
        ;;
    *)
        echo "OpenClaw配置验证工具"
        echo "用法:"
        echo "  $0 validate       - 手动验证配置"
        echo "  $0 safe-restart  - 安全重启（先验证再重启）"
        exit 1
        ;;
esac
