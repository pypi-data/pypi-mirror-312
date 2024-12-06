import json
import base64
import argparse
import time

from pyzrpc.meta import NODE_IPADDR_KEY
from pyzrpc import Logger, DBNodeInfo, Observer, PROXY_NAME_KEY
from pyzrpc.nodes import NodeInfo


class HeartbeatDetection:

    def __init__(self, config):
        _observer = Observer()
        _observer.config = config

        self._logger = Logger()
        self._db_nodes = DBNodeInfo()

        _observer.attach(self._logger)
        _observer.attach(self._db_nodes)
        _observer.notify()

    def start(self):
        while True:
            try:
                node_info = NodeInfo()
                self._logger.logger(PROXY_NAME_KEY).info(f"{node_info.node}")

                self._db_nodes.update_many(
                    query={NODE_IPADDR_KEY: node_info.ipaddr},
                    update_data=node_info.node,
                    upsert=True
                )
                time.sleep(60)
            except Exception as e:
                self._logger.logger(PROXY_NAME_KEY).error(f"[HeartbeatDetection] {e}")
                time.sleep(60)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="run heartbeat detection script")

    parser.add_argument("--config", type=str, help="heartbeat detection config")
    args = parser.parse_args()

    encoded_string = args.config
    encoded_bytes = encoded_string.encode('utf-8')
    decoded_bytes = base64.b64decode(encoded_bytes)
    decoded_string = decoded_bytes.decode('utf-8')
    configs = json.loads(decoded_string)

    HeartbeatDetection(configs).start()
