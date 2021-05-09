# HW3
step1. compile by mbed-os in the directory of main.cpp step2. use python3 to excute wifi-mqtt/mqtt_client.py step3. uLCD會顯示20、40、60三個angle 紅色表示當前選擇的angle 手勢：1.逆時針畫圈 2.順時針畫三角形 3 . 往前出拳 step4. 按下USER_BTN，可以確認angle step5. 進入初始化階段，平放mbed step6. 進入量測階段，如果傾角超過所選取的angle會送msg給python，累積10次會送msg給mbed step7. 回到RPC_LOOP
