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
        1. 视频相关（下载、转录、文案提取）→ 视频智能体
        2. 图片相关（生成、识别、分析）→ 图片智能体
        3. 文档相关（PDF、文本文件操作）→ 文档智能体
        4. 代码相关（执行、运行脚本）→ 代码执行智能体

        复合任务识别和处理：
        识别复合任务的关键词组合：
        - "下载...并提取" → 先下载，再提取文案
        - "生成...并分析" → 先生成，再分析
        - "下载...然后..." → 按顺序执行多个步骤

        复合任务执行流程：
        1. 识别为复合任务时，分解为有序的子任务
        2. 按依赖顺序依次执行：下载→提取，生成→分析等
        3. 在步骤间传递上下文信息（如文件路径）
        4. 汇总所有步骤的结果

        工作流程：
        1. 分析用户意图，判断是单一任务还是复合任务
        2. 单一任务：直接分配给对应智能体
        3. 复合任务：分解步骤，依次协调执行
        4. 汇总结果，返回给用户

        重要提示：
        - 总是明确说明当前正在执行哪个步骤
        - 复合任务要按正确顺序执行，避免同时调用
        - 使用上下文信息连接各步骤
        - 如果任务不明确，先询问用户澄清

        示例回复格式：
        "这是一个复合任务，我来帮你按顺序处理！"
        "第一步：正在调用视频助手下载视频..."
        "第二步：使用下载的文件提取文案..."
        """,
        formatter=DashScopeChatFormatter(),
        toolkit=toolkit,
        memory=InMemoryMemory(),
        model=XXzhouModel().get_dashscope_chat_model()
    )

    return agent
