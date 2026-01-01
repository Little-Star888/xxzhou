import fitz  # PyMuPDF
import base64
import os
from agentscope.tool import ToolResponse
from agentscope.message import (
    Msg,
    TextBlock,
    ImageBlock,
    Base64Source
)
from src.agents.pdf_reader import pdf_reader_agent
import asyncio


async def pdf_reader(prompt: str, pdf_path: str):
    """
    根据用户的提示词，读取和分析PDF文件内容
    :param prompt: 用户的提示词
    :param pdf_path: PDF文件的本地路径
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(pdf_path):
            return ToolResponse(
                content=[TextBlock(type="text", text=f"错误：找不到PDF文件 {pdf_path}")]
            )

        # 检查文件扩展名
        if not pdf_path.lower().endswith('.pdf'):
            return ToolResponse(
                content=[TextBlock(type="text", text=f"错误：文件 {pdf_path} 不是PDF格式")]
            )

        # 提取PDF内容
        pdf_content = extract_pdf_content(pdf_path)

        # 构建消息内容
        message_content = [
            TextBlock(
                type="text",
                text=f"{prompt}\n\nPDF文件：{os.path.basename(pdf_path)}\n\n{pdf_content['text']}"
            )
        ]

        # 处理图片（如果有的话）
        import tempfile
        temp_files = []  # 存储临时文件路径，用于后续清理

        for i, img_data in enumerate(pdf_content['images'][:3]):
            try:
                # 创建临时文件
                temp_fd, temp_path = tempfile.mkstemp(suffix=f'.{img_data["format"]}')
                os.close(temp_fd)  # 关闭文件描述符

                # 解码base64并保存到临时文件
                import base64
                image_bytes = base64.b64decode(img_data['data'])
                with open(temp_path, 'wb') as f:
                    f.write(image_bytes)

                temp_files.append(temp_path)

                # 使用url参数指向临时文件
                message_content.append(
                    ImageBlock(
                        type="image",
                        source=Base64Source(
                            type="url",
                            url=temp_path
                        )
                    )
                )
                print(f"成功添加第{i+1}张图片")
            except Exception as e:
                print(f"处理第{i+1}张图片时出错：{str(e)[:100]}")
                continue

        msg = Msg(
            name="user",
            role="user",
            content=message_content
        )

        res = await pdf_reader_agent(msg)
        # 确保文本内容正确编码
        response_text = res.content[0]["text"]
        if isinstance(response_text, str):
            # 清理可能的问题字符，特别是emoji和特殊Unicode字符
            try:
                # 尝试转换为安全的ASCII字符串，移除非ASCII字符
                safe_text = response_text.encode('ascii', 'ignore').decode('ascii')
                if safe_text.strip():  # 如果清理后还有内容
                    response_text = safe_text
                else:
                    # 如果清理后没有内容，保留基本ASCII字符
                    response_text = ''.join(c for c in response_text if ord(c) < 128 and c.isprintable())
            except:
                # 如果转换失败，返回通用消息
                response_text = "PDF分析完成，但响应内容包含特殊字符无法正确显示。PDF文件已成功读取。"

        # 清理临时文件
        for temp_file in temp_files:
            try:
                os.unlink(temp_file)
            except:
                pass

        # 清理临时文件
        for temp_file in temp_files:
            try:
                os.unlink(temp_file)
            except:
                pass

        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=response_text
                )
            ]
        )

    except Exception as e:
        # 安全地处理错误信息，避免编码问题
        try:
            error_detail = str(e)
            # 移除可能的问题字符
            safe_error = ''.join(c for c in error_detail if ord(c) < 128)
            error_msg = f"PDF读取失败：{safe_error}"
        except:
            error_msg = "PDF读取失败：出现编码错误"

        print("PDF处理错误详情:", error_msg)
        print("PDF文件路径:", pdf_path)
        print("文件是否存在:", os.path.exists(pdf_path))
        if os.path.exists(pdf_path):
            print("文件大小:", os.path.getsize(pdf_path), "bytes")
        return ToolResponse(
            content=[TextBlock(type="text", text=error_msg)]
        )


def extract_pdf_content(pdf_path: str) -> dict:
    """提取PDF中的文本和图片"""
    doc = fitz.open(pdf_path)
    content = {"text": "", "images": []}

    try:
        for page_num in range(min(len(doc), 50)):  # 限制最多处理50页
            page = doc.load_page(page_num)

            # 提取文本
            page_text = page.get_text()
            if page_text.strip():  # 只添加非空页面
                content["text"] += f"\n--- 第{page_num+1}页 ---\n"
                content["text"] += page_text

            # 提取图片
            images = page.get_images(full=True)
            for img_index, img in enumerate(images[:5]):  # 每页最多提取5张图片
                try:
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]

                    # 检查图片数据是否有效
                    if not image_bytes or len(image_bytes) == 0:
                        continue

                    # 转换为base64
                    img_base64 = base64.b64encode(image_bytes).decode('utf-8')

                    # 获取图片格式，如果没有则尝试从图片数据判断
                    img_format = base_image.get("ext", "").lower()
                    if not img_format:
                        # 简单的格式检测
                        if image_bytes.startswith(b'\xff\xd8\xff'):
                            img_format = "jpeg"
                        elif image_bytes.startswith(b'\x89PNG\r\n\x1a\n'):
                            img_format = "png"
                        elif image_bytes.startswith(b'GIF87a') or image_bytes.startswith(b'GIF89a'):
                            img_format = "gif"
                        elif image_bytes.startswith(b'RIFF') and image_bytes[8:12] == b'WEBP':
                            img_format = "webp"
                        else:
                            img_format = "png"  # 默认格式

                    content["images"].append({
                        "page": page_num + 1,
                        "data": img_base64,
                        "format": img_format
                    })
                except Exception as e:
                    print(f"提取第{page_num+1}页第{img_index+1}张图片时出错：{str(e)[:100]}")
                    continue

    finally:
        doc.close()

    return content
