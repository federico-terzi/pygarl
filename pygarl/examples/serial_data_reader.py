from ..data_readers import SerialDataReader

print("Opening the serial connection...")
sdr = SerialDataReader("COM6", verbose=True)

sdr.open()
print("Opened!")

sdr.mainloop()