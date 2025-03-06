import json

from models.data import JSONStorage, Actor



storage = JSONStorage("main.json")

# # 清空测试文件
# storage.storage_path.write_text('{"actors": {}}')

# 生成测试数据
actors = [
    Actor(name=f"User{i}", description=f"Test user {i}")
    for i in range(5)
]

# 循环保存

storage.save_actor(actors)

print("???")

# 验证结果
data = json.loads(storage.storage_path.read_text())
assert len(data["actors"]) == 5, "应保存5个Actor"

# 清理
storage.storage_path.unlink()