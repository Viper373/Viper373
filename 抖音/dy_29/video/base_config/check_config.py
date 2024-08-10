import json
from pathlib import Path
from dy_29.video.base_config.generate_config import GenerateConfig


class CheckConfig:
    def __init__(self):
        self.filename = f'{Path(__file__).parent}/config.json'
        self.generate_config = GenerateConfig()

    @staticmethod
    def validate_bloggers(bloggers):
        """验证博主列表中的每个博主格式"""
        if not isinstance(bloggers, list) or not bloggers:
            return False
        for blogger in bloggers:
            if not isinstance(blogger, dict):
                return False
            if "mark" not in blogger or "sec_user_id" not in blogger:
                return False
            if not isinstance(blogger["mark"], str) or not isinstance(blogger["sec_user_id"], str):
                return False
        return True

    def validate_config(self) -> bool:
        """验证配置文件格式是否正确"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # 验证配置文件的主要结构
                if "bloggers" in config and "storage_folder" in config:
                    # 验证博主列表
                    if not self.validate_bloggers(config["bloggers"]):
                        return False
                    # 验证存储文件夹
                    if not isinstance(config["storage_folder"], str):
                        return False
                    return True
        except (json.JSONDecodeError, FileNotFoundError):
            return False
        return False

    def check_and_generate_config(self):
        """检查配置文件是否存在和有效，如果不是，则生成默认配置"""
        if not self.validate_config():
            print(f"检测到配置文件'{self.filename}'不存在或格式错误，正在重新生成...")
            self.generate_config.generate_config()
        else:
            pass