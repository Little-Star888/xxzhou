"""
智能体间通信管理器
"""
from agentscope.message import Msg
import re

class AgentCommunicator:
    """智能体间通信管理器"""

    @staticmethod
    def is_compound_task(task_description):
        """判断是否为复合任务"""
        compound_patterns = [
            r'下载.*并.*提取',  # 下载...并...提取
            r'生成.*并.*分析',  # 生成...并...分析
            r'下载.*然后.*',    # 下载...然后...
            r'.*并.*',          # 包含"并"字的复合任务
        ]

        task_lower = task_description.lower()
        for pattern in compound_patterns:
            if re.search(pattern, task_lower, re.IGNORECASE):
                return True
        return False

    @staticmethod
    def decompose_video_task(task_description):
        """分解视频相关复合任务"""
        steps = []

        # 检查是否包含下载和提取
        if ('下载' in task_description or 'download' in task_description.lower()) and \
           ('提取' in task_description or '文案' in task_description or 'transcribe' in task_description.lower()):

            # 提取URL信息
            url_pattern = r'https?://[^\s]+'
            url_match = re.search(url_pattern, task_description)
            url = url_match.group(0) if url_match else None

            if url:
                # 第一步：下载视频
                steps.append({
                    'step': 1,
                    'agent': 'video_agent',
                    'task': f'下载视频：{url}',
                    'description': '下载视频文件'
                })

                # 第二步：提取文案（将在后续步骤中获取文件路径）
                steps.append({
                    'step': 2,
                    'agent': 'video_agent',
                    'task': '提取已下载视频的文案',
                    'description': '提取视频文案',
                    'depends_on': 0  # 依赖第一步的结果
                })

        return steps

    @staticmethod
    def decompose_image_task(task_description):
        """分解图片相关复合任务"""
        steps = []

        # 检查是否包含生成和分析
        if ('生成' in task_description or 'create' in task_description.lower()) and \
           ('分析' in task_description or '识别' in task_description or 'read' in task_description.lower()):

            # 提取生成描述
            generate_pattern = r'生成(.+?)(?:并|然后|再)'
            generate_match = re.search(generate_pattern, task_description)
            if generate_match:
                description = generate_match.group(1).strip()

                # 第一步：生成图片
                steps.append({
                    'step': 1,
                    'agent': 'image_agent',
                    'task': f'生成图片：{description}',
                    'description': '生成图片文件'
                })

                # 第二步：分析图片
                steps.append({
                    'step': 2,
                    'agent': 'image_agent',
                    'task': '分析已生成图片的内容',
                    'description': '分析图片内容',
                    'depends_on': 0  # 依赖第一步的结果
                })

        return steps

    @staticmethod
    async def execute_compound_task(task_description):
        """执行复合任务"""
        results = []

        # 识别任务类型并分解
        if '视频' in task_description or 'video' in task_description.lower():
            steps = AgentCommunicator.decompose_video_task(task_description)
        elif '图片' in task_description or 'image' in task_description.lower():
            steps = AgentCommunicator.decompose_image_task(task_description)
        else:
            return {"error": "无法识别的复合任务类型"}

        if not steps:
            return {"error": "无法分解任务步骤"}

        context = None

        for step_info in steps:
            step_num = step_info['step']
            agent_name = step_info['agent']
            task = step_info['task']
            description = step_info['description']

            print(f"执行步骤 {step_num}: {description}")

            # 如果有上下文（前一步的结果），添加到任务中
            full_task = task
            if context and 'depends_on' in step_info:
                # 从上下文提取文件路径
                path_match = re.search(r'文件路径：([^\n]+)', context)
                if path_match:
                    file_path = path_match.group(1).strip()
                    if step_num == 2:  # 第二步通常是处理已下载/生成的文件
                        if '提取' in task or 'transcribe' in task.lower():
                            full_task = f'提取视频文案：{file_path}'
                        elif '分析' in task or 'read' in task.lower():
                            full_task = f'分析图片：{file_path}'

            # 执行步骤
            step_result = await AgentCommunicator.call_sub_agent(agent_name, full_task, context)
            results.append(step_result)

            # 更新上下文为当前步骤的结果
            context = step_result['result']

        return {
            'compound_task': True,
            'steps': results,
            'final_result': context
        }

    @staticmethod
    async def call_sub_agent(agent_name, task_description, context=None):
        """调用子智能体处理任务"""
        # 延迟导入避免循环导入
        from src.agent_factory import AgentFactory
        factory = AgentFactory()
        agent = factory.create_agent_by_name(agent_name)

        # 构建任务消息
        full_task = f"请处理以下任务：{task_description}"
        if context:
            full_task += f"\n\n上下文信息：{context}"

        msg = Msg(
            name="master_agent",
            role="user",
            content=full_task
        )

        # 调用子智能体
        result = await agent(msg)

        return {
            'agent': agent_name,
            'task': task_description,
            'result': result.content[0]['text'] if result.content else '',
            'status': 'completed'
        }

    @staticmethod
    def format_agent_response(agent_name, response_data):
        """格式化智能体响应"""
        agent_names = {
            'video_agent': '视频助手',
            'image_agent': '图片助手',
            'document_agent': '文档助手',
            'code_agent': '代码助手',
            'master_agent': '总协调器'
        }

        friendly_name = agent_names.get(agent_name, agent_name)
        return f"[{friendly_name}] {response_data['result']}"
