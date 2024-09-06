# import launch
# import requests
# import os

# def download_file(url, path):
#     if os.path.exists(path) and os.path.isfile(path):
#         return

#     with requests.get(url, stream=True) as r:
#         r.raise_for_status()
#         try:
#             with open(path, 'wb') as f:
#                 for chunk in r.iter_content(chunk_size=8192):
#                     f.write(chunk)
#         except Exception as e:
#             f.close()
#             raise e

# # TODO: add pip dependency if need extra module only on extension

# if not launch.is_installed("websockets"):    
#     launch.run_pip("install websockets==10.4")
    
# if not launch.is_installed("litelama"):    
#     launch.run_pip("install litelama==0.1.7")

# PROJECT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".")
# model_path = os.path.join(PROJECT_PATH, "./models/big-lama.safetensors")

# download_file('https://hf-mirror.com/anyisalin/big-lama/resolve/main/big-lama.safetensors?download=true', model_path)