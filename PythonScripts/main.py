from connect_com import COM
from collect_data_sensors import SensHandler

from time import sleep

com = COM("COM10")
sens = SensHandler()

type_hardware = "GPU"
index_hardware = sens.get_index_hardware(type_hardware)

while True:
    print("*"*10 + "WORK" + "*" * 10)
    if com.serial.in_waiting > 0:
        print("\nВ БУФЕРЕ ЕСТЬ ДАННЫЕ \n")
        type_hardware = com.serial.read(3).decode("utf-8")
        index_hardware = sens.get_index_hardware(type_hardware)
        print(type_hardware)
    if type_hardware == "CPU":
        print(*sens.get_current_CPU_load(index_hardware))
        com.send_data(*sens.get_current_CPU_load(index_hardware))
    elif type_hardware == "GPU":
        com.send_data(sens.get_current_temp(index_hardware), sens.get_current_GPU_load(index_hardware))
    elif type_hardware == "RAM":
        com.send_data(*sens.get_current_RAM(index_hardware))
    else:
        pass
    sleep(1.5)
    # com.send_type_hardware("GPU")
    # sleep(3)
