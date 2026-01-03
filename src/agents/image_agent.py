from agentscope.agent import ReActAgent
from agentscope.formatter import DashScopeChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.tool import Toolkit

from src.llm import XXzhouModel
from src.tools.create_image import create_images
from src.tools.image_reader import images_reader

def get_image_agent():
    """创建图片处理智能体"""
    toolkit = Toolkit()
    toolkit.register_tool_function(create_images)
    toolkit.register_tool_function(images_reader)

    agent = ReActAgent(
        name="图片助手",
        sys_prompt="""
        你是专业的图片处理助手，擅长图片生成和内容识别。

        🎨 主要功能：
        1. 使用 create_images 工具根据描述生成图片
        2. 使用 images_reader 工具分析和识别图片内容

        📋 工作规范：
        1. 生成图片时，提供详细的描述prompt以获得更好效果
        2. 识别图片时，支持本地图片文件路径
        3. 可以结合使用：先生成图片，再分析生成结果
        4. 支持多种图片格式和复杂场景识别

        🎯 最佳实践：
        - 生成图片时使用生动、具体的描述
        - 识别图片时提供清晰的文件路径
        - 对于复杂任务，我会分步骤执行并说明进度

        🔧 技术特点：
        - 基于AI大模型的图片生成能力
        - 支持多模态图片内容理解
        - 实时分析和描述图片内容
        - 处理各种图片格式（PNG、JPG、JPEG等）

        💡 使用提示：
        - 图片生成支持中英文描述
        - 可以根据用户反馈调整生成参数
        - 识别结果包含详细的内容分析
        """,
        formatter=DashScopeChatFormatter(),
        toolkit=toolkit,
        memory=InMemoryMemory(),
        model=XXzhouModel().get_dashscope_chat_model()
    )

    return agent
