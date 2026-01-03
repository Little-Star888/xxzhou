"""
智能体间通信管理器
"""
from agentscope.message import Msg

class AgentCommunicator:
    """智能体间通信管理器"""

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
            'video_agent': '🎬 视频助手',
            'image_agent': '🖼️ 图片助手',
            'document_agent': '📄 文档助手',
            'code_agent': '💻 代码助手',
            'master_agent': '🎯 总协调器'
        }

        friendly_name = agent_names.get(agent_name, agent_name)
        return f"[{friendly_name}] {response_data['result']}"
