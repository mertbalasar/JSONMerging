import redis, json, os

def remove_item(record, connect):
    connect.delete(f"id/{record}")
    connect.delete(f"first_name/{record}")
    connect.delete(f"last_name/{record}")
    connect.delete(f"email/{record}")
    connect.delete(f"gender/{record}")
    connect.delete(f"ip_address/{record}")
    connect.delete(f"user_name/{record}")
    connect.delete(f"agent/{record}")
    connect.delete(f"country/{record}")

def run():
    user_list = []
    connect = redis.Redis(host="redis", port=6379)
    record = 1
    indicator = connect.get(f"first_name/{record}")
    while indicator:
        user_data = {
                "id": int(connect.get(f"id/{record}")),
                "first_name": str(connect.get(f"first_name/{record}"), "utf-8"),
                "last_name": str(connect.get(f"last_name/{record}"), "utf-8"),
                "email": str(connect.get(f"email/{record}"), "utf-8"),
                "gender": str(connect.get(f"gender/{record}"), "utf-8"),
                "ip_address": str(connect.get(f"ip_address/{record}"), "utf-8"),
                "user_name": str(connect.get(f"user_name/{record}"), "utf-8"),
                "agent": str(connect.get(f"agent/{record}"), "utf-8"),
                "country": str(connect.get(f"country/{record}"), "utf-8")
            }
        remove_item(record, connect)
        user_list.append(user_data)
        record += 1
        indicator = connect.get(f"first_name/{record}")
    json.dump(user_list, open("last_data.json", "w"))
    print("Dosya Oluşturuldu")

if __name__ == '__main__':
    run()