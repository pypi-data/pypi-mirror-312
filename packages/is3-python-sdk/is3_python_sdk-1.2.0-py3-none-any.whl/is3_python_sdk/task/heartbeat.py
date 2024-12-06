import os
import random
import socket
import threading

from is3_python_sdk.data_query import iS3PythonApi

sequenceNum = 0
instanceId = random.randint(0, 2 ** 63 - 1)
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)


def time_task():
    global sequenceNum
    global instanceId
    global ip
    print("发送心跳")
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    filePath = os.path.join(project_root, 'config/config.ini')
    threading.Timer(10, time_task).start()
    requestId = random.randint(0, 2 ** 63 - 1)
    jsonData = {
        "requestId": requestId,
        "instanceId": instanceId,
        "sequenceNum": sequenceNum,
        "ip": ip,
    }
    is3Api = iS3PythonApi(filePath, None)
    response = is3Api.sendHeartbeat(jsonData)
    if response.get('code') == 500:
        sequenceNum = 0
        instanceId = random.randint(0, 2 ** 63 - 1)
    print(response)
    data = response.get('data')
    revRequestId = data.get('requestId')
    # 校验requestId是否相同
    if int(requestId) == int(revRequestId):
        sequenceNum = int(data.get("sequenceNum")) + 1
