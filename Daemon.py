from concurrent import futures
from datetime import datetime, timedelta
from random import randint

import time
import grpc
import berkeley_pb2
import berkeley_pb2_grpc

class Daemon(berkeley_pb2_grpc.ClockSyncServicer):
    daemon_time = time.time() + randint(100, 10000)

    def SyncTime(self, request, context):
        server_time = int(self.daemon_time * 1000)  # tempo do servidor em milissegundos
        client_time = request.client_time
        print(f"Tempo do servidor: {server_time}")
        time.sleep(3)
        print(f"Tempo do relógio: {client_time}")
        time.sleep(3)
        time_media = (server_time + client_time)/2
        daemon_time = time_media
        print(f"O novo tempo do daemon e dos relógios será: {int(time_media)}")
        return berkeley_pb2.TimeResponse(server_time=server_time, time_diff=int(time_media))

def service():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    berkeley_pb2_grpc.add_ClockSyncServicer_to_server(Daemon(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    service()
