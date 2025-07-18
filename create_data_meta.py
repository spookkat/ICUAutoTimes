import os
import argparse

def calculate_len(file_path, header=False):
    with open(file_path, 'r') as f:
        if header:
            next(f)
        data_len = sum(1 for _ in f)
    
    f.close()
    
    return data_len

def create_data_meta(data_path, header=False):
    files_list = os.listdir(data_path)
    with open('data_meta.txt', 'w') as data_meta:
        for file in files_list:
            file_len = calculate_len(os.path.join(data_path, file), header=header)

            data_meta.writelines([f"{file} {file_len}"])

    data_meta.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dataset Metadata")
    parser.add_argument('--data_path', type=str, default='data/', help='dataset folder path')
    args = parser.parse_args()

    data_path = args.data_path

    create_data_meta(data_path, header=True)