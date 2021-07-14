import sys
# -*- coding: utf-8 -*-
sys.path.append("../../")
import json
import bisect
import hashlib

from hashring.common import exceptions as exc
from hashring.common.config import Const
from hashring.common.config import logger

def get_hash(raw_str):
    """将字符串映射到2^32的数字中"""
    md5_str = hashlib.md5(raw_str.encode('utf-8')).hexdigest()
    return int(md5_str, 16) % (Const.MOD_NUM)

class DataManager(object):
    """Data manager."""
    # sorted_cache_list = []  # 排序好的hash值(虚拟节点)
    # cache_node = dict()  # 存储虚拟节点到物理设备的hash映射
    dev_inf = None  # 设备信息
    filename = None

    def __init__(self, path):
        DataManager.filename=path

    @classmethod
    def load(cls):
        u"""加载文件.
        :param filename: 文件名
        """
        with open(DataManager.filename) as f:
            cls.dev_inf = json.load(f)
        

    @classmethod
    def save(cls):
        u"""保存文件.

        :param filename: 文件名
        """
        with open(DataManager.filename, "w") as f:
            json.dump(cls.dev_inf, f)


class RingBuilder(object):
    """ring builder."""

    def __init__(self, data_manager):
        self.sorted_cache_list = []  # 排序好的hash值(虚拟节点)
        self.cache_node = dict()  # 存储虚拟节点到物理设备的hash映射
        self.data_manager = data_manager
        for key, item in self.data_manager.dev_inf.items():
            virtual_num = item[Const.PART_NUM]
            weight = item[Const.DEV_WEIGHT]
            for index in range(0, virtual_num * weight):
                node_hash = get_hash("%s_%s" % (key, index))
                bisect.insort(self.sorted_cache_list, node_hash)
                self.cache_node[node_hash] = key
        

    def add_dev(self, dev_id, dev_name=None, dev_weight=None, part_num=None):
        u"""添加设备.
        :param dev_id: 待添加的设备信息
        """
        # raise exc.ErrorNotImplemented()
        if dev_id in self.data_manager.dev_inf.keys():
            return 
        # params check
        try:
            if dev_id and not isinstance(dev_id, str):
                raise ValueError("dev_id must be str type")
            if dev_name and not isinstance(dev_name, str):
                raise ValueError("dev_name must be str type")
            if dev_weight and  not isinstance(dev_weight, int):
                raise ValueError("dev_weight must be int type")
            if part_num and not isinstance(part_num, int):
                raise ValueError("part_num must be int type")
        except ValueError as e:
            logger.info("error:", repr(e))
    
        added_dev = {dev_id: {Const.DEV_NAME:dev_name, Const.DEV_WEIGHT:dev_weight, Const.PART_NUM:part_num}}
        self.data_manager.dev_inf.update(added_dev)
        # rebalance
        virtual_node_num = dev_weight * part_num
        self.rebalance(dev_id, 
            add_or_remove=Const.ADD,
            start_node_index=0,
            end_node_index=virtual_node_num+1)
        # save dev_inf
        self.data_manager.save()

    def update_dev(self, dev_id, dev_weight=None):
        u"""更新设备信息.

        :param dev_id: 设备ID
        :param weight: 权重
        """
        if dev_id not in self.data_manager.dev_inf:
            return  
        # params check  @TODO dev_weight > 0
        try:
            if dev_id and not isinstance(dev_id, str):
                raise ValueError("dev_id must be str type")
            if dev_weight and not isinstance(dev_weight, int):
                raise ValueError("dev_weight must be int type")
        except ValueError as e:
            logger.info("error:", repr(e))

        # rebalance
        info_of_dev_id = self.data_manager.dev_inf[dev_id]  # dev_id 的设备信息， 字典类型
        virtual_num = info_of_dev_id[Const.PART_NUM]
        old_dev_weight = info_of_dev_id[Const.DEV_WEIGHT]
        old_virtual_node_num = old_dev_weight * virtual_num
        new_virtual_node_num = dev_weight * virtual_num
        logger.info("new_virtual_node_num:{}".format(new_virtual_node_num))
        logger.info("old_virtual_node_num:{}".format(old_virtual_node_num))
        if old_virtual_node_num < new_virtual_node_num:
            self.rebalance(dev_id, 
                add_or_remove=Const.ADD, 
                start_node_index = old_virtual_node_num,
                end_node_index = new_virtual_node_num)
        elif old_virtual_node_num > new_virtual_node_num:
            self.rebalance(dev_id,
                add_or_remove = Const.REMOVE,
                start_node_index = new_virtual_node_num,
                end_node_index = old_virtual_node_num)
        # save dev_inf                
        self.data_manager.dev_inf[dev_id].update({Const.DEV_WEIGHT: dev_weight})
        self.data_manager.save()
        

    def remove_dev(self, dev_id):
        u"""删除设备.

        :param dev_id: 待删除的设备ID
        """
        item = self.data_manager.dev_inf[dev_id]  # dev_id : str
        self.virtual_num = item[Const.PART_NUM]
        del self.data_manager.dev_inf[dev_id]
        virtual_node_num = self.virtual_num * item[Const.DEV_WEIGHT]

        self.rebalance(dev_id,
            add_or_remove=Const.REMOVE,
            start_node_index=0, 
            end_node_index=virtual_node_num)
        self.data_manager.save()

    # @TODO params check
    def rebalance(self, dev_id, add_or_remove, start_node_index, end_node_index):
        u"""重新平衡ring."""
        for index in range(start_node_index, end_node_index):
            node_hash = get_hash("%s_%s" % (dev_id, index))
            logger.info("virtual_node: {}_{}, hash_value:{}".format(dev_id,index,node_hash))
            if add_or_remove == Const.ADD:
                bisect.insort(self.sorted_cache_list, node_hash)
                self.cache_node[node_hash] = dev_id
                logger.info("virtual_node: {}_{} is added".format(dev_id,index))
            else:
                self.sorted_cache_list.remove(node_hash)
                del self.cache_node[node_hash]
                logger.info("virtual_node: {}_{} is removed".format(dev_id,index))

    def hash_dev(self, key):
        u"""获取指定key hash到的设备."""
        node_index = bisect.bisect_left(self.sorted_cache_list, key) # 
        node_index = node_index % len(self.sorted_cache_list)  # 若比最大的node hash还大，分发给第一个node
        return self.cache_node[self.sorted_cache_list[node_index]]
    
    # 保存文件到本地
    def save_hash_to_node(self, filename1, filename2):
        with open(filename1,"w")as f:
            json.dump(self.sorted_cache_list, f)  # 保存哈希列表到本地
        with open(filename2, "w")as f:
            json.dump(self.cache_node, f)  # 保存字典（"哈希值-设备ID"）到本地
