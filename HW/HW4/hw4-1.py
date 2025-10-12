import serial
import time

# 開啟 Arduino 序列埠 
ser = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
time.sleep(2)  # 等 Arduino reset

print("Connected to Arduino. Type RED, GREEN, BLUE, OFF (EXIT to quit).")

try:
    while True:
        # 從終端機讀取指令
        cmd = input("Enter command: ").strip().upper()

        if cmd == "EXIT":
            break

        # 傳送指令給 Arduino (加上換行符號，Arduino 用 readStringUntil('\n') 來接收)
        ser.write((cmd + "\n").encode())

        # 等 Arduino 回應
        response = ser.readline().decode().strip()
        if response:
            print("Arduino:", response)

except KeyboardInterrupt:
    pass

finally:
    ser.close()
    print("Disconnected.")
