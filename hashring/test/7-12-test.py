# _*_ coding:utf-8 _*_

__author__ = '苦叶子'

import unittest
import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")

# 除法函数
def div(a, b):
    return a/b
    
# 测试用例
class demoRaiseTest(unittest.TestCase):
    def test_raise(self):
        self.assertRaises(ZeroDivisionError, div, 1, 1)
        
# 主函数
if __name__ == '__main__':
    unittest.main()