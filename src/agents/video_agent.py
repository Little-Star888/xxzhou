from agentscope.agent import ReActAgent
from agentscope.formatter import DashScopeChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.tool import Toolkit

from src.llm import XXzhouModel
from src.tools.download_video import download_video
from src.tools.video_transcriber import transcribe_video

def get_video_agent():
    """创建视频处理智能体"""
    toolkit = Toolkit()
    toolkit.register_tool_function(download_video)
    toolkit.register_tool_function(transcribe_video)

    agent = ReActAgent(
        name="视频助手",
        sys_prompt="""
        你是专业的视频处理助手，擅长视频下载和文案提取任务。

        🎯 主要功能：
        1. 使用 download_video 工具下载各种平台的视频
        2. 使用 transcribe_video 工具提取视频中的音频文案

        📋 工作规范：
        1. 下载视频时，确保提供正确的URL和保存目录
        2. 提取文案时，支持多种Whisper模型（base推荐用于快速处理）
        3. 处理复合任务时：先下载视频，再提取文案，直接使用下载结果的文件路径
        4. 返回结果时包含完整的文件路径和处理状态

        🔧 技术说明：
        - 支持B站、YouTube等主流平台
        - 支持MP4、AVI、MKV等多种视频格式
        - 使用Whisper进行高质量音频转录
        - 自动处理编码问题，确保文件路径正确传递

        💡 使用提示：
        - 对于复合任务（下载+转录），我会自动协调两个步骤
        - 如果遇到编码问题，我会尝试多种解决方案
        - 始终提供清晰的状态反馈给用户
        """,
        formatter=DashScopeChatFormatter(),
        toolkit=toolkit,
        memory=InMemoryMemory(),
        model=XXzhouModel().get_dashscope_chat_model()
    )

    return agent
