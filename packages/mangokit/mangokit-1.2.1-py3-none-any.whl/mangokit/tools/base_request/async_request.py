# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description:
# @Time   : 2024-07-26 上午10:03
# @Author : 毛鹏
import asyncio
import time

import aiohttp

from mangokit.models.models import ResponseModel


# import warnings
# warnings.simplefilter('ignore', category=UserWarning)


class AsyncRequests:
    proxies: dict = None
    timeout: int = None

    @classmethod
    async def request(cls, method, url, headers=None, **kwargs) -> ResponseModel:
        """
        处理请求的数据，写入到request对象中
        @return:
        """
        async with aiohttp.ClientSession() as session:
            s = time.time()
            async with session.request(
                    method=method,
                    url=url,
                    headers=headers or {},
                    proxy=cls.proxies.get("http") if cls.proxies else None,
                    timeout=cls.timeout if cls.timeout is not None else aiohttp.ClientTimeout(total=None),
                    **kwargs
            ) as response:
                response_text = await response.text()
                response_json = await response.json() if response.content_type == 'application/json' else None

                return ResponseModel(
                    response_time=time.time() - s,
                    headers=dict(response.headers),
                    status_code=response.status,
                    text=response_text,
                    json_data=response_json
                )

    @classmethod
    async def get(cls, url, headers=None, **kwargs) -> ResponseModel:
        return await cls.request('GET', url, headers, **kwargs)

    @classmethod
    async def post(cls, url, headers=None, **kwargs) -> ResponseModel:
        return await cls.request('POST', url, headers, **kwargs)

    @classmethod
    async def delete(cls, url, headers=None, **kwargs) -> ResponseModel:
        return await cls.request('DELETE', url, headers, **kwargs)

    @classmethod
    async def put(cls, url, headers=None, **kwargs) -> ResponseModel:
        return await cls.request('PUT', url, headers, **kwargs)


async_requests = AsyncRequests


# 示例用法
async def main():
    response: ResponseModel = await async_requests.post('https://www.wanandroid.com/user/login',
                                                        data={
                                                            "password": "729164035",
                                                            "username": "maopeng"
                                                        })

    print(response.json_data)


# 运行示例
if __name__ == '__main__':
    asyncio.run(main())
    """
    import aiohttp
import asyncio

async def upload_file(url, file_path):
    # 创建一个 aiohttp session
    async with aiohttp.ClientSession() as session:
        # 打开文件并发送 POST 请求
        with open(file_path, 'rb') as file:
            # 使用 multipart/form-data 发送文件
            data = aiohttp.FormData()
            data.add_field('file', file, filename=file_path)

            async with session.post(url, data=data) as response:
                # 处理响应
                if response.status == 200:
                    print("文件上传成功！")
                    response_data = await response.json()
                    print(response_data)
                else:
                    print(f"文件上传失败，状态码: {response.status}")

# 示例使用
async def main():
    url = 'http://your-upload-url.com/upload'  # 替换为你的上传 URL
    file_path = 'path/to/your/file.txt'  # 替换为你的文件路径
    await upload_file(url, file_path)

# 运行主函数
if __name__ == '__main__':
    asyncio.run(main())

"""
