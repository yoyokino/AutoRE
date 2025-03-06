import json
import threading
from pathlib import Path

from fastapi import HTTPException

from models.systemModel import Actor, UserStory


class JSONStorage:
    def __init__(self, file_path: str = "data"):
        self._lock = threading.Lock()
        self.storage_path = Path(file_path)
        self.storage_path.mkdir(exist_ok=True)

        # 主数据文件
        self.data_file = self.storage_path / "main.json"

    def _load_data(self) -> dict:
        with self._lock:
            for _ in range(3):  # 重试机制
                try:
                    with open(self.data_file, 'r') as f:
                        data = json.load(f)
                        if "system_description" not in data:
                            data["system_description"] = ""
                        if "actors" not in data:
                            data["actors"] = []
                        if "entities" not in data:
                            data["entities"] = []
                        return data
                except json.JSONDecodeError:
                    raise HTTPException(500, "数据文件损坏")

    def _save_data(self, data: dict):
        temp_file = self.data_file.with_suffix(".tmp")
        with self._lock:
            temp_file.write_text(json.dumps(data, indent=2))
            temp_file.replace(self.data_file)

    # Actor 操作
    def add_actor(self, actor: Actor):
        data = self._load_data()

        # 将Pydantic模型转换为字典
        actor_dict = json.loads(actor.model_dump_json())
        # 查找是否已存在同名Actor
        existing_index = next((
            i for i, a in enumerate(data["actors"])
            if a["actor"] == actor_dict["actor"]
        ), None)
        # 更新或添加
        if existing_index is not None:
            data["actors"][existing_index] = actor_dict
        else:
            data["actors"].append(actor_dict)

        self._save_data(data)
        return actor

    def update_actor(self, actor0: Actor, actor1: Actor):
        data = self._load_data()

        # 将Pydantic模型转换为字典
        actor_dict = json.loads(actor0.model_dump_json())
        # 查找是否已存在同名Actor
        existing_index = next((
            i for i, a in enumerate(data["actors"])
            if a["actor"] == actor_dict["actor"]
        ), None)
        # 更新或添加
        if existing_index is not None:
            data["actors"][existing_index] = json.loads(actor1.model_dump_json())

        self._save_data(data)
        return actor1

    def get_actors(self):
        data = self._load_data()
        return data["actors"]

    def delete_all_actors(self):
        data = self._load_data()
        data["actors"] = []
        self._save_data(data)
        return data["actors"]

    def delete_actor(self, actor: str):
        data = self._load_data()

        # 使用列表推导式创建新列表（过滤掉目标actor）
        original_length = len(data["actors"])
        data["actors"] = [
            a for a in data["actors"]
            if a is not None and a.get("actor") != actor
        ]

        # 只有当列表长度变化时才保存
        if len(data["actors"]) < original_length:
            self._save_data(data)
            return True
        return False

    # System_Description操作
    def get_system_description(self):
        data = self._load_data()
        return data["system_description"]

    def update_system_description(self, system_description: str):
        data = self._load_data()
        data["system_description"] = system_description
        self._save_data(data)
        return self.get_system_description()

    # UserStory 操作 ------------------------------------------------------
    def add_user_story(self, actor_name: str, user_story: UserStory):
        data = self._load_data()

        # 查找目标Actor
        target_actor = next((a for a in data["actors"] if a["actor"] == actor_name), None)
        if not target_actor:
            raise HTTPException(404, f"Actor '{actor_name}' not found")

        # 转换模型为字典
        story_dict = json.loads(user_story.model_dump_json())

        # 检查是否已存在同名用户故事
        existing_idx = next((
            i for i, s in enumerate(target_actor["user_stories"])
            if s["user_story"] == story_dict["user_story"]
        ), None)

        # 更新或添加
        if existing_idx is not None:
            target_actor["user_stories"][existing_idx] = story_dict
        else:
            target_actor["user_stories"].append(story_dict)

        self._save_data(data)
        return user_story

    def update_user_story(self, actor_name: str, user_story0: UserStory, user_story1: UserStory):
        data = self._load_data()

        # 查找目标Actor
        target_actor = next((a for a in data["actors"] if a["actor"] == actor_name), None)
        if not target_actor:
            raise HTTPException(404, f"Actor '{actor_name}' not found")

        # 转换模型为字典
        story_dict = json.loads(user_story0.model_dump_json())

        for i in target_actor["user_stories"]:
            print(i["user_story"])

        print(story_dict["user_story"])

        # 检查是否已存在同名用户故事
        existing_idx = next((
            i for i, s in enumerate(target_actor["user_stories"])
            if s["user_story"] == story_dict["user_story"]
        ), None)

        # 更新或添加
        if existing_idx is not None:
            target_actor["user_stories"][existing_idx] = json.loads(user_story1.model_dump_json())

        self._save_data(data)
        return user_story1

    def get_user_stories(self, actor_name: str):
        """获取指定Actor的全部用户故事"""
        data = self._load_data()
        actor = next((a for a in data["actors"] if a["actor"] == actor_name), None)
        if not actor:
            raise HTTPException(404, f"Actor '{actor_name}' not found")
        return actor.get("user_stories", [])

    def delete_all_user_stories(self, actor_name: str):
        """清空指定Actor的用户故事"""
        data = self._load_data()
        actor = next((a for a in data["actors"] if a["actor"] == actor_name), None)
        if not actor:
            raise HTTPException(404, f"Actor '{actor_name}' not found")

        original_count = len(actor.get("user_stories", []))
        actor["user_stories"] = []

        if original_count > 0:
            self._save_data(data)
            return True
        return False

    def delete_user_story(self, actor_name: str, story_title: str):
        """根据用户故事标题删除指定条目"""
        data = self._load_data()
        actor = next((a for a in data["actors"] if a["actor"] == actor_name), None)
        if not actor:
            raise HTTPException(404, f"Actor '{actor_name}' not found")

        # 过滤掉目标story
        original_stories = actor.get("user_stories", [])
        new_stories = [s for s in original_stories if s["user_story"] != story_title]

        # 判断是否有变化
        if len(new_stories) < len(original_stories):
            actor["user_stories"] = new_stories
            self._save_data(data)
            return True
        return False

    # Pre-Condition/Post-Condition 操作
    def add_condition(self, actor_name: str, user_story: dict, condition: dict):
        data = self._load_data()
        target_actor = next((a for a in data["actors"] if a["actor"] == actor_name), None)
        if not target_actor:
            raise HTTPException(404, f"Actor '{actor_name}' not found")

        target_story = next((s for s in target_actor["user_stories"]
                             if s["user_story"] == user_story.get("user_story")), None)
        if not target_story:
            raise HTTPException(404, "User story not found")

        target_story["pre_condition"] = (condition.get("pre_condition"))
        target_story["post_condition"] = (condition.get("post_condition"))
        self._save_data(data)

    def delete_condition(self, actor_name: str, user_story: dict):
        data = self._load_data()
        target_actor = next((a for a in data["actors"] if a["actor"] == actor_name), None)
        if not target_actor:
            raise HTTPException(404, f"Actor '{actor_name}' not found")

        target_story = next((s for s in target_actor["user_stories"]
                             if s["user_story"] == user_story.get("user_story")), None)
        if not target_story:
            raise HTTPException(404, "User story not found")

        target_story["pre_condition"] = None
        target_story["post_condition"] = None
        self._save_data(data)

    def add_basic_flow(self, actor_name: str, user_story: dict, flow_step: str):
        """添加基本流程步骤"""
        data = self._load_data()
        target_actor = next((a for a in data["actors"] if a["actor"] == actor_name), None)
        if not target_actor:
            raise HTTPException(404, f"Actor '{actor_name}' not found")

        target_story = next((s for s in target_actor["user_stories"]
                             if s["user_story"] == user_story.get("user_story")), None)
        if not target_story:
            raise HTTPException(404, "User story not found")

        # 添加步骤编号
        target_story["basic_flow"].append(flow_step)
        self._save_data(data)
        return flow_step

    def delete_basic_flow(self, actor_name: str, user_story: dict, step: str):
        """删除指定步骤"""
        data = self._load_data()
        target_actor = next((a for a in data["actors"] if a["actor"] == actor_name), None)
        if not target_actor:
            raise HTTPException(404, f"Actor '{actor_name}' not found")

        target_story = next((s for s in target_actor["user_stories"]
                             if s["user_story"] == user_story.get("user_story")), None)
        if not target_story:
            raise HTTPException(404, "User story not found")

        # 删除指定步骤并重新编号
        target_story["basic_flow"] = [
            f for f in target_story["basic_flow"] if f != step
        ]

        self._save_data(data)

    def delete_all_basic_flow(self, actor_name: str, user_story: dict):
        """删除指定步骤"""
        data = self._load_data()
        target_actor = next((a for a in data["actors"] if a["actor"] == actor_name), None)
        if not target_actor:
            raise HTTPException(404, f"Actor '{actor_name}' not found")

        target_story = next((s for s in target_actor["user_stories"]
                             if s["user_story"] == user_story.get("user_story")), None)
        if not target_story:
            raise HTTPException(404, "User story not found")

        # 删除所有步骤
        target_story["basic_flow"] = []

        self._save_data(data)

    def update_basic_flow_step(self, actor_name: str, user_story: dict, new_steps: list[str]):
        """修改指定步骤"""
        data = self._load_data()
        target_actor = next((a for a in data["actors"] if a["actor"] == actor_name), None)
        if not target_actor:
            raise HTTPException(404, f"Actor '{actor_name}' not found")

        target_story = next((s for s in target_actor["user_stories"]
                             if s["user_story"] == user_story.get("user_story")), None)
        if not target_story:
            raise HTTPException(404, "User story not found")

        target_story["basic_flow"] = new_steps

        self._save_data(data)
        pass

    def update_one_basic_flow_step(self, actor_name: str, user_story: dict, old_step: str, new_step: str):
        """修改指定步骤"""
        data = self._load_data()
        target_actor = next((a for a in data["actors"] if a["actor"] == actor_name), None)
        if not target_actor:
            raise HTTPException(404, f"Actor '{actor_name}' not found")

        target_story = next((s for s in target_actor["user_stories"]
                             if s["user_story"] == user_story.get("user_story")), None)
        if not target_story:
            raise HTTPException(404, "User story not found")

        # 找到指定步骤
        existing_idx = next((
            i for i, s in enumerate(target_story["basic_flow"])
            if s == old_step
        ), None)

        # 更新或添加
        if existing_idx is not None:
            target_story["basic_flow"][existing_idx] = new_step

        self._save_data(data)

    def add_extended_flow(self, actor_name: str, user_story: dict, flow: dict):
        """添加拓展流程"""
        data = self._load_data()
        target_actor = next((a for a in data["actors"] if a["actor"] == actor_name), None)
        if not target_actor:
            raise HTTPException(404, f"Actor '{actor_name}' not found")

        target_story = next((s for s in target_actor["user_stories"]
                             if s["user_story"] == user_story.get("user_story")), None)
        if not target_story:
            raise HTTPException(404, "User story not found")

        # 添加步骤编号
        target_story["extended_flow"].append(flow)
        self._save_data(data)
        return flow

    def delete_extended_flow(self, actor_name: str, user_story: dict, flow: dict):
        """删除指定拓展流程"""
        data = self._load_data()
        target_actor = next((a for a in data["actors"] if a["actor"] == actor_name), None)
        if not target_actor:
            raise HTTPException(404, f"Actor '{actor_name}' not found")

        target_story = next((s for s in target_actor["user_stories"]
                             if s["user_story"] == user_story.get("user_story")), None)
        if not target_story:
            raise HTTPException(404, "User story not found")

        # 删除指定步骤并重新编号
        target_story["extended_flow"] = [
            f for f in target_story["extended_flow"] if f["title"] != flow["title"]
        ]

        self._save_data(data)

    def delete_all_extended_flow(self, actor_name: str, user_story: dict):
        """删除所有拓展流程"""
        data = self._load_data()
        target_actor = next((a for a in data["actors"] if a["actor"] == actor_name), None)
        if not target_actor:
            raise HTTPException(404, f"Actor '{actor_name}' not found")

        target_story = next((s for s in target_actor["user_stories"]
                             if s["user_story"] == user_story.get("user_story")), None)
        if not target_story:
            raise HTTPException(404, "User story not found")

        target_story["extended_flow"] = []

        self._save_data(data)

    def update_extended_flow(self, actor_name: str, user_story: dict, old_flow: dict, new_flow: dict):
        """修改指定步骤"""
        data = self._load_data()
        target_actor = next((a for a in data["actors"] if a["actor"] == actor_name), None)
        if not target_actor:
            raise HTTPException(404, f"Actor '{actor_name}' not found")

        target_story = next((s for s in target_actor["user_stories"]
                             if s["user_story"] == user_story.get("user_story")), None)
        if not target_story:
            raise HTTPException(404, "User story not found")

        # 找到指定步骤
        existing_idx = next((
            i for i, s in enumerate(target_story["extended_flow"])
            if s["title"] == old_flow["title"]
        ), None)

        # 更新或添加
        if existing_idx is not None:
            target_story["extended_flow"][existing_idx] = new_flow

        self._save_data(data)

    # entity
    def add_entity(self, entity: dict):
        """添加实体"""
        data = self._load_data()

        # 检查实体是否已存在
        existing_entity = next((e for e in data["entities"] if e["entity"] == entity["entity"]), None)
        if existing_entity:
            raise HTTPException(400, f"Entity already exists")

        # 添加新实体
        data["entities"].append(entity)
        self._save_data(data)
        return entity

    def get_entities(self):
        """获取所有实体"""
        data = self._load_data()
        return data.get("entities", [])

    def delete_all_entity(self):
        data = self._load_data()
        data["entities"] = []
        self._save_data(data)
        return data["entities"]

    def get_entity(self, entity_name: str):
        """获取指定实体"""
        data = self._load_data()
        entity = next((e for e in data["entities"] if e["entity"] == entity_name), None)
        if not entity:
            raise HTTPException(404, f"Entity '{entity_name}' not found")
        return entity

    def update_entity(self, entity_name: str, entity: dict):
        """更新实体"""
        data = self._load_data()
        entity_index = next((i for i, e in enumerate(data["entities"]) if e["entity"] == entity_name), None)
        if entity_index is None:
            raise HTTPException(404, f"Entity '{entity_name}' not found")

        # 更新实体，保持原有属性
        data["entities"][entity_index] = entity
        self._save_data(data)
        return entity

    def delete_entity(self, entity_name: str):
        """删除实体"""
        data = self._load_data()
        entity = next((e for e in data["entities"] if e["entity"] == entity_name), None)
        if not entity:
            raise HTTPException(404, f"Entity '{entity_name}' not found")

        data["entities"] = [e for e in data["entities"] if e["entity"] != entity_name]
        self._save_data(data)

    def add_entity_attribute(self, entity_name: str, attribute: dict):
        """添加实体属性"""
        data = self._load_data()
        entity = next((e for e in data["entities"] if e["entity"] == entity_name), None)
        if not entity:
            raise HTTPException(404, f"Entity '{entity_name}' not found")

        # 检查属性是否已存在
        existing_attr = next((a for a in entity.get("attributes", [])
                              if a["content"] == attribute["content"]), None)
        if existing_attr:
            raise HTTPException(400, f"Attribute already exists")

        # 添加新属性
        if "attributes" not in entity:
            entity["attributes"] = []
        entity["attributes"].append(attribute)
        self._save_data(data)
        return attribute

    def update_entity_attribute(self, entity_name: str, old_content: str, attribute: dict):
        """更新实体属性"""
        data = self._load_data()
        entity = next((e for e in data["entities"] if e["entity"] == entity_name), None)
        if not entity:
            raise HTTPException(404, f"Entity '{entity_name}' not found")

        # 检查属性是否存在
        attr_index = next((i for i, a in enumerate(entity.get("attributes", []))
                           if a["content"] == old_content), None)
        if attr_index is None:
            raise HTTPException(404, f"Attribute '{old_content}' not found in entity '{entity_name}'")

        # 更新属性
        entity["attributes"][attr_index] = attribute
        self._save_data(data)
        return attribute

    def delete_entity_attribute(self, entity_name: str, attribute_content: str):
        """删除实体属性"""
        data = self._load_data()
        entity = next((e for e in data["entities"] if e["entity"] == entity_name), None)
        if not entity:
            raise HTTPException(404, f"Entity '{entity_name}' not found")

        if "attributes" not in entity:
            raise HTTPException(404, f"Attribute '{attribute_content}' not found in entity '{entity_name}'")

        # 检查属性是否存在
        attr = next((a for a in entity["attributes"] if a["content"] == attribute_content), None)
        if not attr:
            raise HTTPException(404, f"Attribute '{attribute_content}' not found in entity '{entity_name}'")

        # 删除属性
        entity["attributes"] = [a for a in entity["attributes"] if a["content"] != attribute_content]
        self._save_data(data)

    def get_entity_attributes(self, entity_name: str):
        """获取实体的所有属性"""
        data = self._load_data()
        entity = next((e for e in data["entities"] if e["entity"] == entity_name), None)
        if not entity:
            raise HTTPException(404, f"Entity '{entity_name}' not found")

        return entity.get("attributes", [])

