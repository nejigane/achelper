#!/usr/bin/env python3

import asyncio
import json
import os
import subprocess
import time
import websockets

template = '''
nl = lambda: list(map(int, input().split()))
sl = lambda: input().split()
n = lambda: int(input())
s = lambda: input()

#import sys
#sys.setrecursionlimit(1000)
#
#from fractions import gcd #3.4
#from math import gcd      #3.5
#def lcm(x, y):
#    return (x * y) // gcd(x, y)
#
#import itertools
#for p in itertools.product([False, True], repeat=10):
#for p in itertools.permutations('ABCD', 2):
#for p in itertools.combinations('ABCD', 2):
#
#import bisect
#bisect.bisect_left(A, 3)
#
#import heapq
#h = [1, 2, 3]
#heapq.heappush(h, a)
#heapq.heappop(h)
#
#from collections import defaultdict
#INF = float("inf")
#
#import math
#def ncr(n, r):
#    if r > n:
#        return 0
#    return math.factorial(n) // (math.factorial(n - r) * math.factorial(r))
'''

async def handle(websocket, path):
    data = json.loads(await websocket.recv())
    file_name = '{}.py'.format(data['problem'])
    prev_mtime = 0
    if not os.path.isfile(file_name):
        with open(file_name, 'w') as f:
            f.write('# {}'.format(data['problem']))
            f.write(template)
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
                lines = f.read().split('\n')
                lines = [l for l in lines if l.find('#') != 0]
                data['source'] = '\n'.join(lines)
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
