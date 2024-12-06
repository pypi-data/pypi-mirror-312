# -*- encoding: utf-8 -*-
from pyzrpc.mongo.client import _Tasks, _Services, _NodeInfo


class DBTasks(_Tasks):
    ...


class DBServices(_Services):
    ...


class DBNodeInfo(_NodeInfo):
    ...
