from concurrent import futures
import grpc
import swordsec_pb2_grpc as swordsec_pb2_grpc
import swordsec_pb2 as swordsec_pb2
import redis

class SwordsecService(swordsec_pb2_grpc.SwordsecServicer):

    def __init__(self):
        self.connect = redis.Redis(host="redis", port=6379)
        self.pid = 1
        self.status = True

    def SetUserData(self, request_iterator, context):
        try:
            for user_data in request_iterator:
                self.connect.mset({
                    f"id/{str(self.pid)}": user_data.id,
                    f"first_name/{str(self.pid)}": user_data.first_name,
                    f"last_name/{str(self.pid)}": user_data.last_name,
                    f"email/{str(self.pid)}": user_data.email,
                    f"gender/{str(self.pid)}": user_data.gender,
                    f"ip_address/{str(self.pid)}": user_data.ip_address,
                    f"user_name/{str(self.pid)}": user_data.user_name,
                    f"agent/{str(self.pid)}": user_data.agent,
                    f"country/{str(self.pid)}": user_data.country,
                })
                self.pid += 1
        except:
            self.status = False
        return swordsec_pb2.ProcessStatus(status = self.status)

def start_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    swordsec_pb2_grpc.add_SwordsecServicer_to_server(SwordsecService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    start_server()