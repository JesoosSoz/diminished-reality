import os
import torch
print(os.getcwd())
if(os.getcwd() != r"e:\MIN\diminished-reality\DR.Backend\TestScripts\lama"):
    os.chdir('./DR.Backend/TestScripts/lama')
print(os.getcwd())
import subprocess
cmd = 'python ./bin/predict.py'

p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)