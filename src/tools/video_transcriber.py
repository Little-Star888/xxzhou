import whisper
import os
from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

def transcribe_video(video_path: str, model_name: str = "base"):
    """
    使用 Whisper 模型提取视频中的音频文案

    :param video_path: 视频文件的本地路径
    :param model_name: Whisper 模型名称，可选 'tiny', 'base', 'small', 'medium', 'large'
                      'base' 是最快、资源消耗最小的选择，推荐用于一般使用
                      'medium' 在GPU环境下可获得更好效果
    :return: 提取的文案内容
    """
    # 检查视频文件是否存在
    if not os.path.exists(video_path):
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=f"错误：视频文件不存在 - {video_path}",
                ),
            ]
        )

    # 检查文件是否为支持的视频格式（简单检查扩展名）
    supported_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v']
    file_ext = os.path.splitext(video_path)[1].lower()
    if file_ext not in supported_extensions:
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=f"警告：文件扩展名 {file_ext} 可能不受支持。Whisper 支持常见视频格式，但建议使用 MP4 格式。",
                ),
            ]
        )

    try:
        print(f"正在加载 Whisper 模型: {model_name}...")
        model = whisper.load_model(model_name)

        print(f"正在转录文件: {video_path}...")
        result = model.transcribe(video_path)
        transcribed_text = result["text"]

        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=f"视频文案提取成功！\n\n提取的文案内容：\n{transcribed_text}",
                ),
            ]
        )

    except Exception as e:
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=f"视频文案提取失败：{str(e)}",
                ),
            ]
        )
