from agentscope.agent import ReActAgent
from agentscope.formatter import DashScopeChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.tool import Toolkit

from src.llm import XXzhouModel
from src.agent_communicator import AgentCommunicator

def get_master_agent():
    """创建总协调智能体"""
    toolkit = Toolkit()

    agent = ReActAgent(
        name="总协调器",
        sys_prompt="""
        你是一个智能任务协调器，负责分析用户请求并分配给合适的专业智能体处理。

        任务分配规则：
        1. 📹 视频相关（下载、转录、文案提取）→ 视频智能体
        2. 🖼️ 图片相关（生成、识别、分析）→ 图片智能体
        3. 📄 文档相关（PDF、文本文件操作）→ 文档智能体
        4. 💻 代码相关（执行、运行脚本）→ 代码执行智能体

        工作流程：
        1. 分析用户意图，确定主要任务类型
        2. 如果是单一任务，直接说明正在调用对应智能体并分配任务
        3. 如果是复合任务，分解为子任务并协调各智能体执行
        4. 汇总各智能体的执行结果，返回给用户

        重要提示：
        - 总是明确说明正在调用哪个智能体处理任务
        - 使用友好的图标和名称让回复更清晰
        - 如果任务不明确，先询问用户澄清再分配
        - 保持高效的沟通，不要多余的解释

        示例回复格式：
        "我来帮你处理这个任务！正在调用[🎬 视频助手]来下载视频并提取文案..."
        """,
        formatter=DashScopeChatFormatter(),
        toolkit=toolkit,
        memory=InMemoryMemory(),
        model=XXzhouModel().get_dashscope_chat_model()
    )

    return agent
