from datetime import datetime
from pathlib import Path

class HistoryManager:
    """对话历史管理器"""
    def __init__(self):
        self.conversation = []
        self._auto_save_counter = 0

    def add_exchange(self, prompt: str, response: str):
        self.conversation.extend([
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": response}
        ])
        self._auto_save_counter += 1
        
        # 每5次交互自动保存
        if self._auto_save_counter >= 5:
            self.auto_save()

    def auto_save(self):
        """智能自动保存（符合Unix哲学）"""
        path = Path(f"ag_auto_{datetime.now().strftime('%H%M')}.md")
        if path.exists():
            path = path.with_name(f"{path.stem}_bak{path.suffix}")
        return self.save_markdown(path)

    def save_markdown(self, path: Path = None) -> Path:
        """安全保存到文件系统"""
        path = path or Path(f"ag_{datetime.now().strftime('%Y%m%d%H%M')}.md")
        path = path.resolve()
        
        content = "# AG对话记录\n\n" + "\n\n".join(
            f"**{msg['role']}**: {msg['content']}" 
            for msg in self.conversation
        )
        
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return path
