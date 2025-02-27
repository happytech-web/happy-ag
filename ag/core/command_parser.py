import re
from typing import Tuple

class CommandParser:
    """类Vim命令解析器"""
    SAVE_PATTERN = re.compile(r"^:w(!?)\s*(.*)$")
    
    @classmethod
    def parse_save(cls, cmd: str) -> Tuple[bool, str]:
        """解析保存命令
        :return: (是否强制覆盖, 文件名)
        """
        match = cls.SAVE_PATTERN.match(cmd)
        if not match:
            return None
            
        force, filename = match.groups()
        return (force == '!', filename.strip() or None)
