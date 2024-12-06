# encoding: utf-8
"""
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    created by lane.chang on '07/07/2024'
    comment: 对于异步队列的演示
"""
import asyncio

from laner.model_depends.queue import RedisConfig, Queue, Task


async def put_message(queue: Queue):
    """ 添加队列消息
    """
    count = 1
    while True:
        await asyncio.sleep(1)
        message = {'test': count}
        await queue.put(message=message)
        print(f'加入消息队列 message: {message}')

        if count > 10:
            break
        count += 1

async def read_message(queue: Queue):
    """ 读取队列信息
    """
    async for message in await queue.read(count=1, block=0):
        print(f'read_message 接收到队列消息：{message}')

async def read_message_handel(message=None):
    """ 读取到队列信息进行业务处理
    """
    if not message:
        return

    print(f'read_message_handel 接收到队列消息, 并进行业务处理：{message}')


async def main():
    redis_config = RedisConfig(host='127.0.0.1')
    queue = Queue(redis_config, callback_func=Task(func=read_message_handel))

    tasks = list()
    tasks.append(
        asyncio.create_task(put_message(queue))
    )  # 发送队列消息
    tasks.append(
        asyncio.create_task(read_message(queue))
    )  # 读取队列信息
    tasks.append(
        asyncio.create_task(queue.read_until(exit_condition=lambda x: x['test'] == '8', count=1, block=0))
    )  # 读取队列信息、回调指定函数 并指定退出条件

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    """
    """
    asyncio.run(main())