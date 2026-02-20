import os
import pickle

def run_process():
    # 위반 사항 1: os.system
    os.system("ls -al")
    
    # 위반 사항 2: eval
    user_data = "1 + 1"
    eval(user_data)

def load_config():
    # 위반 사항 3: pickle.load
    with open("config.pkl", "rb") as f:
        data = pickle.load(f)