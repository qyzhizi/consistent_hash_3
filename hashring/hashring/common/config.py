class Const(object):

    DEV_ID = "dev_id"  # 设备ID
    DEV_NAME = "dev_name"  # 设备名     
    DEV_WEIGHT = "dev_weight"  # 设备权重
    PART_NUM = "part_num"  # 设备分区数
    REMOVE = False  # 删除设备标志
    ADD = True  # 添加设备标志
    MOD_NUM = 2**23  # 哈希值范围[0,2**23)
    EXIT_SUCCESS = 0 
    EXIT_ERROR = 2
    # 设备信息，用于初始化哈希环
    DEV_INFO_JSON = "/home/qy/2021-7-12-hash/hashring/data/dev_info-4.json"
    TEST_PATH = '/home/qy/2021-7-12-hash/hashring/data/dev_info-4.json'
    RELOAD_PATH = '/home/qy/2021-7-12-hash/hashring/data/dev_info.json'
    # 日志文件
    LOG_FILE_NAME_RUN = '/home/qy/2021-7-12-hash/hashring/data/log_file.txt'
    LOG_FILE_NAME_TEST = '/home/qy/2021-7-12-hash/hashring/data/log_file_test.txt'