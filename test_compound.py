#!/usr/bin/env python3
from src.agent_communicator import AgentCommunicator

# 测试任务分解
video_task = '下载这个视频 https://www.bilibili.com/video/BV1fFiwBoEAw 并提取文案'
print('视频复合任务分解测试：')
steps = AgentCommunicator.decompose_video_task(video_task)
for step in steps:
    print(f'步骤 {step["step"]}: {step["description"]}')
    print(f'  智能体: {step["agent"]}')
    print(f'  任务: {step["task"]}')
    print()

image_task = '生成一张美丽的风景图片并分析内容'
print('图片复合任务分解测试：')
steps = AgentCommunicator.decompose_image_task(image_task)
for step in steps:
    print(f'步骤 {step["step"]}: {step["description"]}')
    print(f'  智能体: {step["agent"]}')
    print(f'  任务: {step["task"]}')
    print()
