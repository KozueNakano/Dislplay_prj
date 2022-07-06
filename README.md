# pi3サイネージセットアップ
### pi os lite busterをインストール
- pi os lite busterでomxplayerが動く。bullseyeでは動かない。
### raspiの便利機能を設定する    
- WLANのロケーション設定
- TimeZoneの設定
- keyboard使う場合はkeymapの設定
### ローカル用ネットワークのAPとDHCPを設定する
- 有線LANでインターネットに接続できるようにしておく。
- 設定のipaddress、hostname、等はすべてそのまま使う
- raspberry pi os "buster"の頃のガイドに従って、APとDHCPを設定する。
    [Guide](https://www.raspberrypi.com/documentation/computers/configuration.html#setting-up-a-routed-wireless-access-point)
- hostname gw.wlan
- ssid display_prj
- pass raspberrypi
### VS Codeでsshで開発できるようにする。
- host PCと同じネットワークに有線で接続する
- raspi-configでssh接続を許可する
- terminalからssh接続できるか確認する
    - `ssh pi@raspberrypi.local`
    - ホストが変わっている警告が出たら、sshキーを新たに生成し直す。
        - *`WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!`*
        - `ssh-keygen -R raspberrypi.local`

- VSCodeに、Remote - SSH拡張をインストールして、piにssh接続する
### gitのインストール
- $`sudo apt update` $`sudo apt install git`
### githubとの接続
- $`mkdir ~/.ssh` $`cd ~/.ssh`
- $`ssh-keygen -t rsa`
    - パスフレーズは設定する。
- githubのsettingから、sshの公開鍵を設定する
    - ~/.ssh/id_rsa.pub の内容をkeyとしてgithubに設定する
- $`ssh -T git@github.com` で接続を確認する
- gitにユーザー名とe-mailアドレスを設定する
    - `git config --global user.name "ユーザー名"`
    - `git config --global user.email メールアドレス`
### githubからリポジトリをクローンする
- クローン先のディレクトリをpiに作成する
    - `mkdir ~/Display_prj`
- さっき作ったディレクトリに、リポジトリの中身をクローン
    - `git clone git@github.com:KozueNakano/Dislplay_prj.git ~/Display_prj`
### 起動スプラッシュをミュートする
- /boot/cmdline.txt
        - superUserでの変更が必要なので、piにキーボードをつなげて変更する
    - `console=tty1`→`console=tty2`
    - add `logo.nologo quiet splash consoleblank=600  #vt.global_cursor_default=0`
        - 最後の#のコメントを外すと、カーソルの点滅を消せる
- /boot/config.txt
    - 最後に下行を追記
        ```disable_splash=1```
- disable login prompt
    - `sudo systemctl disable getty@tty1.service`
### omxplayer install
- sudo apt-get install omxplayer
### mosquitto install
- `sudo apt-get install mosquitto`
- `sudo apt-get install mosquitto-clients`
- `sudo chmod a+rwx /etc/mosquitto/conf.d`
- `cp /home/pi/Display_prj/display_prj.conf /etc/mosquitto/conf.d/`
- `sudo chmod a+rwx /etc/mosquitto`
- `touch /etc/mosquitto/password.txt`
- password.txtに`sub:mosquitto`を追記
- 暗号化
- `mosquitto_passwd -U /etc/mosquitto/password.txt`
- test
    ```
    sudo reboot now
    mosquitto_sub -h localhost -p 1883 -t "#" -u sub -P mosquitto
    mosquitto_pub -h raspberrypi.local -p 1883 -t "a" -m "ho"
    ```
### fbi install
- `sudo apt-get install fbi`
- /boot/config.txt
    - uncomment 
    `#disable_overscan=1`→`disable_overscan=1`
### python library install
- pip
    - `sudo apt install -y python3 python3-pip`
- paho すべてのユーザーから利用できるようにsudoでインストールする
    - `sudo pip3 install paho-mqtt`
### GPIOの機能設定
- raspi-configのinterfaceから、GPIOと競合しそうな、SPI,I2C,UART,1Wireなどをdisableする

### シャットダウン、起動ボタン
- gpio3とGNDを短絡するスイッチを接続する
- /boot/config.txtに下記を追加
    - `dtoverlay=gpio-shutdown`

### GPIOでpublish
- gpioとGNDを短絡するスイッチを接続する
    - ioとコマンドのアサインは、gpio_pub.pyを確認する

### 自動起動
- 起動するスクリプトに実行権限を与える、ついでにプロジェクトのディレクトリごと権限設定しておく
    - `sudo chmod a+rwx -R /home/pi/Display_prj`    
- serviceのunit fileを配置する
    - `sudo cp /home/pi/Display_prj/mqtt_play.service /etc/systemd/system/`
    - `sudo cp /home/pi/Display_prj/gpio_pub.service /etc/systemd/system/`
- serviceとして登録できたか確認する
    - `sudo systemctl list-unit-files --type=service | grep mqtt_play`
    - `sudo systemctl list-unit-files --type=service | grep gpio_pub`
- serviceを登録する、起動する、確認する
    - `sudo systemctl enable mqtt_play.service`
    - `sudo systemctl enable gpio_pub.service`
    - `sudo systemctl start mqtt_play.service`
    - `sudo systemctl start gpio_pub.service`
    - `sudo systemctl status mqtt_play.service`
    - `sudo systemctl status gpio_pub.service`
- 再起動して、serviceが起動しているか確認する

### ftpでファイル転送できるようにする
- `sudo apt-get install vsftpd`
- PCでpiが立てているWiFi APに接続する。
- filezillaでクイック接続
    - host:gw.wlan
    - user:pi
    - pass:デフォルトならraspberry
    - port:22

### フレキシブルディスプレイの設定
- フレキシブルディスプレイのHDMIコントローラが、信号のスケーリングに対応していないので、ぴったりの設定をしないとなにも表示されない。
- windowsで表示できたディスプレイは、Nvidiaのグラフィックボードを積んdなデスクトップPCで、Nvidiaのコントロールパネルから、カスタム解像度の設定の項目で、HDMIの信号の詳細を確認することができる。
- 今回は下記の設定を、/boot/config.txtに追記することで表示できる。(デフォルトで書いてある設定項目のかぶる項目はコメントアウトする)

```
#==================================================================================#
# HDMI 基本設定 Basic configuration
#==================================================================================#
hdmi_pixel_freq_limit=400000000
hdmi_drive=2
dtparam=audio=on
start_x=1
hdmi_group=2
hdmi_mode=87
dmi_force_hotplug=1
gpu_mem=128
dtparam=spi=on
dtparam=i2c_arm=on
#==================================================================================#
# 1440 x 1920 7.8Inch
#==================================================================================#
# メインの設定
#----------------------------------------------------------------------------------#
hdmi_timings=1440 0 32 4 44 1920 0 15 4 15 0 0 0 50 0 148504000 0
max_framebuffer_width=1440
max_framebuffer_height=1920
#----------------------------------------------------------------------------------#
display_rotate=3
framebuffer_width=1920
framebuffer_height=1440
```
参考
- https://www.raspberrypi.com/documentation/computers/config_txt.html
- https://twitter.com/_mer2/status/1299588071181053952
- https://akizukidenshi.com/catalog/g/gM-11967/

### ftpで動画ファイルを入れ替える方法
1. piを起動する
1. SSID:アップロード元のPCで、display_prjに接続する
1. filezillaでクイック接続
    - host:gw.wlan
    - user:pi
    - pass:デフォルトならraspberry
    - port:22
1. ~/Display_prjに動画、静止画ファイルをアップロードする。ファイル名を以下の通りとする。
    - 動画
        - 1920x1400
        - 0~9.mp4
    - 静止画
        - 1920x1400
        - ..png , +-.png , =.png , +.png , -.png , *.png , :.png , %.png

### 電源断に対するreadOnly化
- raspi-config
    - 4 Performance Options
        - P3 Overlay File System
            - overlay : enable
            - boot Partition : readOnly
