from random import randint

import grpc
import time
import berkeley_pb2
import berkeley_pb2_grpc

def sync_time():
    clock_time = time.time() + randint(100, 10000)

    print(f"Mandando tempo para o Daemon: {clock_time}")
    time.sleep(3)

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = berkeley_pb2_grpc.ClockSyncStub(channel)
        client_time = int(clock_time * 1000)  # tempo do cliente em milissegundos
        request = berkeley_pb2.TimeRequest(client_time=client_time)
        response = stub.SyncTime(request)
        server_time = response.server_time
        clock_time = server_time
        time_diff = server_time - client_time
        client_time += time_diff
        time.sleep(3)
        print('Novo tempo do servidor:', server_time)
        time.sleep(3)
        print('Novo tempo do cliente:', client_time)

if __name__ == '__main__':
    sync_time()
