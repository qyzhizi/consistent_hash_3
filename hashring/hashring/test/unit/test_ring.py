# -*- coding: utf-8 -*-
import unittest
import json
import sys
sys.path.append("../../../")

from hashring.app.ringbuilder import RingBuilder
from hashring.app.ringbuilder import DataManager  
from hashring.app.ringbuilder import get_hash  
from hashring.common import exceptions as exc
from hashring.common.config import Const
# from hashring.common.config import logger

import logging
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler(Const.LOG_FILE_NAME_RUN)  #  log file
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -%(lineno)d- %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class TestRingBase(unittest.TestCase):
    u"""测试基类."""

    def setUp(self):
        pass

    def tearDown(self):
        pass


class TestRingData(unittest.TestCase):
    u"""ring测试类."""

    def setUp(self):
        # 将设备信息加载到用于测试的文件
        self.test_path = Const.TEST_PATH
        self.reload_path = Const.RELOAD_PATH
        self.reload_dev_info(self.reload_path, self.test_path)
        # 加载测试的文件,构建实例
        self.data_manager = DataManager(self.test_path)
        self.data_manager.load()

    def tearDown(self):
        # 加载原来的设备信息,恢复测试文件
        self.reload_dev_info(self.reload_path, self.test_path)

    def reload_dev_info(self, reload_path,test_path):        
        with open(reload_path) as f:
            reload_dev_info = json.load(f)
        with open(test_path, "w") as f:
            json.dump(reload_dev_info, f)

    def test_add_dev(self):
        """添加设备接口.

        测试点：判断接口是否抛指定异常
        注意：单测案例为示例，增加具体逻辑后需修改
        """
        logger.info("run test_add_dev")
        actual_res = RingBuilder(self.data_manager).add_dev(dev_id="5", 
                                                    dev_name="dev_5",
                                                    dev_weight=1,
                                                    part_num=3)
        self.assertEqual(actual_res, Const.EXIT_SUCCESS)

    def test_remove_dev(self):
        """删除设备接口.

        测试点：检查接口返回值是否为空
        注意：单测案例为示例，增加具体逻辑后需修改
        """
        logger.info("run test_remove_dev")
        actual_res = RingBuilder(self.data_manager).remove_dev("2")  # "2" : 表示设备ID
        self.assertEqual(actual_res, Const.EXIT_SUCCESS)
    
    def test_update_dev(self):
        """更新设备信息
        测试点：检查接口返回值是否为空
        注意：单测案例为示例，增加具体逻辑后需修改
        """
        logger.info("run test_update_dev")
        actual_res = RingBuilder(self.data_manager).update_dev("2", 2)  # "2" : 表示设备ID
        self.assertEqual(actual_res, Const.EXIT_SUCCESS)

    def test_hash_dev(self):
        """hash设备接口.

        测试点：检查hash结果是否符合预期
        注意：单测案例为示例，增加具体逻辑后需修改
        """
        logger.info("run test_hash_dev")
        actual_res = RingBuilder(self.data_manager).hash_dev(get_hash("2_1"))  # "2_1": 表示虚拟设备
        self.assertEqual(actual_res, "2")  # "2"表示设备ID


if __name__ == '__main__':
    unittest.main()
