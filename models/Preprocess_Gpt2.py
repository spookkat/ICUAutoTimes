import torch
import torch.nn as nn
from transformers import (
    GPT2LMHeadModel,
    GPT2Tokenizer,
)

import sys

class Model(nn.Module):
    def __init__(self, configs):
        super(Model, self).__init__()
        self.device = configs.gpu
        print(self.device)
        
        self.gpt2 = GPT2LMHeadModel.from_pretrained(
            configs.llm_ckp_dir,
            torch_dtype=torch.float16,
        ).to(self.device)

        self.gpt2_tokenizer = GPT2Tokenizer.from_pretrained(configs.llm_ckp_dir)
        self.gpt2_tokenizer.pad_token = self.gpt2_tokenizer.eos_token  # GPT2 doesn't have pad token
        self.vocab_size = self.gpt2_tokenizer.vocab_size
        self.hidden_dim_of_gpt2 = self.gpt2.config.hidden_size
        #self.hidden_dim_of_gpt2 = 768
        print(self.hidden_dim_of_gpt2)
        
        for name, param in self.gpt2.named_parameters():
            param.requires_grad = False

    def tokenizer(self, x):
        output = self.gpt2_tokenizer(x, return_tensors="pt", padding=True, truncation=True)['input_ids'].to(self.device)
        result = self.gpt2.transformer.wte(output)  # GPT-2 input embeddings
        return result   
    
    def forecast(self, x_mark_enc):        
        # x_mark_enc: list of input strings (length bs)
        #print(x_mark_enc.shape)
        # for i in range(len(x_mark_enc)):
        #     #print(x_mark_enc[i].strip())
        #     #print(len(x_mark_enc[i].strip()))
        #     print(self.tokenizer(x_mark_enc[i].strip()).shape)
        #     print(self.tokenizer(x_mark_enc[i].strip()).unsqueeze(0).shape)
        #     print(self.gpt2_tokenizer.tokenize(x_mark_enc[i].strip()))
        #     print(len(self.gpt2_tokenizer.tokenize(x_mark_enc[i].strip())))
        #embeddings = torch.squeeze(torch.cat([self.tokenizer(x_mark_enc[i].strip()).unsqueeze(0) for i in range(len(x_mark_enc))], 0))
        embeddings = self.tokenizer(x_mark_enc)
        print(embeddings.shape)
        bs, seq_len, dim = embeddings.shape
        embeddings = embeddings.view(bs, seq_len, dim)

        outputs = self.gpt2.transformer(inputs_embeds=embeddings).last_hidden_state
        #print(outputs.shape)
        
        last_hidden = outputs[:, -1, :]  # take last token hidden state
        #print(last_hidden.shape)
        return last_hidden
    
    def forward(self, x_mark_enc):
        return self.forecast(x_mark_enc)