import os
import json
from pyzrpc import Observer, Logger, DBTasks, DBServices, DBNodeInfo, PROXY_NAME_KEY


class GenZrpc:

    def __init__(self):
        script_path = os.path.dirname(os.path.realpath(__file__))

        self._configs = json.load(open(os.path.join(script_path, 'st_config.json')))

        self._observer = Observer()
        self._observer.config = self._configs
        self._logger_obj = Logger()
        self._db_task = DBTasks()
        self._db_service = DBServices()
        self._bd_node_info = DBNodeInfo()

        self._observer.attach(self._db_task)
        self._observer.attach(self._logger_obj)
        self._observer.attach(self._db_service)
        self._observer.attach(self._bd_node_info)
        self._observer.notify()

    def logger(self):
        return self._logger_obj.logger(PROXY_NAME_KEY)

    def db_task(self):
        return self._db_task

    def db_service(self):
        return self._db_service

    def db_node_info(self):
        return self._bd_node_info
