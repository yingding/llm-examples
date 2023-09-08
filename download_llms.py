"""
Before run this script, need to generate a token from huggingface
To login, `huggingface_hub` requires a token generated from https://huggingface.co/settings/tokens
-> user profile -> settings -> Access Tokens -> New token
name: llama2
role: read

Then call
huggingface-cli

use 
echo "<my_token>" > token
to create a token instead of using vi, which will add a new line char to token automatically.

"""
import os
import click
# import argpass



# set the model download cache directory
# DATA_ROOT="/data"
DATA_ROOT="/home/jovyan/llm-models"
os.environ['model-type']="7B"
os.environ['XDG_CACHE_HOME']=f"{DATA_ROOT}/core-kind/yinwang/models"

from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

model_map = {
   "7B": "meta-llama/Llama-2-7b-chat-hf",
   "13B" : "meta-llama/Llama-2-13b-chat-hf",
   "70B" : "meta-llama/Llama-2-70b-hf"
}

token_file_path = f"{DATA_ROOT}/core-kind/yinwang/.cache/huggingface/token"
file = open(token_file_path, "r")
# file read add a new line to the token, remove it.
token = file.read().replace('\n', '')
file.close()

# print the raw string to see if there is new line in the token
# print(r'{}'.format(token))

# Reference: https://click.palletsprojects.com/en/8.1.x/quickstart/
# @click.option(..., is_flag=True, ...) set the option to be boolean
# call with download_llms --help
# https://www.geeksforgeeks.org/argparse-vs-docopt-vs-click-comparing-python-command-line-parsing-libraries/
# https://click.palletsprojects.com/en/8.1.x/quickstart/
# https://click.palletsprojects.com/en/8.1.x/options/
# https://www.youtube.com/watch?v=kNke39OZ2k0
@click.command()
@click.option('-t','--model-type', 'model_type', default=os.environ['model-type'], type=str, required=False, help=f"set the llama2 type to download: {', '.join(model_map.keys())}, default is 7B")
def download(model_type: str="7B"):
    """
    This method will download the llama2 model. If cache exists, the cached model will be used.
    
    valid call:
    python3 download_llms.py -t 7B
    python3 download_llms.py --model-type 7B
    
    invalid call:
    python3 download_llms.py -t=7B
    python3 download_llms.py --model-type=7B
    
    Args:
      model_type: "7B", "13B", "70B"
    """
    # model_type = params.get("model-type", os.environ['model-type'])  
    model_name = model_map.get(model_type, model_map[os.environ['model-type']])
    
    print("-"*10)
    print(f"model_type: {model_type}")
    print(f"model_name: {model_name}")
    print("-"*10)
        
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=token)
    model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=token)
    
if __name__ == '__main__':
    """
    uses default for click
    https://stackoverflow.com/questions/49011223/python-correct-use-of-click-with-main-and-init
    """
#    parser = argparse.ArgumentParser()
#    parser.add_argument('--model-type', dest='model-type',
#                        default=os.environ['model-type'], type=str, help='the llama2 type to download: 7B, 13B')
    
#    args = parser.parse_args()
#    params_dict = args.__dict__
    
#    print(params_dict)
    download()