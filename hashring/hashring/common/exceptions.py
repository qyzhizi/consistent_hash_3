# -*- coding: utf-8 -*-


class ErrorNotImplemented(Exception):
    u"""接口未实现.

    Note：这个异常类只是示例，实际接口未实现是可以直接抛NotImplemented这个内置异常的。
    """
    def __str__(self):
        return "接口未实现！"
