"""测试conf模块"""
from conf import setting
def print_setting():
    print(setting.AUTHENTICATION)

if __name__ == '__main__':
    print_setting()
    """测试通过"""