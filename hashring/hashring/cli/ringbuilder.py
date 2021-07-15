# -*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import sys
from sys import argv as sys_argv, exit
sys.path.append("../../")
from hashring.app.ringbuilder import RingBuilder
from hashring.app.ringbuilder import DataManager  


from hashring.common.config import Const

# 日志配置
import logging
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler(Const.LOG_FILE_NAME_RUN)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -%(lineno)d- %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class Commands(object):
    u"""命令行."""

    def __init__(self, filename):
        # 加载设备信息，初始化哈希环
        self.data_manager = DataManager(filename)
        self.data_manager.load()
        self.ring_builder = RingBuilder(self.data_manager)

    def add(self):
        u"""添加设备."""
        dev_info = input("input dev_id, dev_name, dev_weight, part_num :")
        dev_id, dev_name, dev_weight_str, part_num_str = dev_info.split()
        dev_weight = int(dev_weight_str)
        part_num = int(part_num_str)
        try:
            self.ring_builder.add_dev(dev_id, dev_name, dev_weight, part_num)
        except TypeError as e:
            logger.exception(e)
            print("Params error, add device fail")
            return -1
        print("Add device {} success".format(dev_id))
        return 0

    def update(self):  # dev_id, weight=None
        u"""更新设备.

        :param dev_id: 设备ID
        :param weight: 目标权重
        """
        dev_info = input("input dev_id, dev_weight:")
        dev_id, dev_weight_str= dev_info.split()
        dev_weight = int(dev_weight_str)
        try:
            self.ring_builder.update_dev(dev_id, dev_weight)
        except TypeError as e:
            logger.exception(e)
            print("Params error, update device fail")
            return -1
        print("Update device {} success".format(dev_id))
        return 0

    def remove(self):
        u"""删除设备."""
        dev_id = input("input dev_id that need to remove:")
        try:
            self.ring_builder.remove_dev(dev_id)
        except Exception as e:
            logger.exception(e)
            print("Params error, add device fail")
            return -1
        print("remove device {} success".format(dev_id))
        return 0

    def hash(self):
        u"""获取指定key hash到的设备."""
        hash_key_str = input("input hash key:")
        hash_key_int = int(hash_key_str)
        try:
            dev_id = self.ring_builder.hash_dev(hash_key_int)
        except Exception as e:
            logger.exception(e)
            print("Params error, from hash to dev_id fail")
            return -1
        print("the device ID is {}".format(dev_id))
        return dev_id


def main(arguments=None):
    """
    usage:
    ring-builder add/upade/remove/hash

    """
    parser = argparse.ArgumentParser(description='call func, then input params')
    parser.add_argument('function', help='add/upade/remove/hash : function name')
    args = parser.parse_args()

    # if arguments is not None:
    #     argv = arguments
    # else:
    #     argv = sys_argv

    # if len(argv) < 2:
    #     print("Invalid argument number.")
    #     exit(Const.EXIT_ERROR)

    builder_file_path = Const.DEV_INFO_JSON
    commands = Commands(builder_file_path)

    func = getattr(commands, args.function, None)  # args.function : 调用的函数
    if not func:
        print("Invalid argument.")
        exit(Const.EXIT_ERROR)

    func()
    exit(Const.EXIT_SUCCESS)
