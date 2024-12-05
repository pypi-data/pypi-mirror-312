#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Copyright (c) 2024 Baidu, Inc. 
# All rights reserved.
#
# File    : client
# Author  : zhoubohan
# Date    : 2024/11/29
# Time    : 14:18
# Description :
"""
from typing import Iterable, Union

from bceidaas.auth.bce_credentials import BceCredentials
from openai import OpenAI, AsyncOpenAI, Stream
from openai.pagination import SyncPage
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletion,
    ChatCompletionChunk,
)
from openai.types.model import Model


class LMDeployClient(object):
    """
    LMDeployClient is a client for lm deploy
    """

    def __init__(
        self,
        endpoint: str,
        base_url: str = "",
        credentials: BceCredentials = None,
        max_retries: int = 1,
        timeout_in_seconds: int = 30,
        is_async: bool = False,
    ):
        """
        Constructor
        """
        self._endpoint = endpoint
        self._base_url = base_url
        self._credentials = credentials
        self._is_async = is_async

        if self._base_url != "":
            self._endpoint = (
                self._endpoint.rstrip("/") + "/" + self._base_url.strip("/") + "/"
            )

        if is_async:
            self._openai_client = AsyncOpenAI(
                base_url=self._endpoint,
                max_retries=max_retries,
                timeout=timeout_in_seconds,
            )

        else:
            self._openai_client = OpenAI(
                base_url=self._endpoint,
                max_retries=max_retries,
                timeout=timeout_in_seconds,
            )

    async def amodels(self) -> SyncPage[Model]:
        """
        Get models
        """
        return await self._openai_client.models.list()

    def models(self) -> SyncPage[Model]:
        """
        Get models
        """
        return self._openai_client.models.list()

    async def available_amodels(self) -> Union[str, ValueError]:
        """
        Async Get available models
        """
        models = await self.amodels()
        if len(models.data) == 0:
            return ValueError("No available models")

        return models.data[0].id

    def available_models(self) -> Union[str, ValueError]:
        """
        Get available models
        """
        models = self.models()
        if len(models.data) == 0:
            return ValueError("No available models")

        return models.data[0].id

    def chat_completion(
        self,
        messages: Iterable[ChatCompletionMessageParam],
        model: str = "",
        n: int = 1,
        max_completion_tokens: int = 512,
        max_tokens: int = 512,
        temperature: float = 0.7,
        top_p: float = 1.0,
        presence_penalty: float = 0.0,
        frequency_penalty: float = 0.0,
        stream: bool = False,
    ) -> ChatCompletion | Stream[ChatCompletionChunk]:
        """
        Chat completion
        """
        return self._openai_client.chat.completions.create(
            messages=messages,
            model=model,
            n=n,
            max_completion_tokens=max_completion_tokens,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            stream=stream,
        )

    async def chat_acompletion(
        self,
        messages: Iterable[ChatCompletionMessageParam],
        model: str = "",
        n: int = 1,
        max_completion_tokens: int = 512,
        max_tokens: int = 512,
        temperature: float = 0.7,
        top_p: float = 1.0,
        presence_penalty: float = 0.0,
        frequency_penalty: float = 0.0,
        stream: bool = False,
    ) -> ChatCompletion | Stream[ChatCompletionChunk]:
        """
        Async Chat completion
        """
        return await self._openai_client.chat.completions.create(
            messages=messages,
            model=model,
            n=n,
            max_completion_tokens=max_completion_tokens,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            stream=stream,
        )
