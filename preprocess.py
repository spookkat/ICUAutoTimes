import argparse
import torch
from models.Preprocess_Llama import Model as Model_Llama
from models.Preprocess_Gpt2 import Model as Model_GPT2

from data_provider.data_loader import Dataset_Preprocess
from torch.utils.data import DataLoader

import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AutoTimes Preprocess')
    parser.add_argument('--gpu', type=int, default=0, help='gpu id')
    parser.add_argument('--llm', type=str, default='llama', help='llm name')
    parser.add_argument('--llm_ckp_dir', type=str, default='./llama', help='llm checkpoints dir')
    parser.add_argument('--dataset', type=str, default='ETTh1.csv', 
                        help='dataset to preprocess, options:[ETTh1, electricity, weather, traffic]')
    parser.add_argument('--dataset_path', type=str, default='./dataset/ETT-small/')
    parser.add_argument('--batch_size', type=int, default=1024)
    args = parser.parse_args()
    print(args.dataset)
    
    model = None
    if args.llm == 'llama':
        model = Model_Llama(args)
    elif args.llm == 'gpt2':
        model = Model_GPT2(args)

    seq_len = 672
    label_len = 576
    pred_len = 96
    
    # assert args.dataset in ['ETTh1', 'electricity', 'weather', 'traffic', 'Test']
    # if args.dataset == 'ETTh1':
    #     data_set = Dataset_Preprocess(
    #         root_path='./dataset/ETT-small/',
    #         data_path='ETTh1.csv',
    #         size=[seq_len, label_len, pred_len])
    # elif args.dataset == 'electricity':
    #     data_set = Dataset_Preprocess(
    #         root_path='./dataset/electricity/',
    #         data_path='electricity.csv',
    #         size=[seq_len, label_len, pred_len])
    # elif args.dataset == 'weather':
    #     data_set = Dataset_Preprocess(
    #         root_path='./dataset/weather/',
    #         data_path='weather.csv',
    #         size=[seq_len, label_len, pred_len])
    # elif args.dataset == 'traffic':
    #     data_set = Dataset_Preprocess(
    #         root_path='./dataset/traffic/',
    #         data_path='traffic.csv',
    #         size=[seq_len, label_len, pred_len])
    # elif args.dataset == 'Test':
    #     data_set = Dataset_Preprocess(
    #         root_path='./dataset/Test/',
    #         data_path='0001_processed.csv',
    #         size=[seq_len, label_len, pred_len])
    # elif args.dataset == 'Custom':
    #     data_set = Dataset_Preprocess(
    #         root_path='./dataset/Custom/',
    #         data_path='.',
    #         size=[seq_len, label_len, pred_len])
    data_set = Dataset_Preprocess(
                    root_path=args.dataset_path,
                    data_path=args.dataset,
                    size=[seq_len, label_len, pred_len])


    data_loader = DataLoader(
        data_set,
        #batch_size=128,
        batch_size=args.batch_size,
        shuffle=False,
    )

    from tqdm import tqdm
    print(len(data_set.data_stamp))
    print(data_set.tot_len)
    save_dir_path = f"{args.dataset_path}/time_embeddings/"
    os.makedirs(save_dir_path, exist_ok=True)
    output_list = []
    previous_filename = ''

    print("Starting embedding generation. Press 'CTRL+C' to stop.")
    for idx, (file_name, data) in tqdm(enumerate(data_loader)):
        try:
            curr_filename = file_name[0]
            #print(curr_filename)
            if curr_filename != previous_filename:
                if len(output_list) != 0:
                    result = torch.cat(output_list, dim=0)
                    #print(result.shape)
                    torch.save(result, save_dir_path + f'/{previous_filename}.pt')
                    print(f"Saved embeddings for {previous_filename}")
                    del result
                    del output_list
                    del output
                print(f"Starting for file: {curr_filename}")

            output = model(data)
            output_list.append(output.detach().cpu())
            previous_filename = curr_filename
        
        except KeyboardInterrupt:
            print("Interrupted")
            del output_list
            break
        
    # result = torch.cat(output_list, dim=0)
    # print(result.shape)
    # torch.save(result, save_dir_path + f'/{args.dataset}.pt')
