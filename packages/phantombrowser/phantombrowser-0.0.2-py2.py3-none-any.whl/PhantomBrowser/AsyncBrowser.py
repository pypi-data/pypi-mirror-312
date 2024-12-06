# -*-coding:utf8;-*-
from urllib.parse import urlencode
import aiohttp
import aiofiles
import json as jsonpy
import os
from typing import Optional, Union, Dict, Any, List


class AsyncBrowser:
    """
    Phantomjs cloud api wrapper.
    author: guangrei.
    """

    def __init__(self, apikey: Optional[str] = None) -> None:
        if apikey is None:
            apikey = os.environ.get(
                "PHANTOMJSCLOUD.COM_APIKEY", "a-demo-key-with-low-quota-per-ip-address"
            )
        userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Guangrei/2024.04.21 Chrome/124.0.0.0 Safari/537.36"
        # settings https://phantomjscloud.com/docs/http-api/interfaces/ipagerequest.html
        self.pageRequest: Dict[str, Any] = {}
        self.endpoints: str = (
            "https://phantomjscloud.com/api/browser/v2/" + apikey + "/"
        )
        self.response: Optional[bytes] = None
        self.disableJavascript: bool = False
        self.customHeaders: Dict[str, str] = {}
        self.urlSettings: Dict[str, Any] = {}
        self.requestSettings: Dict[str, Any] = {"doneWhen": [{"event": "domReady"}]}
        self.renderSettings: Dict[str, Any] = {}
        self.userAgent: str = userAgent
        self.cookies: List[str] = []
        self._session: aiohttp.ClientSession = aiohttp.ClientSession()

    async def _magicRender(self, type: str) -> None:
        if type == "html":
            self.pageRequest["renderType"] = "html"
            self.requestSettings["ignoreImages"] = True
        elif type == "pdf":
            self.pageRequest["renderType"] = "pdf"
            self.requestSettings["ignoreImages"] = False
        elif type == "plainText":
            self.pageRequest["renderType"] = "plainText"
            self.requestSettings["ignoreImages"] = True
        elif type == "png":
            self.pageRequest["renderType"] = "png"
            self.requestSettings["ignoreImages"] = False
        elif type == "jpg":
            self.pageRequest["renderType"] = "jpg"
            self.requestSettings["ignoreImages"] = False
        elif type == "jpeg":
            self.pageRequest["renderType"] = "jpeg"
            self.requestSettings["ignoreImages"] = False
        else:
            raise ValueError("Not supported!")

    async def _evaluate(self) -> aiohttp.ClientResponse:
        self.requestSettings["disableJavascript"] = self.disableJavascript
        self.requestSettings["userAgent"] = self.userAgent
        self.requestSettings["cookies"] = self.cookies
        self.pageRequest["urlSettings"] = self.urlSettings
        self.pageRequest["renderSettings"] = self.renderSettings
        self.pageRequest["requestSettings"] = self.requestSettings
        async with self._session.post(
            self.endpoints, json=self.pageRequest
        ) as response:
            content = await response.read()
        self.response = content
        return response

    async def post(
        self,
        url: str,
        json: Optional[str] = None,
        data: Optional[Union[str, Dict[str, str]]] = None,
        encoding: Optional[str] = None,
        headers: Dict[str, str] = {},
        render: str = "html",
        json_output: bool = False,
    ) -> aiohttp.ClientResponse:
        await self._magicRender(render)
        self.pageRequest["outputAsJson"] = json_output
        self.pageRequest["url"] = url
        self.urlSettings["operation"] = "POST"
        if json is not None:
            self.urlSettings["data"] = jsonpy.dumps(json)
            self.urlSettings["contentType"] = "application/json"
        elif json is None and data is not None:
            if isinstance(data, dict):
                self.urlSettings["data"] = urlencode(data)
                self.urlSettings["contentType"] = "application/x-www-form-urlencoded"
            elif isinstance(data, str):
                self.urlSettings["data"] = data
                self.urlSettings["contentType"] = "text/plain"
            else:
                raise TypeError
        self.urlSettings["encoding"] = encoding
        self.urlSettings["headers"] = headers
        return await self._evaluate()

    async def get(
        self,
        url: str,
        encoding: Optional[str] = None,
        headers: Dict[str, str] = {},
        render: str = "html",
        json_output: bool = False,
    ) -> aiohttp.ClientResponse:
        await self._magicRender(render)
        self.pageRequest["outputAsJson"] = json_output
        self.pageRequest["url"] = url
        self.urlSettings["operation"] = "GET"
        self.urlSettings["encoding"] = encoding
        self.urlSettings["headers"] = headers
        return await self._evaluate()

    async def put(
        self,
        url: str,
        encoding: Optional[str] = None,
        headers: Dict[str, str] = {},
        render: str = "html",
        json_output: bool = False,
    ) -> aiohttp.ClientResponse:
        await self._magicRender(render)
        self.pageRequest["outputAsJson"] = json_output
        self.pageRequest["url"] = url
        self.urlSettings["operation"] = "PUT"
        self.urlSettings["encoding"] = encoding
        self.urlSettings["headers"] = headers
        return await self._evaluate()

    async def patch(
        self,
        url: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Union[str, Dict[str, str]]] = None,
        encoding: Optional[str] = None,
        headers: Dict[str, str] = {},
        render: str = "html",
        json_output: bool = False,
    ) -> aiohttp.ClientResponse:
        await self._magicRender(render)
        self.pageRequest["outputAsJson"] = json_output
        self.pageRequest["url"] = url
        self.urlSettings["operation"] = "PATCH"
        if json is not None:
            self.urlSettings["data"] = jsonpy.dumps(json)
            self.urlSettings["contentType"] = "application/json"
        elif json is None and data is not None:
            if isinstance(data, dict):
                self.urlSettings["data"] = urlencode(data)
                self.urlSettings["contentType"] = "application/x-www-form-urlencoded"
            elif isinstance(data, str):
                self.urlSettings["data"] = data
                self.urlSettings["contentType"] = "text/plain"
            else:
                raise TypeError
        self.urlSettings["encoding"] = encoding
        self.urlSettings["headers"] = headers
        return await self._evaluate()

    async def option(
        self,
        url: str,
        encoding: Optional[str] = None,
        headers: Dict[str, str] = {},
        render: str = "html",
        json_output: bool = False,
    ) -> aiohttp.ClientResponse:
        await self._magicRender(render)
        self.pageRequest["outputAsJson"] = json_output
        self.pageRequest["url"] = url
        self.urlSettings["operation"] = "OPTION"
        self.urlSettings["encoding"] = encoding
        self.urlSettings["headers"] = headers
        return await self._evaluate()

    async def delete(
        self,
        url: str,
        encoding: Optional[str] = None,
        headers: Dict[str, str] = {},
        render: str = "html",
        json_output: bool = False,
    ) -> aiohttp.ClientResponse:
        await self._magicRender(render)
        self.pageRequest["outputAsJson"] = json_output
        self.pageRequest["url"] = url
        self.urlSettings["operation"] = "DELETE"
        self.urlSettings["encoding"] = encoding
        self.urlSettings["headers"] = headers
        return await self._evaluate()

    async def saveAs(self, path: str, content: Optional[bytes] = None) -> bool:
        if content is not None:
            async with aiofiles.open(path, mode="wb") as f:
                await f.write(content)
                return True
        if self.response is not None:
            async with aiofiles.open(path, mode="wb") as f:
                await f.write(self.response)
                return True
        else:
            return False

    async def close(self) -> None:
        await self._session.close()
