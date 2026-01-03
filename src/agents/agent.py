from agentscope.agent import ReActAgent
from agentscope.formatter import DashScopeChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.tool import (
    Toolkit,
    write_text_file,
    view_text_file,
    insert_text_file,
    execute_python_code,
    execute_shell_command
)
from src.llm import XXzhouModel

from src.tools.download_video import download_video
from src.tools.create_image import create_images
from src.tools.image_reader import images_reader
from src.tools.pdf_reader import pdf_reader
from src.tools.video_transcriber import transcribe_video

toolkit = Toolkit()
toolkit.register_tool_function(write_text_file)
toolkit.register_tool_function(insert_text_file)
toolkit.register_tool_function(view_text_file)
toolkit.register_tool_function(execute_python_code)
toolkit.register_tool_function(execute_shell_command)
toolkit.register_tool_function(download_video)
toolkit.register_tool_function(create_images)
toolkit.register_tool_function(images_reader)
toolkit.register_tool_function(pdf_reader)
toolkit.register_tool_function(transcribe_video)

agent = ReActAgent(
    name="小小舟",
    sys_prompt="""
    1. 你可以使用download_video工具下载视频。
    2. 你根据用户的prompt，调用create_images工具生成图片.
    3. 使用images_reader识别图片内容
    4. 使用pdf_reader读取和分析PDF文件内容，可以提取文本、识别图片和表格
    5. 使用transcribe_video工具提取本地视频文件的音频文案，支持MP4、AVI、MKV等多种视频格式
    """,
    formatter=DashScopeChatFormatter(),
    toolkit=toolkit,
    memory=InMemoryMemory(),
    model=XXzhouModel().get_dashscope_chat_model()
)

# agent.set_console_output_enabled(False)