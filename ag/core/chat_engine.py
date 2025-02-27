import os
from typing import List, Dict
from dotenv import load_dotenv
from .model_config import ModelRegistry
from openai import OpenAI


class ChatEngine:
    """对话核心引擎"""
    def __init__(self, model_type: str = 'v3', long_mode: bool = False):
        load_dotenv()
        config = ModelRegistry.get_config(model_type)
        
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url=config.base_url
        )
        self.model_name = config.name
        self.system_prompt = config.sys_prompt['long'] if long_mode else config.sys_prompt['short']
        self.history: List[Dict] = []
        self.is_reasoner = "reasoner" in self.model_name.lower()

    def _build_messages(self, prompt: str) -> List[Dict]:
        """动态构建消息队列（保证单系统消息）"""
        messages = [msg for msg in self.history if msg["role"] != "system"]
        return [
            {"role": "system", "content": self.system_prompt},
            *messages,
            {"role": "user", "content": f"{prompt}" if self.is_reasoner else prompt}
        ]

    def generate_stream_response(self, prompt: str):
        """流式响应生成器"""
        # self.history.append({"role": "user", "content": prompt})
        cur_messages = self._build_messages(prompt)
        # print(cur_messages)
        
        stream = self.client.chat.completions.create(
            model=self.model_name,
            messages=cur_messages,
            stream=True
        )
        
        full_content = []
        for chunk in stream:
            # if delta := chunk.choices[0].delta.content:
            #     yield delta
            #     full_content.append(delta)if isinstance(chunk, ChatCompletionChunk):
            # 优先获取推理内容（网页1）
            reasoning_delta = getattr(chunk.choices[0].delta, "reasoning_content", "")
            content_delta = chunk.choices[0].delta.content or ""

            # R1模型逐字输出推理内容（网页1）
            if self.is_reasoner:
                if reasoning_delta:
                    # 这里只打印不yield了，否则会把思考过程也发过去了，浪费token
                    print(reasoning_delta, end="", flush=True)
                if content_delta:
                    yield content_delta
                    full_content.append(content_delta)
            # V3模型常规输出（网页11）
            elif not self.is_reasoner and content_delta: 
                yield content_delta
                full_content.append(content_delta)
        
        self._update_history(prompt, full_content)


    def _update_history(self, user_prompt: str, assistant_response: List[str]):
        """更新对话历史记录"""
        self.history.append({"role": "user", "content": user_prompt})
        self.history.append({
            "role": "assistant",
            "content": "".join(assistant_response)
        })
