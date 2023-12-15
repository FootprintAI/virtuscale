
class Resource():
    def __init__(self, cpu:str="1"):
        self._cpu = cpu
        #self._memory = "1Gi"

    @property
    def cpu(self) -> str:
        return self._cpu

    @cpu.setter
    def cpu(self, cpu: str):
        self._cpu = cpu

    #@property
    #def memory(self) -> str:
    #    return self._memory

    #@driver.setter
    #def memory(self, memory: str):
    #    self._memory = memory
