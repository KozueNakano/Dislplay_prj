#!usr/bin/env python
import paho.mqtt.client as mqtt     # MQTTのライブラリをインポート
import sys
import signal
from time import sleep              # 3秒間のウェイトのために使う

import RPi.GPIO as GPIO

io_cmd_list = [
    [2,"0"],
    [17,"1"],
    [27,"2"],
    [22,"3"],
    [5,"4"],
    [6,"5"],
    [13,"6"],
    [19,"7"],
    [26,"8"],
    [21,"9"],
    [20,"A"],
    [16,"."],
    [12,"`"],
    [25,"="],
    [24,"+"],
    [23,"-"],
    [18,"*"],
    [15,"/"],
    [14,"%"]
]

def handler(signal, frame):
        print('keyboard abort')
        sys.exit(0)

if __name__ == '__main__':

    signal.signal(signal.SIGINT, handler)

    # ボタンの割込み関数
    def gpio_callback(channel):
        global status
        print("gpio ditected!")
        for io_cmd in io_cmd_list:
            if io_cmd[0] == channel:
                print(io_cmd[1])
                client.publish("gpio",io_cmd[1])    # トピック名とメッセージを決めて送信

    #pin Name method GPIO
    GPIO.setmode(GPIO.BCM)
    for io_cmd in io_cmd_list:
        GPIO.setup(io_cmd[0], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(io_cmd[0], GPIO.FALLING, callback=gpio_callback, bouncetime=500)

    
    # ブローカーに接続できたときの処理
    def on_connect(client, userdata, flag, rc):
        print("Connected with result code " + str(rc))  # 接続できた旨表示

    # ブローカーが切断したときの処理
    def on_disconnect(client, userdata, rc):
        if rc != 0:
            print("Unexpected disconnection.")

    # publishが完了したときの処理
    def on_publish(client, userdata, mid):
        print("publish: {0}".format(mid))

    # MQTTの接続設定
    client = mqtt.Client("gpio")             # クラスのインスタンス(実体)の作成
    client.username_pw_set("sub", "mosquitto")
    client.on_connect = on_connect         # 接続時のコールバック関数を登録
    client.on_disconnect = on_disconnect   # 切断時のコールバックを登録
    client.on_publish = on_publish         # メッセージ送信時のコールバック

    client.connect("localhost", 1883, 60)  # 接続先は自分自身

    client.loop_forever()    # subはloop_forever()でずっと待てる，loop_start()で起動だけさせる.
