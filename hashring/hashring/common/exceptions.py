# -*- coding: utf-8 -*-


class ErrorNotImplemented(Exception):
    u"""接口未实现.

    Note：这个异常类只是示例，实际接口未实现是可以直接抛NotImplemented这个内置异常的。
    """
    def __str__(self):
        return "接口未实现！"


class ErrorInvalidPara(Exception):
    """
    非法输入参数
    """
    def __init__(self, print_str):
        self.print_str = print_str

    def __str__(self):
        return self.print_str


class ErrorFile(Exception):
    """
    文件内容为空
    """
    def __init__(self, print_str):
        self.print_str = print_str

    def __str__(self):
        return self.print_str