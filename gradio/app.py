import gradio as gr
import argparse

def greet(name):
    return "Hello " + name + "!"

def main(root_path):
    gr.Interface(fn=greet, inputs="text", outputs="text").launch(server_name="0.0.0.0",root_path=root_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--root_path', default='', type=str, help='Root path')
    args = parser.parse_args()
    
    main(root_path=args.root_path)
