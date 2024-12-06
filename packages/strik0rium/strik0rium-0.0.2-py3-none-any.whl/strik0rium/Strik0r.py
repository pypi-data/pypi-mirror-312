class Strik0r(object):
    _instance = None  # 用于存储唯一实例

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Strik0r, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # 避免重复初始化
        if not hasattr(self, "initialized"):
            self.name = 'Strik0r'
            self.age = 22
            self.email = 'strik0rium@gmail.com'
            self.initialized = True  # 标志已经初始化

    def hello(self):
        print("Hello, I'm Strik0r.")