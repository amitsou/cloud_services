# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "../"))
from Functions import processing_utils as pu


def on_log(client, userdata, level, buf):
    """
        Log callback
    """
    print("log: ", buf)
    pass

def on_disconnect(client, userdata, flags, rc=0):
    """
        Callback to define what's happening when disconnecting
    """
    print("DisConnected flags {0}, result code:{1}, client_id: {2} ".format(flags, rc, client._client_id))

def on_message(client, userdata, message):
    """
        Callback to handle subscription topics incoming messages
    """
    msg = message
    pu.motion_clf(msg)

def on_connect(client, userdata, flags, rc):
    """
        Callback to define what to happen when connecting
    """
    if(rc==0):
        print("connecting to broker ", broker)
        print("subscribing to topics ")
        client.subscribe(in_topic)

    elif(rc==3):
        print("server unavailable")
        client.loop_stop()
        sys.exit("Server is unavailable, please try later")
    elif(rc==5):
        print("Invalid Credentials")
        client.loop_stop()
        sys.exit(5)
    else:
        print("Bad connection, returned code=",rc)
        client.loop_stop()
        sys.exit("Bad connection, returned code={0}".format(rc))


if __name__ == '__main__':
    u_name. u_pass, in_topic, out_topic = pu.p_type_service_args()
    broker = "localhost"

    client = mqtt.Client("P-type")
    client.username_pw_set(username, user_pass)
    client.on_message = on_message
    client.on_log = on_log
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    try:
	    client.connect(broker)
    except:
	    print("Error connecting")
	    sys.exit()

    client.loop_forever()
