import os
import time

if os.environ["LUNCH"] != "false":
    print("Lunch start!")
    bashCommand = f'python lunch/main.py --root_path="{os.environ["LUNCH"]}" &'
    os.system(bashCommand)

if os.environ["GRADIO"] != "false":
    print("Gradio start!")
    bashCommand = f'python gradio/app.py --root_path="{os.environ["GRADIO"]}" &'
    os.system(bashCommand)

time.sleep(60*60*10)