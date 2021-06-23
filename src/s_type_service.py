# -*- coding: utf-8 -*-
'''
port 1884 is the port used when the container cont1 was created using the command:
$ sudo docker create -t -p 5000:5000 -p 5433:5432 -p 1884:1883 -p 9001:9001 -p 15672:15672 -p 81:80 -v fileshare:/myfolder --name cont1 synaisthisi
'''

import sys
sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "../"))
from Functions import sensing_utils as su

if __name__ == '__main__':
    username, user_pass, out_topic = su.s_type_service_args()
    client = mqtt.Client("S-type")
    client.username_pw_set(username, user_pass)
    broker = "localhost"

    try:
        client.connect(broker,1884)
    except:
        print("Error Connecting")
        sys.exit()

    su.upload_image(out_topic) #Publishing to the output topic
    client.disconnect()
    print("Conection Closed")
