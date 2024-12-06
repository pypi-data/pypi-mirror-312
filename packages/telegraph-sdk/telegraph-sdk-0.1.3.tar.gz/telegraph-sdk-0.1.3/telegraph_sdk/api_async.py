import asyncio
import logging

import httpx

logger = logging.getLogger(__name__)

class Telegraph:
    """
    Telegraph API客户端，用于创建用户和发布文章。
    """

    BASE_URL = 'https://api.telegra.ph'

    def __init__(self, short_name, author_name, author_url, proxy=None, access_token=None):
        self.session = httpx.AsyncClient(
            proxy=proxy,
            timeout=httpx.Timeout(10.0, connect=2, read=10, write=10),
            base_url=self.BASE_URL,
        )
        self.short_name = short_name
        self.author_name = author_name
        self.author_url = author_url
        self.access_token = access_token

    async def __request(self, endpoint, method='POST', retries=3, **kwargs):
        """
        通用请求方法，支持异步请求。
        :param endpoint: API端点路径。
        :param method: HTTP方法。
        :param retries: 重试次数。
        :param kwargs: 其他参数。
        :return: 响应JSON。
        """
        url = f"{self.BASE_URL}/{endpoint}"

        for attempt in range(retries):
            try:
                response = await self.session.request(method=method, url=url, **kwargs)
                response.raise_for_status()
                return response.json()
            except (httpx.RequestError, httpx.HTTPStatusError) as e:
                logger.warning(f"Request error on attempt {attempt + 1}/{retries}: {e}")
                if attempt == retries - 1:
                    raise

    async def init_user(self):
        """
        初始化Telegraph用户。
        """
        if self.access_token:
            return

        response = await self.__request(
            endpoint='createAccount',
            json={
                'short_name': self.short_name,
                'author_name': self.author_name,
                'author_url': self.author_url,
            }
        )

        if response.get('ok'):
            self.access_token = response['result']['access_token']

    async def create_page(self, title, content, author_name=None, author_url=None):
        """
        创建文章页面。
        :param title: 文章标题。
        :param content: 文章内容，支持HTML格式。
        :param author_name: 作者名称（可选）。
        :param author_url: 作者URL（可选）。
        :return: 文章URL或空字符串。
        """
        await self.init_user()

        payload = {
            "access_token": self.access_token,
            "title": title,
            "author_name": author_name or self.author_name,
            "author_url": author_url or self.author_url,
            "content": [{"tag": "p", "children": [content]}],
            "return_content": True
        }

        response = await self.__request(endpoint='createPage', json=payload)

        if response.get("ok"):
            return response["result"].get("url", "")
        return ''

    async def get_views(self, path):
        """
        获取文章的查看次数。
        :param path: 文章路径。
        :return: 视图数据。
        """
        await self.init_user()

        response = await self.__request(
            endpoint='getViews',
            json={'path': path}
        )
        return response

    async def get_page_list(self):
        """
        获取用户的文章列表。
        :return: 文章列表数据。
        """
        await self.init_user()

        response = await self.__request(
            endpoint='getPageList',
            json={"access_token": self.access_token}
        )
        return response

    async def close(self):
        """
        关闭HTTP客户端会话。
        """
        await self.session.aclose()


if __name__ == '__main__':
    async def main():
        tg = Telegraph(
            short_name='open-fin',
            author_name='ov',
            author_url='',
            proxy='http://127.0.0.1:51623'
        )

        try:
            page_url = await tg.create_page(
                title='Test Page',
                content='This is a test content.',
                author_name='oovv',
                author_url='https://telegra.ph/test-11-30-6'
            )
            print(f"Page created: {page_url}")
        finally:
            await tg.close()


    asyncio.run(main())
