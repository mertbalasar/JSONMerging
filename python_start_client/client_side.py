from __future__ import print_function
import grpc
import swordsec_pb2_grpc as swordsec_pb2_grpc
import swordsec_pb2 as swordsec_pb2
import os
import json, redis

def make_user_data(u_id, u_first_name, u_last_name, u_email, u_gender, u_ip_address, u_user_name, u_agent, u_country):
    return swordsec_pb2.UserData(
        id = u_id,
        first_name = u_first_name,
        last_name = u_last_name,
        email = u_email,
        gender = u_gender,
        ip_address = u_ip_address,
        user_name = u_user_name,
        agent = u_agent,
        country = u_country
    )

def read_from_files():
    fileList = os.listdir("./data")
    for f in fileList:
        data = json.load(open(f"./data/{f}"))
        for item in data:
            user_data = make_user_data(
                u_id = int(item["id"]),
                u_first_name = item["first_name"],
                u_last_name = item["last_name"],
                u_email = item["email"],
                u_gender = item["gender"],
                u_ip_address = item["ip_address"],
                u_user_name = item["user_name"],
                u_agent = item["agent"],
                u_country = item["country"]
            )
            yield user_data

def send_data(stub):
    response = stub.SetUserData(read_from_files())
    if response.status: print("Başarılı")
    else: print("Başarısız")

def run():
    with grpc.insecure_channel('start-python-server:50051') as channel:
        stub = swordsec_pb2_grpc.SwordsecStub(channel)
        send_data(stub)

if __name__ == '__main__':
    run()