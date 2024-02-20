# 加载配置文件
import configparser
from config import ROOT_PSTH

config_path = ROOT_PSTH + 'config/config.ini'
global_config = configparser.ConfigParser()
global_config.read(config_path) # 全局配置

# 当前配置
FRP_PATH = global_config.get('frp', 'root_path')
DEFAULT_ROOT_PATH = global_config.get('default', 'root_path')
