#!/usr/bin/env python3

import asyncio
import json
import os
import subprocess
import time
import websockets

async def handle(websocket, path):
    data = json.loads(await websocket.recv())
    file_name = '{}.py'.format(data['problem'])
    if not os.path.isfile(file_name):
        with open(file_name, 'w') as f:
            f.write('# {}'.format(data['problem']))

    prev_mtime  = os.path.getmtime(file_name)
    while True:
        mtime = os.path.getmtime(file_name)
        if mtime > prev_mtime:
            for sample in data['samples']:
                proc = subprocess.Popen(['python3', file_name],
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
                stdout, stderr = proc.communicate(sample['input'].encode('utf-8'))
                sample['stdout'] = stdout.decode('utf-8')
                sample['stderr'] = stderr.decode('utf-8')
            with open(file_name) as f:
                data['source'] = f.read()
            await websocket.send(json.dumps(data))
            prev_mtime = mtime
        time.sleep(0.3)
        try:
            pong_waiter = await websocket.ping()
            await pong_waiter
        except:
            break

server = websockets.serve(handle, 'localhost', 8080)
asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
