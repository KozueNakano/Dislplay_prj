#!usr/bin/env python
import paho.mqtt.client as mqtt     # MQTTのライブラリをインポート
import sys
import signal
from time import sleep              # 3秒間のウェイトのために使う

def handler(signal, frame):
        print('keyboard abort')
        sys.exit(0)

if __name__ == '__main__':

    signal.signal(signal.SIGINT, handler)

    
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

    client.loop_start()    # subはloop_forever()だが，pubはloop_start()で起動だけさせる

    while True:
        client.publish("gpio","3")    # トピック名とメッセージを決めて送信
        sleep(10)   # 3秒待つ