"""
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    created by lane.chang on '04/07/2022'
    comment: 异步队列(redis)
"""
import asyncio
from uuid import uuid4
from typing import Callable, Dict, Optional

import aioredis
from aioredis.client import FieldT, EncodableT

from pydantic import Field
from laner.pydantic import BaseModel


class Task(BaseModel):
    """
    """
    func: Callable = Field(..., title='处理任务')
    args: list = Field([], title='参数列表')
    kwargs: dict = Field({}, title='字典参数列表')

    def __init__(self, *args, **kwargs):
        """
        """
        super(BaseModel, self).__init__(*args, **kwargs)
        if 'message' in self.kwargs and self.kwargs['message'] is not None:
            raise Exception('key value conflict: message')

    async def exec(self):
        """ 执行
        :return:
        """
        if asyncio.iscoroutinefunction(self.func):
            await self.func(*self.args, **self.kwargs)
        else:
            self.func(*self.args, **self.kwargs)


class RedisConfig(BaseModel):
    """ redis设置
    """
    host: str = Field(..., title='redis host')
    user: str = Field('', title='redis user')
    password: str = Field('', title='redis password')
    db: int = Field(0, title='redis db')

    def __str__(self):
        """
        :return:
        """
        return f"redis://{self.user}:{self.password}@{self.host}/"


class Queue:
    """ 队列(异步)
    """
    def __init__(self, redis_config: RedisConfig, callback_func: Task = None):
        """
        :param redis_config: redis配置
        """
        self.id = f'queue:{str(uuid4()).replace("-", "")}'
        self.callback_func = callback_func  # 回调函数
        self.client = aioredis.from_url(str(redis_config))

    async def put(self, message: Dict[FieldT, EncodableT], max_len: Optional[int] = None, approximate: bool = True):
        """ 添加消息队列
        :param message:
        :param max_len:
        :param approximate:
        :return:
        """
        await self.client.xadd(name=self.id, id="*", fields=message, maxlen=max_len, approximate=approximate)


    async def _read(self, count: Optional[int] = None, block: Optional[int] = None):
        """
        :param count:
        :param block:
        :return:
        """
        try:
            while True:
                response = await self.client.xread(streams={self.id: '0-0'}, count=count, block=block)
                if not response:
                    continue

                for stream, messages in response:
                    for message in messages:
                        message_id = message[0]
                        message_content = message[1]
                        message_content = {k.decode('utf-8'): v.decode('utf-8') for k, v in message_content.items()}
                        if not message_content:
                            continue

                        yield message_content

                        await self.client.xdel(self.id, message_id)
        finally:
            if await self.client.exists(self.id):
                await self.client.delete(self.id)


    async def read(self, count: Optional[int] = None, block: Optional[int] = None):
        """ 读取消息队列
        :param count:
        :param block:
        :return:
        """
        return self._read(count, block)


    async def read_until(self, exit_condition: Callable, count: Optional[int] = None, block: Optional[int] = None):
        """
        :param exit_condition: 退出条件
        :param count:
        :param block:
        :return:
        """
        try:
            async for message in self._read(count, block):
                if exit_condition(message):
                    break

                if self.callback_func is not None:
                    self.callback_func.kwargs.update({'message': message})
                    await self.callback_func.exec()  # 执行回调
        except Exception as ex:
            raise ex
        finally:
            if await self.client.exists(self.id):
                await self.client.delete(self.id)

