
import random
import paho.mqtt.client as mqtt_client
import time

# broker = 'broker.hivemq.com'
broker = '192.168.7.2'
port = 1883
topic_lock = "device/lock"
topic_canlock = "device/canlock"
topic_data = "device/data"
topic_login = "login"
topic_logincheck = "login/check"
topic_datatest = "test/data"
topic_connect ="connect"
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'
lock_msg = None
connected_flag = False


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        global connected_flag
        if rc == 0:
            print("Connected to MQTT Broker!")
            # publish(client,topic_connect,"connect")
            connected_flag = True
        else:
            print("Failed to connect, return code %d\n", rc)
            connected_flag = False

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        global lock_msg
        received_message = msg.payload.decode()
        #test
        if msg.topic == topic_datatest:
            print(f"Received `{received_message}` from `{msg.topic}` topic")
            publish(client,topic_data,msg.payload.decode())
        #sub topic lock
        elif msg.topic == topic_lock:
            lock_msg = received_message
            print(f"Received `{received_message}` from `{msg.topic}` topic")
            # check_lock(client,received_message)
        #sub topic login
        elif msg.topic == topic_login:
            print(f"Received `{received_message}` from `{msg.topic}` topic new ")
            check_login(client,received_message)
    client.subscribe(topic_datatest)
    client.subscribe(topic_lock)
    client.subscribe(topic_login)
    client.on_message = on_message

def publish(client, topic,msg):
    while not connected_flag:
        time.sleep(1)
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
        print(f"Successfully sent `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic `{topic}`")
def check_login(client: mqtt_client,msg:str):
    pubmsg = ""
    username,password = msg.split("/")
    db = open("login_data.txt")
        
    name =[]
    pw = []
    for i in db:
        a,b = i.split("/")
        b = b.strip()
        name.append(a)
        pw.append(b)
    db.close()
    data = dict(zip(name, pw))
    try:
        if data[username]:
            try:
                if password == data[username]:
                    print("login success")
                    pubmsg ="success"
                else:
                    print("incorrect")
                    pubmsg = "incorrect"
            except:
                print("incorrect")
                pubmsg = "incorrect"
        else:
            print("No username")
            pubmsg ="no username"
    except:
        print("no username")
        pubmsg = "no username"
    publish(client,topic_logincheck,pubmsg)
def check_lock(client:mqtt_client,msg:str) :
    user,a,b,c = msg.split("/")
    db = open("data.txt","r+")
    ps =[]
    name =[]
    for i in db:
        nameArea,nameuser = i.split(":")
        ps.append(nameArea)
        
    db.close()
def run():
    client = connect_mqtt()
    # client.loop_start()
    # while not connected_flag:
    #     time.sleep(1)
    subscribe(client)
    client.loop_forever() 
if __name__ == '__main__':
    run()
