# エラー時の処理
#function err() {
#    exit 1
#}

#trap err ERR

cd /home/pi/Display_prj

#export PYTHONPATH=/home/pi/.local/lib/python3.7/site-packages

/bin/python3 /home/pi/Display_prj/mqtt_play.py &
#/bin/python3 /home/pi/Display_prj/playtest.py &
