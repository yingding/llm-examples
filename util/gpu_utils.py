import torch

class GPUInfoHelper():
    def __init__(self):
        pass
    
    
    # Reference: https://stackoverflow.com/questions/58216000/get-total-amount-of-free-gpu-memory-and-available-using-pytorch
    # from typing import Tuple
    def byte_gb_info(self, byte_mem) -> str:
        """calculate the byte size to GB size for better human readable"""
        # format the f string float with :.2f to decimal digits
        # https://zetcode.com/python/fstring/
        return f"{(byte_mem/1024**3):4f} GB"


    def accelerator_mem_info(self, device_idx: int):
        # total
        t = torch.cuda.get_device_properties(device_idx).total_memory
        # usable
        r = torch.cuda.memory_reserved(device_idx)
        # allocated
        a = torch.cuda.memory_allocated(device_idx)
        # still free
        f = r-a
        # unit = "GB"   
        print( # "GPU memory info:\n" + 
              f"Physical  memory : {self.byte_gb_info(t)}\n" + 
              f"Reserved  memory : {self.byte_gb_info(r)}\n" + 
              f"Allocated memory : {self.byte_gb_info(a)}\n" + 
              f"Free      memory : {self.byte_gb_info(f)}")


    def accelerator_compute_info(self, device_idx: int) -> None:
        name = torch.cuda.get_device_properties(device_idx).name
        count = torch.cuda.get_device_properties(device_idx).multi_processor_count
        print(f"Device_name      : {name} \n" +
              f"Multi_processor  : {count}")    


    def gpu_usage(self) -> None:        
        num_of_gpus = torch.cuda.device_count();
        # this shows only the gpu device, not the MIG
        print(f"num_of_gpus: {num_of_gpus}")
        for device_idx in range(torch.cuda.device_count()):
            print("-"*20)
            self.accelerator_compute_info(device_idx)                 
            self.accelerator_mem_info(device_idx)
            print("-"*20)
        