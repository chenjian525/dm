import os.path
from tornado.options import options, define

try:
    from tornado.util import exec_in
except ImportError:
    exec_in = lambda *args: None


def load_dev_options():
    conf = {}

    with open(os.path.join(os.path.dirname(__file__), 'dev.py'), encoding='UTF-8') as f:
        exec_in(f.read(), conf, conf)
    for name in conf:
        if name != '__builtins__':
            define(name, conf[name])


def load_app_options():
    load_dev_options()
    remaining = options.parse_command_line(final=False)  # 读取命令行参数
    if options.mode == 'dev':
        options.run_parse_callbacks()
    else:
        options.parse_config_file(os.path.join(os.path.dirname(__file__), options.mode + '.py'), final=True)

    return remaining
