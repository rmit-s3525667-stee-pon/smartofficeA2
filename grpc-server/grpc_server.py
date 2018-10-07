# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Code reference from Tutelab 7
"""The Python implementation of the GRPC helloworld.Greeter server."""
import os
from concurrent import futures
from sense_hat import SenseHat
import time


import grpc
import sensehat_led
import sensehat_led_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

sensehat = SenseHat()

class Greeter(sensehat_led_grpc.GreeterServicer):
    """Greeter class"""
    #Get the value and display the correct color base on the value
    def SayHello(self, request, context):
        """Turn the SenseHat LED"""
        if request.name == "green":
            sensehat.clear(0,255,0)
            time.sleep(2)
            sensehat.clear()
            return sensehat_led.HelloReply(message='Patient is found!')
        elif request.name =="red":
            sensehat.clear(255,0,0)
            time.sleep(2)
            sensehat.clear()
            return sensehat_led.HelloReply(message='Patient is not found!')

# hosting the server
def serve():
    """Host the server"""
    host = os.popen('hostname -I').read() # get the IP address of your Raspberry Pi
    print(host)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sensehat_led_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('{}:50051'.format(host))
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
