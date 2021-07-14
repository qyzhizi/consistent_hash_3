# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
from sys import argv as sys_argv, exit
sys.path.append("../../")
from hashring.app.ringbuilder import RingBuilder
from hashring.app.ringbuilder import DataManager  


from hashring.common.config import Const
from hashring.common.config import logger


class Commands(object):
    u"""命令行."""
    data_manager = None
    ring_builder = None

    def __init__(self, filename):
        # 加载设备信息，初始化哈希环
        self.builder_file_path = filename
        Commands.data_manager = DataManager(self.builder_file_path)
        Commands.data_manager.load()
        Commands.ring_builder = RingBuilder(Commands.data_manager)


    @staticmethod
    def add():
        u"""添加设备."""
        dev_info = input("input dev_id, dev_name, dev_weight, part_num :")
        dev_id, dev_name, dev_weight_str, part_num_str = dev_info.split()
        dev_weight = int(dev_weight_str)
        part_num = int(part_num_str)
        Commands.ring_builder.add_dev(dev_id, dev_name, dev_weight, part_num)
        logger.info("Add device {} success".format(dev_id))

    @staticmethod
    def update():  # dev_id, weight=None
        u"""更新设备.

        :param dev_id: 设备ID
        :param weight: 目标权重
        """
        dev_info = input("input dev_id, dev_weight:")
        dev_id, dev_weight_str= dev_info.split()
        dev_weight = int(dev_weight_str)
        Commands.ring_builder.update_dev(dev_id, dev_weight)
        logger.info("Add device {} success".format(dev_id))

    @staticmethod
    def remove():
        u"""删除设备."""
        dev_id = input("input dev_id that need to remove:")
        Commands.ring_builder.remove_dev(dev_id)
        logger.info("remove device {} success".format(dev_id))

    # @staticmethod
    # def rebalance():
    #     u"""重新平衡."""
    #     pass

    @staticmethod
    def hash():  # def hash(key)
        u"""获取指定key hash到的设备."""
        hash_key_str = input("input hash key:")
        hash_key_int = int(hash_key_str)
        dev_id = Commands.ring_builder.hash_dev(hash_key_int)
        logger.info("the device ID is {}".format(dev_id))


def main(arguments=None):
    if arguments is not None:
        argv = arguments
    else:
        argv = sys_argv

    if len(argv) < 2:
        print("Invalid argument number.")
        exit(Const.EXIT_ERROR)

    # builder_file_path = input("input builder file:")
    builder_file_path = Const.DEV_INFO_JSON
    commands = Commands(builder_file_path)

    func = getattr(commands, argv[1], None)  # argv[1]: 函数名
    if not func:
        print("Invalid argument.")
        exit(Const.EXIT_ERROR)

    func()
    exit(Const.EXIT_SUCCESS)
