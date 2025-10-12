import serial
import time

# 修改成你 Arduino 的序列埠
arduino = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)  # 等待 Arduino 啟動

while True:
    cmd = input("輸入指令 (CW 100 / CCW 150), exit 離開: ")
    if cmd.lower() == "exit":
        break
    arduino.write((cmd + "\n").encode())
    time.sleep(0.1)  # 等待 Arduino 處理

    # 可選: 讀 Arduino 回傳訊息（如果有）
    while arduino.in_waiting:
        msg = arduino.readline().decode().strip()
        if msg:
            print(msg)

arduino.close()
