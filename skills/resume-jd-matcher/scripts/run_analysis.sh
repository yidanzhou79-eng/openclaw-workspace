#!/bin/bash
# 简历-JD匹配度分析脚本运行器

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/analyze.py"

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查依赖
echo "🔍 检查Python依赖..."
python3 -c "import re, json, logging" 2>/dev/null || {
    echo "✅ 基础依赖已满足"
}

# 运行分析
echo "🚀 开始简历-JD匹配度分析..."
python3 "$PYTHON_SCRIPT"

# 输出结果文件路径
echo ""
echo "📁 分析完成！"
echo "📄 详细分析报告已生成"
echo ""
echo "📋 后续步骤："
echo "1. 将实际JD和简历内容替换到脚本中"
echo "2. 运行: python3 $PYTHON_SCRIPT"
echo "3. 查看分析结果和建议"
echo ""
echo "💡 提示：可以通过OpenClaw agent调用此分析功能"