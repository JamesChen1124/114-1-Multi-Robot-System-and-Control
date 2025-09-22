import serial, time

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)
print("Type something and press Enter")

while True:
    s = input("> ")
    ser.write((s + "\n").encode())
    print(ser.readline().decode(errors="ignore").strip())

ser.close()
