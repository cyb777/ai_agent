# 导入Python内置标准日志模块logging，用于日志记录
import logging
# 导入日志轮转处理器：按文件大小自动分割日志，避免单个日志文件过大
from logging.handlers import RotatingFileHandler
# 导入Path类：用于优雅、跨平台的文件/目录路径处理
from pathlib import Path

# 定义日志工具类Logger，封装全局日志配置
class Logger:
    # 类私有属性：单例模式标记，确保整个程序只创建一个日志实例，防止重复初始化
    _logger = None  

    # 类方法：无需实例化，直接通过类调用，用于获取全局日志对象
    @classmethod
    def get_logger(cls, name=__name__):
        """
        获取全局唯一的 Logger 实例（单例模式）
        :param name: 日志器名称，默认使用当前模块名 __name__
        :return: 配置好的日志实例
        """
        # 判断：如果已经创建过日志实例，直接返回，不重复创建
        if cls._logger:
            return cls._logger

        # 1. 配置日志存储路径
        # 获取当前文件的绝对路径 → 向上跳转两级目录 → 得到项目根目录
        BASE_DIR = Path(__file__).resolve().parent.parent

        # 拼接日志文件夹路径：项目根目录下的 logs 文件夹
        log_dir = BASE_DIR / "logs"
        # 创建 logs 文件夹：exist_ok=True 表示文件夹已存在则不报错
        log_dir.mkdir(exist_ok=True)

        # 拼接日志文件路径：logs 文件夹下的 app.log 日志文件
        log_file = log_dir / "app.log"

        #2. 初始化日志器
        # 创建日志器对象，name为日志器标识（默认模块名）
        logger = logging.getLogger(name)
        # 设置日志器的最低输出级别：INFO（只输出 INFO及以上级别日志：INFO/WARNING/ERROR/CRITICAL）
        logger.setLevel(logging.INFO)

        #3. 防止重复添加日志处理器
        # 判断：如果日志器还没有添加任何处理器，再执行添加操作（避免重复输出）
        if not logger.handlers:

            # 定义日志输出格式
            formatter = logging.Formatter(
                # 日志格式：时间 - 日志级别 - [日志器名称] - 日志信息
                "%(asctime)s - %(levelname)s - [%(name)s] - %(message)s"
            )

            # 4. 配置控制台日志输出
            # 创建控制台处理器：将日志输出到终端/命令行
            console_handler = logging.StreamHandler()
            # 为控制台处理器设置日志格式
            console_handler.setFormatter(formatter)

            #5. 配置文件日志输出（轮转模式）
            # 创建文件轮转处理器：按大小分割日志文件
            file_handler = RotatingFileHandler(
                log_file,                # 日志文件存储路径
                maxBytes=10 * 1024 * 1024,  # 单个日志文件最大大小：10MB
                backupCount=5,           # 最多保留5个历史日志文件
                encoding="utf-8"         # 文件编码：UTF-8，支持中文
            )
            # 为文件处理器设置日志格式
            file_handler.setFormatter(formatter)

            #6. 为日志器添加处理器
            # 将控制台处理器添加到日志器
            logger.addHandler(console_handler)
            # 将文件处理器添加到日志器
            logger.addHandler(file_handler)

        # 将创建好的日志实例赋值给类私有属性，实现单例
        cls._logger = logger
        # 返回最终配置完成的日志实例
        return logger