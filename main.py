import sys, asyncio, os
from agentscope.message import Msg
from src.agent_factory import AgentFactory

async def main():
    if len(sys.argv) < 2:
        print("小小舟智能助手 - 多智能体版本")
        print("=" * 50)
        print("只需要在xxzhou命令后输入您的要求即可。")
        print("例如：xxzhou <你要输入的内容>")
        print()
        print("视频相关：")
        print("  示例：xxzhou 下载这个视频 https://www.bilibili.com/video/BV1fFiwBoEAw 并提取文案")
        print()
        print("图片相关：")
        print("  示例：xxzhou 生成一张美丽的海滩风景图")
        print("  示例：xxzhou 分析这张图片的内容 image.jpg")
        print()
        print("文档相关：")
        print("  示例：xxzhou 读取这个PDF文件的内容 document.pdf")
        print("  示例：xxzhou 在文件中写入一些内容")
        print()
        print("代码相关：")
        print("  示例：xxzhou 运行这个Python脚本")
        print("  示例：xxzhou 执行系统命令 dir")
        print()
        print("系统会自动选择最合适的智能体处理您的任务！")
        return  # 无参数时提示用法，直接退出

    # 拼接所有参数
    input_content = " ".join(sys.argv[1:])

    # 获取当前终端打开的目录路径
    current_dir = os.getcwd()
    current_dir = os.path.abspath(current_dir)

    # 创建智能体工厂和通信器
    factory = AgentFactory()
    from src.agent_communicator import AgentCommunicator

    # 检查是否为复合任务
    if AgentCommunicator.is_compound_task(input_content):
        print("检测到复合任务，开始分解执行...")
        print("="*50)

        try:
            # 执行复合任务
            compound_result = await AgentCommunicator.execute_compound_task(input_content)

            if 'error' in compound_result:
                print(f"复合任务执行失败：{compound_result['error']}")
            else:
                print("\n" + "="*50)
                print("复合任务执行完成！")
                print("="*50)
                print("最终结果：")
                print(compound_result['final_result'])

        except Exception as e:
            print(f"复合任务执行过程中出现错误：{str(e)}")
            print("请检查输入参数或联系开发者")

    else:
        # 单一任务处理
        agent_type = factory.get_agent_by_task_type(input_content)

        print(f"检测到任务类型：{agent_type.replace('_agent', '').upper()}")

        # 创建对应的智能体
        if agent_type == 'master_agent':
            agent = factory.create_master_agent()
            print("使用总协调器处理复杂任务")
        elif agent_type == 'video_agent':
            agent = factory.create_video_agent()
            print("使用视频助手处理")
        elif agent_type == 'image_agent':
            agent = factory.create_image_agent()
            print("使用图片助手处理")
        elif agent_type == 'document_agent':
            agent = factory.create_document_agent()
            print("使用文档助手处理")
        elif agent_type == 'code_agent':
            agent = factory.create_code_agent()
            print("使用代码助手处理")

        # 构建消息
        msg = Msg(
            name="user",
            role="user",
            content=input_content + f"\n当前工作目录：{current_dir}"
        )

        # 执行任务
        try:
            result = await agent(msg)
            print("\n" + "="*50)
            print("执行结果：")
            print("="*50)
            print(result.content[0]["text"])
        except Exception as e:
            print(f"执行过程中出现错误：{str(e)}")
            print("请检查输入参数或联系开发者")

if __name__ == "__main__":
    asyncio.run(main())