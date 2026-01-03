from agentscope.agent import ReActAgent
from agentscope.formatter import DashScopeChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.tool import Toolkit
from agentscope.tool import write_text_file, view_text_file, insert_text_file

from src.llm import XXzhouModel
from src.tools.pdf_reader import pdf_reader

def get_document_agent():
    """创建文档处理智能体"""
    toolkit = Toolkit()
    toolkit.register_tool_function(pdf_reader)
    toolkit.register_tool_function(write_text_file)
    toolkit.register_tool_function(view_text_file)
    toolkit.register_tool_function(insert_text_file)

    agent = ReActAgent(
        name="文档助手",
        sys_prompt="""
        你是专业的文档处理助手，擅长文本和PDF文件的处理。

        📄 主要功能：
        1. 使用 pdf_reader 工具读取和分析PDF文件内容
        2. 使用文本文件操作工具进行文件读写编辑

        📋 工作规范：
        1. 处理PDF时，支持文本提取、图片识别、表格分析
        2. 文件操作时，确保正确的文件路径和内容格式
        3. 支持批量处理多个文档
        4. 保持文件内容的完整性和格式

        🔧 技术特点：
        - 全面的PDF解析能力（文本、图片、表格）
        - 灵活的文件操作功能（读取、写入、插入、查看）
        - 支持多种文档格式
        - 智能的内容分析和提取

        💡 使用提示：
        - PDF处理支持复杂布局和多媒体内容
        - 文件操作前会验证路径和权限
        - 支持增量编辑和内容追加
        - 提供详细的处理结果反馈

        ⚠️ 注意事项：
        - 操作文件前确保用户有相应权限
        - 备份重要文件避免数据丢失
        - 处理大文件时会提示用户
        """,
        formatter=DashScopeChatFormatter(),
        toolkit=toolkit,
        memory=InMemoryMemory(),
        model=XXzhouModel().get_dashscope_chat_model()
    )

    return agent
