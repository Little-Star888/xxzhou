from agentscope.agent import ReActAgent
from agentscope.formatter import DashScopeChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.tool import Toolkit

from src.llm import XXzhouModel
from src.agent_communicator import AgentCommunicator
from src.agents.master_agent import get_master_agent
from src.agents.video_agent import get_video_agent
from src.agents.image_agent import get_image_agent
from src.agents.document_agent import get_document_agent
from src.agents.code_agent import get_code_agent

class AgentFactory:
    """智能体工厂类，负责创建和管理所有专业智能体"""

    @staticmethod
    def create_master_agent():
        """创建总协调智能体"""
        return get_master_agent()

    @staticmethod
    def create_video_agent():
        """创建视频处理智能体"""
        return get_video_agent()

    @staticmethod
    def create_image_agent():
        """创建图片处理智能体"""
        return get_image_agent()

    @staticmethod
    def create_document_agent():
        """创建文档处理智能体"""
        return get_document_agent()

    @staticmethod
    def create_code_agent():
        """创建代码执行智能体"""
        return get_code_agent()

    @staticmethod
    def create_agent_by_name(agent_name):
        """根据名称创建智能体"""
        agent_map = {
            'master_agent': get_master_agent,
            'video_agent': get_video_agent,
            'image_agent': get_image_agent,
            'document_agent': get_document_agent,
            'code_agent': get_code_agent
        }

        if agent_name in agent_map:
            return agent_map[agent_name]()
        else:
            raise ValueError(f"未知的智能体类型: {agent_name}")

    @staticmethod
    def get_agent_by_task_type(task_description):
        """根据任务描述智能选择合适的智能体"""
        # 首先检查是否为复合任务
        from src.agent_communicator import AgentCommunicator
        if AgentCommunicator.is_compound_task(task_description):
            return 'master_agent'  # 复合任务交给总协调器处理

        task_lower = task_description.lower()

        # 视频相关关键词
        video_keywords = ['视频', 'video', '下载', 'download', '文案', 'transcribe', '转录', '音频']
        if any(keyword in task_lower for keyword in video_keywords):
            return 'video_agent'

        # 图片相关关键词
        image_keywords = ['图片', 'image', '生成', 'create', '画图', '识别', 'read', '分析']
        if any(keyword in task_lower for keyword in image_keywords):
            return 'image_agent'

        # 文档相关关键词
        document_keywords = ['文档', 'pdf', '文件', 'text', 'write', 'read', '编辑', '查看']
        if any(keyword in task_lower for keyword in document_keywords):
            return 'document_agent'

        # 代码相关关键词
        code_keywords = ['代码', 'code', '执行', 'run', 'shell', 'python', '脚本', '命令']
        if any(keyword in task_lower for keyword in code_keywords):
            return 'code_agent'

        # 默认使用总协调智能体处理复杂或不明确的任务
        return 'master_agent'
