import argparse
import asyncio
import importlib
import logging
import os
import pathlib
import re
import signal
import sys
import threading
import traceback

import voxe
import tornado
import tornado.websocket

from pyrpcd.share import managers


running_state = True


def sig_handler(sig, frame):
    global running_state
    running_state = False
    logging.debug("> Recycle done! exiting ...")
    exit(0)


signal.signal(signal.SIGINT, sig_handler)


def self_import(pth: str):
    pth = os.path.normpath(pth)
    _pth = pathlib.Path(pth)
    if _pth.is_absolute():
        if len(list(filter(lambda p: os.path.normpath(p) == pth, sys.path))) == 0:
            sys.path.append(os.path.dirname(pth))
    if _pth.is_file() and pth.lower().endswith('.py'):
        module_name = _pth.name.split('.')[0]
    elif _pth.is_dir():
        module_name = _pth.name
    else:
        raise Exception('Not standard python module')
    return importlib.import_module(module_name)


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=8080, help='default: 8080, port of server')
    parser.add_argument('--prefix', type=str, default='/', help='default: /, prefix of url')
    parser.add_argument('--static_path', type=str, default='www', help='default: www, static resources accessing')
    parser.add_argument('--cache_path', type=str, default='cache', help='default: cache, cache directory for partition upload')
    parser.add_argument('--log_level', type=str, default='debug', choices=['debug', 'info', 'warning', 'error'], help='default: debug, set log level')
    parser.add_argument('modules', nargs='+')
    return parser.parse_args(args)


def encode_filename(s: str) -> str:
    return "".join(['%02X' % e for e in s.encode('utf-8')])


def decode_filename(s: str) -> str:
    return b''.join([bytes.fromhex(s[i * 2:i * 2 + 2]) for i in range(len(s) // 2)]).decode('utf-8')


def save_partition(filename: str, section: str, data: bytes, cache_path: str):
    cache_path = pathlib.Path(cache_path)
    if not cache_path.exists():
        cache_path.mkdir()
    encoded_filename = encode_filename(f"{section}:{filename}")
    with open(cache_path / encoded_filename, "wb") as fp:
        fp.write(data)
    filesize = int(section.split(':')[0])
    indexes, size = {}, 0
    for pth in cache_path.iterdir():
        if pth.is_file() and re.match(r"^[A-Fa-f0-9]+$", pth.name):
            decoded_filename = decode_filename(pth.name)
            if f":{filename}" not in decoded_filename:
                continue
            items = str(decoded_filename).split(':')
            _, start, end, name = int(items[0]), int(items[1]), int(items[2]), items[3]
            if start not in indexes:
                indexes[start] = (start, end, pth)
                size += end - start
    if size != filesize:
        return
    logging.info("  partition merging :", filename)
    with open(cache_path / f"{filename}", 'wb') as fp:
        sections = [indexes.get(k) for k in indexes]
        sections.sort(key=lambda x: x[0])
        for _section in sections:
            pth = _section[2]
            with open(pth, 'rb') as ep:
                fp.write(ep.read())
            os.remove(pth)


class RemoteManager:
    def __del__(self):
        managers.remove(self)

    def __init__(self):
        managers.add(self)
        self.connections = set()
        self.subscribers = []
        self.queue = asyncio.Queue()
        self.loop = asyncio.new_event_loop()
        self.handlers = []
        self.scopes = []

    def enable_search(self):
        root = os.getcwd()
        sys.path.append(root)
        return self

    def load_scope(self, module):
        scope = self_import(module)
        methods = [e for e in dir(scope) if not re.match(r"__[a-zA-Z0-9]*__", e)]
        log = (f'load scope : {module}\n---\n  '
               + '\n  '.join(methods)
               + '\n---')
        logging.info(log)
        self.scopes.append(dict(methods=methods, scope=scope))
        return self

    def apply(self, method_name, args):
        method = None
        for scope in self.scopes:
            if method_name in scope['methods']:
                method = scope['scope'].__getattribute__(method_name)
                break
        if method is None:
            raise Exception(f'No such method {method_name}')
        return method(*args) if callable(method) else method

    async def queue_loop(self):
        global running_state
        while running_state:
            try:
                item = await asyncio.wait_for(self.queue.get(), timeout=0.25)
                for ws in self.connections:
                    try:
                        await ws.write_message(item)
                    except Exception as e:
                        logging.error(str(e))
                self.queue.task_done()
            except asyncio.QueueEmpty:
                pass
            except asyncio.TimeoutError:
                pass

    def launch_queue(self):
        def th():
            self.loop.run_until_complete(self.queue_loop())

        threading.Thread(target=th).start()

    def launch_server(self, port=8080):
        tornado.web.Application(self.handlers).listen(port)
        logging.info("listening on port {}".format(port))
        tornado.ioloop.IOLoop.current().start()

    def publish(self, message):
        async def _pub(x):
            await self.queue.put(x)

        asyncio.run_coroutine_threadsafe(_pub(message), self.loop)


class WebsocketMessageHandler(tornado.websocket.WebSocketHandler):
    def initialize(self, remote):
        self.remote = remote

    def check_origin(self, origin: str) -> bool:
        return True

    def open(self, *args: str, **kwargs: str):
        self.remote.connections.add(self)
        logging.debug("websocket open :", self.request.remote_ip)


    def on_close(self):
        self.remote.connections.remove(self)
        logging.debug("websocket close :", self.request.remote_ip)

    def on_message(self, message):
        for subscribe in self.remote.subscribers:
            try:
                subscribe(message)
            except Exception as e:
                traceback.print_exception(e)


class PartitionUploadHandler(tornado.web.RequestHandler):
    def initialize(self, cache_path):
        self.cache_path = cache_path

    def post(self):
        section = self.request.headers.get('Section')
        filename = self.request.headers.get('Filename')
        save_partition(filename, section, self.request.body, self.cache_path)
        self.write(dict(success=True, code=200))


class RPCHandler(tornado.web.RequestHandler):
    def initialize(self, remote):
        self.remote = remote

    def post(self, *args, **kwargs):
        method_name = self.request.uri.split('/')[-1]
        args_voxe = self.request.body
        try:
            args = list(voxe.loads(args_voxe)) if len(args_voxe) > 0 else []
            logging.debug(" ", method_name, "(", tuple(args) if args is not None else '', ')')
            resp = self.remote.apply(method_name, args)
        except Exception as e:
            resp = e
        self.write(voxe.dumps(resp))


def main(args, remote: RemoteManager = None):
    try:
        prefix = args.prefix
        prefix = '/' if prefix == '' else prefix
        prefix = (prefix + '/') if not prefix.endswith('/') else prefix
        prefix = ('/' + prefix) if not prefix.startswith('/') else prefix
        static_path = args.static_path
        cache_path = args.cache_path
        remote = RemoteManager() if remote is None else remote
        remote.handlers = [
            *remote.handlers,
            (f'{prefix}websocket', WebsocketMessageHandler, dict(remote=remote)),
            (f'{prefix}upload', PartitionUploadHandler, dict(cache_path=cache_path)),
            (f'{prefix}rpc/([_a-zA-Z][_a-zA-Z0-9]*?)$', RPCHandler, dict(remote=remote)),
            (r'^/(.*?)$', tornado.web.StaticFileHandler, {"path": static_path, "default_filename": "index.html"},),
        ]
        remote.enable_search()
        for m in args.modules:
            remote.load_scope(m)
        remote.launch_queue()
        remote.launch_server(args.port)
    except Exception as e:
        logging.error(str(e))
        global running_state
        running_state = False
        exit(1)


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    options = [(r"^debug$", logging.DEBUG), (r"^info$", logging.INFO), (r"^warning$", logging.WARNING),
               (r"^error$", logging.ERROR), (r".*", logging.DEBUG)]
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s',
                        level=[e[1] for e in options if re.match(e[0], args.log_level)][0])
    main(args)
