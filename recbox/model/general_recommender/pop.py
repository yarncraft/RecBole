# -*- coding: utf-8 -*-
# @Time   : 2020/8/11 9:57
# @Author : Zihan Lin
# @Email  : linzihan.super@foxmail.con
# @File   : pop.py

import torch
from ...utils import InputType
from ..abstract_recommender import GeneralRecommender


class Pop(GeneralRecommender):
    input_type = InputType.POINTWISE
    def __init__(self, config, dataset):
        super(Pop, self).__init__()
        self.USER_ID = config['USER_ID_FIELD']
        self.ITEM_ID = config['ITEM_ID_FIELD']
        self.device = config['device']
        self.n_items = dataset.num(self.ITEM_ID)
        self.item_cnt = torch.zeros(self.n_items, 1, dtype=torch.long, device=self.device, requires_grad=False)
        self.max_cnt = None

        self.fake_loss = torch.nn.Parameter(torch.FloatTensor([2]))

    def forward(self):
        pass

    def calculate_loss(self, interaction):

        item = interaction[self.ITEM_ID]
        self.item_cnt[item, :] = self.item_cnt[item, :] + 1

        self.max_cnt = torch.max(self.item_cnt, dim=0)[0]

        return self.fake_loss

    def predict(self, interaction):

        item = interaction[self.ITEM_ID]
        result = self.item_cnt[item, :] / self.max_cnt
        return result

    def full_sort_predict(self, interaction):
        batch_user_num = interaction[self.USER_ID].shape[0]
        result = self.item_cnt.to(torch.float64) / self.max_cnt.to(torch.float64)
        result = torch.repeat_interleave(result.unsqueeze(0), batch_user_num, dim=0)
        return result.view(-1)