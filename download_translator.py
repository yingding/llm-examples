"""
Run this script to download a T5 family translator model

Example: 
>> python3 download_translator.py --help 
"""
import os
import click

# set the model download cache directory
# DATA_ROOT="/data"
DATA_ROOT="/home/jovyan/llm-models"
os.environ['model-type']="small"
os.environ['XDG_CACHE_HOME']=f"{DATA_ROOT}/core-kind/yinwang/models"

# from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import MT5Model, MT5ForConditionalGeneration, MT5TokenizerFast, MT5Config

# T5 model family info on huggingface
# https://huggingface.co/docs/transformers/model_doc/t5
# Note: T5 can only translate from "translate_en_to_de" but not de_to_en
# need to use mt5 

# model_map = {
#    "small": "t5-small",
#    "base" : "t5-base",
#    "large" : "t5-large",
#    "3B" : "t5-3b", # 11.4 GB
#    "11B" : "t5-11b" # 45.2 GB
# }

model_map = {
   "small": "google/mt5-small", # 1.2 GB
   "base" : "google/mt5-base", # 2.33 GB
   "large" : "google/mt5-large", # 4.9 GB,
   "xl" : "google/mt5-xl", # 15 GB
   "xxl" : "google/mt5-xxl" # 51.7 GB
}

# token_file_path = f"{DATA_ROOT}/core-kind/yinwang/.cache/huggingface/token"
# file = open(token_file_path, "r")

# file read add a new line to the token, remove it.
# token = file.read().replace('\n', '')

# print the raw string to see if there is new line in the token
# print(r'{}'.format(token))


@click.command()
@click.option('-t','--model-type', 'model_type', default=os.environ['model-type'], type=str, required=False, help=f"set the model type to download: {', '.join(model_map.keys())}, default is 7B")
def download(model_type: str="small"):
    """
    This method will download a T5 translator model. If cache exists, the cached model will be used.
    
    valid call:
    python3 download_translator.py -t small
    python3 download_translator.py --model-type small
    
    invalid call:
    python3 download_llms.py -t=small
    python3 download_llms.py --model-type=small
    
    Args:
      model_type: "small", ..., "3B", "11B"
    """
    # model_type = params.get("model-type", os.environ['model-type'])  
    model_name = model_map.get(model_type, model_map[os.environ['model-type']])
    
    print("-"*10)
    print(f"model_type: {model_type}")
    print(f"model_name: {model_name}")
    print("-"*10)
    
    tokenizer = MT5TokenizerFast.from_pretrained(model_name)
    model = MT5ForConditionalGeneration.from_pretrained(model_name)
    
    # tokenizer = T5Tokenizer.from_pretrained(model_name)
    # model = T5ForConditionalGeneration.from_pretrained(model_name)
    
    
if __name__ == '__main__':
    """
    uses default for click
    https://stackoverflow.com/questions/49011223/python-correct-use-of-click-with-main-and-init
    
    translator on huggingface: 
    https://huggingface.co/learn/nlp-course/chapter7/4?fw=tf
    
    Inference and Fine-tuning T5 model
    https://huggingface.co/docs/transformers/model_doc/t5
    """
    download()