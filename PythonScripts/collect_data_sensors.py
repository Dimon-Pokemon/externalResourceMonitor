import clr # the pythonnet module.
# clr.AddReference(r'./OpenHardwareMonitorLib') 
clr.AddReference(r'./CPUThermometerLib')
# e.g. clr.AddReference(r'OpenHardwareMonitor/OpenHardwareMonitorLib'), without .dll

from OpenHardwareMonitor.Hardware import Computer

class SensHandler:
    computer = None

    def __init__(self):
        self.computer = Computer()
        self.computer.GPUEnabled = True # get the Info about GPU
        self.computer.CPUEnabled = True
        self.computer.RAMEnabled = True
        self.computer.FanControllerEnabled = True
        self.computer.MainboardEnabled = True
        self.computer.Open()

    def get_info(self):
        for device in range(0, len(self.computer.Hardware)):
            print(self.computer.Hardware[device].Name)
            print(self.computer.Hardware[device].HardwareType)
            for sensor in range(0, len(self.computer.Hardware[device].Sensors)):
                print(f"Имя: {self.computer.Hardware[device].Sensors[sensor].Name}. Тип: {self.computer.Hardware[device].Sensors[sensor].SensorType}")
            print("\n"+"*"*100+"\n")



    def get_current_temp(self, number):
        self.computer.Hardware[number].Update()
        temps = []
        for a in range(0, len(self.computer.Hardware[number].Sensors)):
            if "/temperature" in str(self.computer.Hardware[number].Sensors[a].Identifier):
                temp = self.computer.Hardware[number].Sensors[a].get_Value()
                print(f"Temperature sensor №{a}: {temp}°C")
                temps.append(temp)
        
        avg_temp = int(sum(temps)/len(temps))
        print(f"AVG temperature: {avg_temp}°C")
        return avg_temp
                


    def get_current_GPU_load(self, number):
        self.computer.Hardware[number].Update()
        loads = []
        core = None
        for a in range(0, len(self.computer.Hardware[number].Sensors)):
            if "/load" in str(self.computer.Hardware[number].Sensors[a].Identifier):
                load = self.computer.Hardware[number].Sensors[a].get_Value()
                print(f"Load sensor №{a}: {load}%. Имя: {self.computer.Hardware[number].Sensors[a].Name}. Тип: {self.computer.Hardware[number].Sensors[a].SensorType}")
                loads.append(load)
                if self.computer.Hardware[number].Sensors[a].Name == "GPU Core":
                    core = int(load)
        
        avg_load = int(sum(loads)/len(loads))
        print(f"AVG load: {avg_load}%. Core load: {core}%")
        return core
    
    def get_current_CPU_load(self, number):
        self.computer.Hardware[number].Update()
        loads = []
        avg_load = None
        for a in range(0, len(self.computer.Hardware[number].Sensors)):
            if "/load" in str(self.computer.Hardware[number].Sensors[a].Identifier):
                load = self.computer.Hardware[number].Sensors[a].get_Value()
                print(f"Load sensor №{a}: {load}%. Имя: {self.computer.Hardware[number].Sensors[a].Name}. Тип: {self.computer.Hardware[number].Sensors[a].SensorType}")
                loads.append(load)
                if self.computer.Hardware[number].Sensors[a].Name == "CPU Total":
                    avg_load = int(load)
        
        # avg_load = int(sum(loads)/len(loads))
        print(f"AVG load: {avg_load}%.")
        return [int(loads[0]), int(loads[1]), int(loads[2]), int(loads[3]), int(loads[4]), int(loads[5])]
    
    def get_current_RAM(self, number):
        data = []
        self.computer.Hardware[number].Update()
        for a in range(0, len(self.computer.Hardware[number].Sensors)):
            value = self.computer.Hardware[number].Sensors[a].get_Value()
            print(f"Sensor №{a}: {value}. Имя: {self.computer.Hardware[number].Sensors[a].Name}. Тип: {self.computer.Hardware[number].Sensors[a].SensorType}")
            data.append(value)
        
        return [int(data[0]), int(data[1]), int(data[2])]

    def get_index_hardware(self, hardware: str):
        for index in range(0, len(self.computer.Hardware)):
            if str(self.computer.Hardware[index].HardwareType) == hardware or hardware.lower() in str(self.computer.Hardware[index].HardwareType).lower():
                return index


if __name__ == "__main__":
    from time import sleep
    c = SensHandler()
    c.get_info()
    while True:
        # c.get_current_CPU_load(c.get_index_hardware("CPU"))
        c.get_current_RAM(c.get_index_hardware("RAM"))
        sleep(1)
        # print(c.get_current_temp(0))
        # print(c.get_current_load(0))
