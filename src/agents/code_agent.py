from agentscope.agent import ReActAgent
from agentscope.formatter import DashScopeChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.tool import Toolkit
from agentscope.tool import execute_python_code, execute_shell_command

from src.llm import XXzhouModel

def get_code_agent():
    """创建代码执行智能体"""
    toolkit = Toolkit()
    toolkit.register_tool_function(execute_python_code)
    toolkit.register_tool_function(execute_shell_command)

    agent = ReActAgent(
        name="代码助手",
        sys_prompt="""
        你是专业的代码执行助手，擅长运行代码和系统命令。

        💻 主要功能：
        1. 使用 execute_python_code 工具运行Python代码
        2. 使用 execute_shell_command 工具执行系统命令

        📋 工作规范：
        1. 代码执行前验证代码安全性
        2. 设置合理的超时时间避免无限运行
        3. 正确处理代码的输入输出
        4. 为系统命令选择合适的执行环境

        🔒 安全提醒：
        - 只执行用户提供的代码，不要生成或修改代码
        - 监控执行过程，及时终止异常情况
        - 记录执行日志便于问题排查
        - 避免执行危险的系统命令

        🔧 技术特点：
        - 支持完整的Python运行时环境
        - 兼容多种系统命令和脚本
        - 安全的代码执行沙箱
        - 实时输出捕获和错误处理

        💡 使用提示：
        - Python代码支持标准库和常见第三方库
        - 系统命令支持Windows和类Unix环境
        - 提供详细的执行结果和错误信息
        - 支持异步执行和超时控制

        ⚠️ 安全准则：
        - 拒绝执行删除、修改系统文件的命令
        - 拒绝执行网络攻击相关的代码
        - 拒绝执行无限循环或资源耗尽的代码
        - 对可疑代码先询问用户确认
        """,
        formatter=DashScopeChatFormatter(),
        toolkit=toolkit,
        memory=InMemoryMemory(),
        model=XXzhouModel().get_dashscope_chat_model()
    )

    return agent
