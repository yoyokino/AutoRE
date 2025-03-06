import json
import threading
import time
from pathlib import Path
from typing import Dict, List, Optional
from pydantic import BaseModel
import uuid
from datetime import datetime
from fastapi import HTTPException


# 数据模型
class UserStory(BaseModel):
    id: str = str(uuid.uuid4())
    description: str
    pre_conditions: List[str] = []
    post_conditions: List[str] = []
    basic_flow: List[dict] = []
    extended_flow: List[dict] = []


class Actor(BaseModel):
    # id: str = str(uuid.uuid4())
    name: str
    description: str
    user_stories: List[UserStory] = []


class SystemEntity(BaseModel):
    id: str = str(uuid.uuid4())
    name: str
    description: str
    type: str  # Actor/Operation/DataStore等
    attributes: dict = {}
    relations: List[str] = []


# JSON存储核心类
class JSONStorage:
    def __init__(self, file_path: str = "data"):
        self._lock = threading.Lock()
        self.storage_path = Path(file_path)
        self.storage_path.mkdir(exist_ok=True)

        # 主数据文件
        self.data_file = self.storage_path / "main.json"
        # 版本历史目录
        self.version_dir = self.storage_path / "versions"
        self.version_dir.mkdir(exist_ok=True)

    def _load_data(self) -> dict:
        with self._lock:
            for _ in range(3):  # 重试机制
                try:
                    with open(self.data_file, 'r') as f:
                        return json.load(f)
                except json.JSONDecodeError:
                    raise HTTPException(500, "数据文件损坏")


    def _save_data(self, data: dict):
        """保存主数据（带原子写入保障）"""
        temp_file = self.data_file.with_suffix(".tmp")
        with self._lock:
            temp_file.write_text(json.dumps(data, indent=2))
            temp_file.replace(self.data_file)  # 原子替换
        # except Exception as e:
        #     temp_file.unlink(missing_ok=True)
        #     raise HTTPException(500, f"保存失败: {str(e)}")

    # Actor 操作
    def get_actor(self, actor_id: str) -> Optional[Actor]:
        data = self._load_data()
        actor_data = data["actors"].get(actor_id)
        return Actor(**actor_data) if actor_data else None

    def save_actor(self, actor: Actor):
        data = self._load_data()

        # 更新数据
        data["actors"] = json.loads(actor.model_dump_json())
        self._save_data(data)
        return actor

    def save_actors(self, actor: Actor):
        data = self._load_data()

        # 更新数据
        data["actors"] = json.loads(actor.model_dump_json())
        self._save_data(data)
        return actor

    def delete_actor(self, actor_id: str):
        data = self._load_data()

        if actor_id in data["actors"]:
            # 保存删除记录
            del data["actors"][actor_id]
            self._save_data(data)
            return True
        return False

    # UserStory 操作
    def link_user_story(self, actor_id: str, story: UserStory):
        actor = self.get_actor(actor_id)
        if not actor:
            raise HTTPException(404, "Actor不存在")

        actor.user_stories.append(story)
        actor.updated_at = datetime.now()
        return self.save_actor(actor)

