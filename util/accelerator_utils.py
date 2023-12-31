import torch
import os
import subprocess
import re
import sys
import time


class AcceleratorHelper():
    @staticmethod
    def print_container_info() -> None:
        print("-"*10)
        print(time.strftime("%Y-%m-%d_%H-%M-%S"))
        print(f"python version: {sys.version}")
        print(f"torch version: {torch.__version__}")
        print("-"*10)


    @staticmethod
    def nvidia_device_info() -> str:
        """get the nvidia MIGs device uuid and GPU uuid 
        """
        # blocking call
        result = subprocess.run(["nvidia-smi", "-L"], stdout=subprocess.PIPE)
        # decode the byte object, returns string with \n
        cmd_out_str = result.stdout.decode('utf-8')
        return [line.strip() for line in cmd_out_str.split('\n') if len(line) > 0]


    @staticmethod
    def extract_nvidia_device_uuids(input: str):
        """parse the nvidia devices uuid from the nvidia device info str
        """
        try:
            # r'' before the search pattern indicates it is a raw string, 
            # otherwise "" instead of single quote
            uuid = re.search(r'UUID\:\s(.+?)\)', input).group(1)
        except AttributeError:
            # "UUID\:\s" and "\)" not found
            uuid = ""
        return uuid


    @staticmethod
    def nvidia_device_uuids_filtered_by(is_mig: bool = False, log_output: bool = False) -> str:
        """get a comma separated str of nvidia MIGs devices
        """
        info_list = AcceleratorHelper.nvidia_device_info()
        if is_mig:
            # skip the first GPU ID, get the MIGs IDS
            uuid_list = [AcceleratorHelper.extract_nvidia_device_uuids(e) for e in info_list[1:]]
        else: # all GPU devices
            uuid_list = [AcceleratorHelper.extract_nvidia_device_uuids(e) for e in info_list]
        if log_output is not None and log_output:
            print(uuid_list)
        
        # if multi gpus need to join the device together for pytorch
        return ",".join(uuid_list)


    @staticmethod
    def init_cuda_torch(uuids: str, data_path: str, debug: bool = False) -> None:
        """setup the default env variables for transformers
        
        Args:
          uuids: a comma separate str of nvidia gpu/mig uuids
        """
        os.environ["WORLD_SIZE"] = "1" 
        os.environ["CUDA_VISIBLE_DEVICES"] = uuids 
        os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:512" #512
        os.environ['XDG_CACHE_HOME'] = f"{data_path}/models"
        if (debug):
            # for debugging      
            os.environ["CUDA_LAUNCH_BLOCKING"] = "1" 
        # os.environ["TOKENIZERS_PARALLELISM"]="false" 


class AcceleratorStatus():
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
        print(f"Device name      : {name} \n" +
              f"Device idx       : {device_idx} \n" +
              f"No. of processors: {count}")    


    def gpu_usage(self) -> None:        
        num_of_gpus = torch.cuda.device_count();
        # this shows only the gpu device, not the MIG
        print(f"num_of_gpus: {num_of_gpus}")
        for device_idx in range(torch.cuda.device_count()):
            print("-"*20)
            self.accelerator_compute_info(device_idx)                 
            self.accelerator_mem_info(device_idx)
            print("-"*20)
        