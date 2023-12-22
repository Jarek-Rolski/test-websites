import os
import time

if os.environ["LUNCH"]== "true":
    print("Lunch start!")
    bashCommand = 'python lunch/main.py --root_path="/lunch" &'
    os.system(bashCommand)

if os.environ["GRADIO"]== "true":
    print("Gradio start!")
    bashCommand = 'python gradio/app.py --root_path="/gradio" &'
    os.system(bashCommand)

time.sleep(60*60*10)