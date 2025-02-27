import argparse
from datetime import datetime
from pathlib import Path
from core.chat_engine import ChatEngine
from core.history_manager import HistoryManager
from core.command_parser import CommandParser
from utils import renderer

class CLIApp:
    """命令行应用主入口"""
    
    def __init__(self):
        self.parser = self._build_parser()
        self.args = self.parser.parse_args()
        self.engine = self._init_engine()
        self.history = HistoryManager()
        self.saver = CommandParser()

    def _build_parser(self) -> argparse.ArgumentParser:
        """构建命令行参数解析器"""
        parser = argparse.ArgumentParser(
            prog='ag',
            description='happytech AI agent',
            epilog='usage:\n  ag -m r1 "解释量子计算"\n  ag -l > output.md'
        )
        
        parser.add_argument('prompt', nargs='?', help='直接输入问题进入快速模式')
        parser.add_argument('-m', '--model', choices=['v3', 'r1'], default='v3',
                          help='choose model (v3/r1)')
        parser.add_argument('-l', '--long', action='store_true',
                          help='reply in detail')
        parser.add_argument('-o', '--output', type=Path,
                          help='give a output path')
        return parser

    def _init_engine(self) -> ChatEngine:
        """初始化聊天引擎（参考ModelConfig设计）"""
        try:
            return ChatEngine(
                model_type=self.args.model,
                long_mode=self.args.long
            )
        except ValueError as e:
            print(f"🚨 模型初始化失败: {str(e)}")
            exit(1)

    def _interactive_loop(self):
        """交互模式主循环"""
        print(f"👽 进入交互模式 | 模型: {self.args.model.upper()}")
        while True:
            try:
                prompt = input("\n🔵 输入问题（:q退出）> ").strip()
                if not prompt:
                    continue
                
                # 处理命令
                if prompt.startswith(':'):
                    self._process_command(prompt)
                    continue
                
                # 生成响应
                response = self._generate_response(prompt)
                print(f"\n🤖 响应:")
                print(renderer.render_glow(response, self.args.long))
                
                # 自动保存提示
                if len(self.history.conversation) % 3 == 0:
                    print("💡 输入':save'保存当前对话")

            except KeyboardInterrupt:
                print("\n🟠 输入中断，输入':q'退出")

    def _generate_response(self, prompt: str) -> str:
        """生成并记录响应"""
        full_response = []
        print("\n🤔 thinking...")
        
        try:
            for chunk in self.engine.generate_stream_response(prompt):
                print(chunk, end='', flush=True)
                full_response.append(chunk)
        except Exception as e:
            print(f"\n🔴 生成失败: {str(e)}")
            return ""
        
        response = ''.join(full_response)
        self.history.add_exchange(prompt, response)
        return response

    def _process_command(self, cmd: str):
        """处理系统命令（参考CommandParser设计）"""
        if cmd in (':q', ':quit'):
            self._exit_sequence()
        elif cmd.startswith(':save'):
            self._save_dialog(cmd)
        else:
            print(f"🟡 未知命令: {cmd}")

    def _save_dialog(self, cmd: str):
        """处理保存逻辑"""
        save_cmd = CommandParser.parse_save(cmd)
        if not save_cmd:
            print("🔴 保存命令格式错误，使用':save [filename]'")
            return
        
        try:
            path = self.history.save_markdown(
                filename=save_cmd[1] or f"dialog_{datetime.now().strftime('%Y%m%d%H%M')}.md"
            )
            print(f"✅ 已保存至: {path}")
        except Exception as e:
            print(f"🔴 保存失败: {str(e)}")

    def _exit_sequence(self):
        """退出处理流程"""
        if self.history.conversation:
            choice = input("退出前是否保存对话？(y/n) ").lower()
            if choice == 'y':
                self._save_dialog(':save')
        print("🟢 会话结束")
        exit(0)

    def run(self):
        """应用主入口"""
        if self.args.prompt:
            response = self._generate_response(self.args.prompt)
            if self.args.output:
                self.history.save_markdown(self.args.output)
            exit(0)
            
        self._interactive_loop()

if __name__ == '__main__':
    CLIApp().run()
