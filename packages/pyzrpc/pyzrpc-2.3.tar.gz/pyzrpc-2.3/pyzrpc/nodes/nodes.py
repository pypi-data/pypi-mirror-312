import json
import psutil
import platform

from pyzrpc.utils import FormatTime
from pyzrpc import Network


class PlatformInfo:

    def __init__(self):
        self.name = platform.system()
        self.release = platform.release()
        self.version = platform.version()
        self.machine = platform.machine()
        self.processor = platform.processor()

    def __str__(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return self.__str__()


class MemoryInfo:

    def __init__(self):
        memory_info = psutil.virtual_memory()

        self.memory_total = f"{memory_info.total / (1024 ** 3):.2f} GB"
        self.memory_available = f"{memory_info.available / (1024 ** 3):.2f} GB"
        self.memory_used = f"{memory_info.used / (1024 ** 3):.2f} GB"
        self.memory_percent = f"{memory_info.percent}%"

    def __str__(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return self.__str__()


class DiskInfo:
    def __init__(self):
        disk_info = psutil.disk_usage('/')
        self.disk_total = f"{disk_info.total / (1024 ** 3):.2f} GB"
        self.disk_used = f"{disk_info.used / (1024 ** 3):.2f} GB"
        self.disk_free = f"{disk_info.free / (1024 ** 3):.2f} GB"
        self.disk_percent = f"{disk_info.percent}%"

    def __str__(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return self.__str__()


class CPUInfo:
    def __init__(self):
        self.cpu_count = psutil.cpu_count()
        self.cpu_percent = psutil.cpu_percent(interval=1)
        self.cpu_freq_max = psutil.cpu_freq().max
        self.cpu_freq_min = psutil.cpu_freq().min
        self.cpu_freq_current = psutil.cpu_freq().current

    def __str__(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return self.__str__()


class _NodeInfo:
    def __init__(self):
        self.name = platform.node()
        self.ipaddr = self.get_ipaddr()
        self.platform = PlatformInfo()
        self.memory = MemoryInfo()
        self.disk = DiskInfo()
        self.cpu = CPUInfo()

        format_time = FormatTime()
        format_time.format = '%Y-%m-%d %H:%M:%S'
        self.update_time = format_time.get_converted_time()

        self.node = {
            'name': self.name,
            'ipaddr': self.ipaddr,
            'platform': self.platform.__dict__,
            'memory': self.memory.__dict__,
            'disk': self.disk.__dict__,
            'cpu': self.cpu.__dict__,
            'update_time': self.update_time
        }

    @staticmethod
    def get_ipaddr():
        return str(Network().get_ipaddr())
