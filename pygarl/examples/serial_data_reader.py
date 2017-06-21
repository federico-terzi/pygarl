from ..data_readers import SerialDataReader

print("Opening the serial connection...")
sdr = SerialDataReader("COM6")

sdr.open()
print("Opened!")

sdr.mainloop()