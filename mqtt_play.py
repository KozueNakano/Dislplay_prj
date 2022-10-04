#!usr/bin/env python
import paho.mqtt.client as mqtt     # MQTTのライブラリをインポート
import subprocess
from subprocess import call
import signal
import os
import sys
import fcntl
import termios


class VideoPlayer:
    def __init__(self):
        self.proc = None
        self.imageState = 0

    def stop(self):
        #stop image
        os.system("TERM=linux sudo echo -e 'q\\033\\0143' > /dev/tty1")
        c = "q\n"#'\x1B'#"q"
        with open('/dev/tty1', mode='w') as f:
            fcntl.ioctl(f, termios.TIOCSTI, c)
            print('quit fbi sent')
            self.imageState = 0

        if self.proc is not None and self.proc.poll() is None:
            print("stop")
            self.proc.stdin.write('q')
            self.proc.stdin.flush()
            print("q sent")

    def startVideo(self,n):
        cmd = "omxplayer --aspect-mode stretch /home/pi/Display_prj/%d.mp4"%(n)
        print(cmd)
        self.proc = subprocess.Popen(cmd, shell=True, 
                                        stdin=subprocess.PIPE, 
                                        universal_newlines=True)
    def startImage(self,a):
        self.imageState = 1
        cmd = "fbi -T 1 -d /dev/fb0 -a --noverbose --nocomments /home/pi/Display_prj/%s.png"%(a)
        print(cmd)
        self.proc = subprocess.Popen(cmd, shell=True, 
                                        stdin=subprocess.PIPE, 
                                        universal_newlines=True)




def handler(signal, frame):
        print('keyboard abort')
        sys.exit(0)

def blankTerminal():
    subprocess.check_call(
        "TERM=linux sudo setterm -blank force < /dev/tty1", 
        shell=True
    )
def de_blankTerminal():
    subprocess.check_call(
        "TERM=linux sudo setterm -blank poke < /dev/tty1", 
        shell=True
    )

if __name__ == '__main__':

    #os.system("TERM=linux sudo setterm -blank force < /dev/tty1")
    signal.signal(signal.SIGINT, handler)

    vp = VideoPlayer();
    
    # ブローカーに接続できたときの処理
    def on_connect(client, userdata, flag, rc):
        print("Connected with result code " + str(rc))  # 接続できた旨表示
        client.subscribe("#")  # subするトピックを設定

    # ブローカーが切断したときの処理
    def on_disconnect(client, userdata, rc):
        if rc != 0:
            print("Unexpected disconnection.")

    # メッセージが届いたときの処理
    def on_message(client, userdata, msg):
        # msg.topicにトピック名が，msg.payloadに届いたデータ本体が入っている
        print("Received message '" + str(msg.payload) +
            "' on topic '" + msg.topic + "' with QoS " + str(msg.qos))

        if msg.payload in [b'0',b'1',b'2',b'3',b'4',b'5',b'6',b'7',b'8',b'9']:
            print(int(msg.payload.decode()))
            videoNo = int(msg.payload.decode())
            vp.stop()
            vp.startVideo(videoNo)
        if msg.payload == b'A':
            vp.stop()
        if msg.payload in [b'.',b'=',b'+',b'-',b'*',b'%']:
            vp.stop()
            print(msg.payload.decode())
            vp.startImage(msg.payload.decode())
        if msg.payload in [b'`']:
            vp.stop()
            print("+-")
            vp.startImage("+-")
        if msg.payload in [b'/']:
            vp.stop()
            print(":")
            vp.startImage(":")
        #if msg.payload == b'M':
        #    os.system("TERM=linux sudo echo -e '\\033\\0143' > /dev/tty1")

        #for restart test
        #if msg.payload == b'=':
        #    vp.stopVideo()
        #    print("= abortFunc")
        #    sys.exit(1)

    # MQTTの接続設定
    client = mqtt.Client("player")             # クラスのインスタンス(実体)の作成
    client.username_pw_set("sub", "mosquitto")
    client.on_connect = on_connect         # 接続時のコールバック関数を登録
    client.on_disconnect = on_disconnect   # 切断時のコールバックを登録
    client.on_message = on_message         # メッセージ到着時のコールバック

    client.connect("localhost", 1883, 60)  # 接続先は自分自身

    client.loop_forever()                  # 永久ループして待ち続ける
