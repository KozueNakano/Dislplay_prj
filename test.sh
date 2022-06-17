# エラー時の処理
function err() {
    exit 1
}
# エラーの有無にかかわらず、最後に実行する関数
#function finally() {
#}

#trap finally EXIT 
trap err ERR

/bin/python3 /home/pi/Display_prj/err_test.py