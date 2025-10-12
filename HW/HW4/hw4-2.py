import serial
import time

# 修改成你 Arduino 的序列埠
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # 等待 Arduino 啟動

while True:
    cmd = input("輸入指令 (例如 1 ON / 2 OFF): ")
    if cmd.lower() == "exit":
        break
    arduino.write((cmd + "\n").encode())  # 發送指令
    time.sleep(0.1)  # 等待 Arduino 處理

    # 讀取 Arduino 回傳的 LED 狀態
    while arduino.in_waiting:
        status = arduino.readline().decode().strip()
        if status:
            print("LED 狀態:", status)

arduino.close()
