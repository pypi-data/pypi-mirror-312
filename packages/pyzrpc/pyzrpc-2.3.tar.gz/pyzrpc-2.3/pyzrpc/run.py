# -*- encoding: utf-8 -*-
import os
import sys
import time
import json
import base64
import psutil
import subprocess

from pyzrpc import FLASK_PORT_KEY, FLASK_PORT_DEFAULT_VALUE_KEY, FLASK_HOST_KEY, FLASK_HOST_DEFAULT_VALUE_KEY
from pyzrpc.meta import FLASK_STATUS_KEY
from pyzrpc.work import work_start
from pyzrpc.service import service_start
from pyzrpc.nodes import heartbeat_detection
from pyzrpc.admin import admin_web


class _ServiceRegistry:
    _service_list = []
    _config = None

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value

    @property
    def service_list(self):
        return self._service_list

    def registry(self, services):
        self._service_list = services

    def _start_service(self, _service):
        bytes_to_encode = json.dumps(self.config).encode('utf-8')
        encoded_bytes = base64.b64encode(bytes_to_encode)
        encoded_string = encoded_bytes.decode('utf-8')

        for proc in psutil.process_iter(['cmdline']):
            for cmd in proc.cmdline():
                if _service.__file__ in cmd:
                    proc.kill()
                    time.sleep(0.1)

        python_executable = sys.executable if 'python' in sys.executable else 'python3'
        command = [
            python_executable,
            service_start.__file__,
            '--config', encoded_string,
            '--path', _service.__file__
        ]
        process = subprocess.Popen(command)
        return process.pid

    def _start_work(self, _service, service_pid):
        bytes_to_encode = json.dumps(self.config).encode('utf-8')
        encoded_bytes = base64.b64encode(bytes_to_encode)
        encoded_string = encoded_bytes.decode('utf-8')

        python_executable = sys.executable if 'python' in sys.executable else 'python3'
        command = [
            python_executable,
            work_start.__file__,
            '--config', encoded_string,
            '--service_pid', str(service_pid),
            '--path', _service.__file__
        ]

        process = subprocess.Popen(command)
        return process.pid

    def _start_heartbeat_detection(self):
        bytes_to_encode = json.dumps(self.config).encode('utf-8')
        encoded_bytes = base64.b64encode(bytes_to_encode)
        encoded_string = encoded_bytes.decode('utf-8')

        for proc in psutil.process_iter(['cmdline']):
            for cmd in proc.cmdline():
                if heartbeat_detection.__file__ in cmd:
                    proc.kill()
                    time.sleep(0.1)

        python_executable = sys.executable if 'python' in sys.executable else 'python3'
        command = [
            python_executable,
            heartbeat_detection.__file__,
            '--config', encoded_string
        ]

        process = subprocess.Popen(command)
        return process.pid

    def _start_admin_web(self):
        for proc in psutil.process_iter(['cmdline']):
            for cmd in proc.cmdline():
                if admin_web.__file__ in cmd:
                    proc.kill()
                    time.sleep(0.1)

        python_executable = sys.executable if 'python' in sys.executable else 'python3'
        command = [
            python_executable,
            '-m', 'streamlit', 'run',
            admin_web.__file__,
            '--server.port', str(self.config.get(FLASK_PORT_KEY, FLASK_PORT_DEFAULT_VALUE_KEY)),
            '--server.address', self.config.get(FLASK_HOST_KEY, FLASK_HOST_DEFAULT_VALUE_KEY)
        ]

        config_path = os.path.join(os.path.dirname(admin_web.__file__), 'st_config.json')
        open(config_path, 'w').write(json.dumps(self.config, ensure_ascii=False))

        process = subprocess.Popen(command)

        return process.pid

    def start(self):

        for _service in self.service_list:
            service_pid = self._start_service(_service)
            time.sleep(0.2)
            self._start_work(_service, service_pid)

        if self.config.get(FLASK_STATUS_KEY, False):
            self._start_admin_web()

        self._start_heartbeat_detection()
