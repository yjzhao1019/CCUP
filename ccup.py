from tqdm import tqdm
import glob
import re
import numpy as np
from os import path as osp
from collections import defaultdict
import os

class CCUP(object):
    
    def __init__(self, root='data', dataset=None, **kwargs):
        self.dataset_dir = '/home/zhaoyujian/Dataset/CCUP/ccup_all'
        self.train_dir = osp.join(self.dataset_dir, 'train')
        self.query_dir = osp.join(self.dataset_dir, 'query')
        self.gallery_dir = osp.join(self.dataset_dir, 'gallery')
        
        train, num_train_pids, num_train_imgs = self._process_dir_train(self.dataset_dir, relabel=True)
        query, num_query_pids, num_query_imgs = [], 0, 0
        gallery, num_gallery_pids, num_gallery_imgs = [], 0, 0
        
        num_total_pids = num_train_pids + num_query_pids
        num_total_imgs = num_train_imgs + num_query_imgs + num_gallery_imgs
 
        
        print("=> CCUP loaded")
        print("Dataset statistics:")
        print("  ------------------------------")
        print("  subset   | # ids | # images")
        print("  ------------------------------")
        print("  train    | {:5d} | {:8d}".format(num_train_pids, num_train_imgs))
        print("  query    | {:5d} | {:8d}".format(num_query_pids, num_query_imgs))
        print("  gallery  | {:5d} | {:8d}".format(num_gallery_pids, num_gallery_imgs))
        print("  ------------------------------")
        print("  total    | {:5d} | {:8d}".format(num_total_pids, num_total_imgs))
        print("  ------------------------------")
        
        self.train = train
        self.query = query
        self.gallery = gallery
        
        self.num_train_pids = num_train_pids
        self.num_query_pids = num_query_pids
        self.num_gallery_pids = num_gallery_pids
    
    def _process_dir_train(self, dir_path, relabel=False):
        img_paths = glob.glob(osp.join(dir_path, '*.jpg'))
        pattern = re.compile(r'([-\d]+)_C([\d]+)_.*')

        pid_container = set()
        for img_path in tqdm(sorted(img_paths)):
            # print(img_path)
            pid, _ = map(int, pattern.search(img_path).groups())
            if pid == -1: continue  # junk images are just ignored
            pid_container.add(pid)
        pid2label = {pid: label for label, pid in enumerate(pid_container)}
        dataset = []
        for img_path in tqdm(sorted(img_paths)):
            pid, camid = map(int, pattern.search(img_path).groups())
            if pid == -1: continue  # junk images are just ignored
            
            camid -= 1  # index starts from 0
            if relabel: pid = pid2label[pid]

            dataset.append((img_path, pid, camid, 1))
        return dataset, len(pid_container), len(dataset)
