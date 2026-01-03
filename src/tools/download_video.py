import subprocess, os, glob
from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

def download_video(url, save_dir):
    """
    下载视频并返回具体的文件路径
    :param url: 视频地址（支持bilibili、youtube等yt-dlp支持的平台）
    :param save_dir: 视频保存的本地路径
    :return: 包含下载结果和文件路径的响应
    """
    os.makedirs(save_dir, exist_ok=True)

    # 构造命令，使用 --print-after-move filepath 获取实际保存的文件路径
    cmd = [
        "yt-dlp",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]",
        "-o", os.path.join(save_dir, "%(title)s.%(ext)s"),
        "--print", "after_move:filepath",  # 输出最终文件路径
        url
    ]

    try:
        # 使用系统默认编码避免编码问题
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='gbk' if os.name == 'nt' else 'utf-8')

        # 从输出中解析实际的文件路径
        downloaded_file = None
        for line in result.stdout.strip().split('\n'):
            if line.startswith(save_dir) and os.path.exists(line):
                downloaded_file = line
                break

        # 如果没找到，尝试查找最新的视频文件
        if not downloaded_file:
            video_files = []
            for ext in ['*.mp4', '*.avi', '*.mkv', '*.mov', '*.wmv', '*.flv', '*.webm']:
                pattern = os.path.join(save_dir, ext)
                video_files.extend(glob.glob(pattern))

            if video_files:
                # 选择最新的文件
                downloaded_file = max(video_files, key=os.path.getmtime)

        if downloaded_file:
            return ToolResponse(
                content=[
                    TextBlock(
                        type="text",
                        text=f"✅ 视频下载成功！\n📁 文件路径：{downloaded_file}\n📊 文件大小：{os.path.getsize(downloaded_file) / (1024*1024):.1f} MB",
                    ),
                ]
            )
        else:
            return ToolResponse(
                content=[
                    TextBlock(
                        type="text",
                        text=f"✅ 下载命令执行成功，但无法确定确切的文件路径。文件可能保存在：{save_dir}",
                    ),
                ]
            )

    except subprocess.CalledProcessError as e:
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=f"❌ 视频下载失败：{e.stderr}",
                ),
            ]
        )
    except Exception as e:
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=f"❌ 下载过程中出现错误：{str(e)}",
                ),
            ]
        )
    