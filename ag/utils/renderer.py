import subprocess

def render_glow(content: str, long_mode: bool):
    """使用glow渲染Markdown（支持Unix管道[14](@ref)）"""
    try:
        cmd_args = ['glow', '-']
        if long_mode:
            cmd_args.insert(1, '-p')
        with subprocess.Popen(
                ['glow', '-'],
                stdin=subprocess.PIPE,
                text=True
        ) as proc:
            proc.communicate(input=content)
    except (FileNotFoundError, subprocess.CalledProcessError):
        return content  # 回退原始内容

