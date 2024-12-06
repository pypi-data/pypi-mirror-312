import lazyllm
from typing import Any, Dict
from .openaiModule import OpenAIModule
from .glmModule import GLMModule
from .kimiModule import KimiModule
from .sensenovaModule import SenseNovaModule
from .qwenModule import QwenModule
from .doubaoModule import DoubaoModule
from .onlineChatModuleBase import OnlineChatModuleBase

class _ChatModuleMeta(type):

    def __instancecheck__(self, __instance: Any) -> bool:
        if isinstance(__instance, OnlineChatModuleBase):
            return True
        return super().__instancecheck__(__instance)


class OnlineChatModule(metaclass=_ChatModuleMeta):
    """Used to manage and create access modules for large model platforms currently available on the market. Currently, it supports openai, sensenova, glm, kimi, qwen and doubao (since the platform is not currently being developed for individual users, access is not currently supported). For how to obtain the platform's API key, please visit [Getting Started](/#platform)

Args:
    model (str): Specify the model to access, default is ``gpt-3.5-turbo(openai)`` / ``SenseChat-5(sensenova)`` / ``glm-4(glm)`` / ``moonshot-v1-8k(kimi)`` / ``qwen-plus(qwen)`` .
    source (str): Specify the type of module to create. Options include  ``openai`` /  ``sensenova`` /  ``glm`` /  ``kimi`` /  ``qwen`` / ``doubao (not yet supported)`` .
    base_url (str): Specify the base link of the platform to be accessed. The default is the official link.
    system_prompt (str): Specify the requested system prompt. The default is the official system prompt.
    stream (bool): Whether to request and output in streaming mode, default is streaming.
    return_trace (bool): Whether to record the results in trace, default is False.      


Examples:
    >>> import lazyllm
    >>> from functools import partial
    >>> m = lazyllm.OnlineChatModule(source="sensenova", stream=True)
    >>> query = "Hello!"
    >>> with lazyllm.ThreadPoolExecutor(1) as executor:
    ...     future = executor.submit(partial(m, llm_chat_history=[]), query)
    ...     while True:
    ...         if value := lazyllm.FileSystemQueue().dequeue():
    ...             print(f"output: {''.join(value)}")
    ...         elif future.done():
    ...             break
    ...     print(f"ret: {future.result()}")
    ...
    output: Hello
    output: ! How can I assist you today?
    ret: Hello! How can I assist you today?
    """
    MODELS = {'openai': OpenAIModule,
              'sensenova': SenseNovaModule,
              'glm': GLMModule,
              'kimi': KimiModule,
              'qwen': QwenModule,
              'doubao': DoubaoModule}

    @staticmethod
    def _encapsulate_parameters(base_url: str,
                                model: str,
                                stream: bool,
                                return_trace: bool,
                                **kwargs) -> Dict[str, Any]:
        params = {"stream": stream, "return_trace": return_trace}
        if base_url is not None:
            params['base_url'] = base_url
        if model is not None:
            params['model'] = model
        params.update(kwargs)

        return params

    def __new__(self,
                model: str = None,
                source: str = None,
                base_url: str = None,
                stream: bool = True,
                return_trace: bool = False,
                **kwargs):
        if model in OnlineChatModule.MODELS.keys() and source is None: source, model = model, source

        params = OnlineChatModule._encapsulate_parameters(base_url, model, stream, return_trace, **kwargs)

        if source is None:
            if "api_key" in kwargs and kwargs["api_key"]:
                raise ValueError("No source is given but an api_key is provided.")
            for source in OnlineChatModule.MODELS.keys():
                if lazyllm.config[f'{source}_api_key']: break
            else:
                raise KeyError(f"No api_key is configured for any of the models {OnlineChatModule.MODELS.keys()}.")

        assert source in OnlineChatModule.MODELS.keys(), f"Unsupported source: {source}"
        return OnlineChatModule.MODELS[source](**params)
