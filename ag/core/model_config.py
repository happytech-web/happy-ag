from dataclasses import dataclass

@dataclass
class ModelConfig:
    name: str
    base_url: str
    sys_prompt: dict

class ModelRegistry:
    """模型注册中心（支持扩展）"""
    _registry = {
        'v3': ModelConfig(
            name='deepseek-chat',
            base_url='https://api.deepseek.com',
            sys_prompt={
                'short': "你是一个专业助手，给出比较简要的回答，但是不要牺牲全面性可靠性完整性",
                'long': "作为领域专家，详细分析问题，给出全面精炼且不冗余的回答"
            }
        ),
        'r1': ModelConfig(
            name='deepseek-reasoner',
            base_url='https://api.deepseek.com',
            sys_prompt={
                'short': "你是一个专业助手，给出比较简要的回答，但是不要牺牲全面性可靠性完整性",
                'long': "作为领域专家，详细分析问题，给出全面且不冗余的回答"
            }
        )
    }

    @classmethod
    def get_config(cls, model_type: str) -> ModelConfig:
        if model_type not in cls._registry:
            raise ValueError(f"未注册模型: {model_type}")
        return cls._registry[model_type]
