import json
from pathlib import Path


class GenerateConfig:

    def __init__(self):
        self.filename = f'{Path(__file__).parent}/config.json'

    def generate_config(self):
        """仅生成配置文件"""
        # DEFAULT
        config = {
            "bloggers": [
                {
                    "mark": "用户标识（可任意命名）",
                    "sec_user_id": "用户主页/user/后的ID"
                },
                {
                    "mark": "",
                    "sec_user_id": ""
                },
                {
                    "mark": "",
                    "sec_user_id": ""
                },
            ],
            # 添加更多用户
            "storage_folder": "视频存储目录路径（最好写成绝对路径）"
        }

        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        print(f"配置文件'{self.filename}'已生成")
