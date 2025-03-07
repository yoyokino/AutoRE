from fastapi import APIRouter, HTTPException
from langchain_openai import ChatOpenAI

from agents.actor_agent import ActorAgent
from agents.basic_flow_agent import BasicFlowAgent
from agents.condition_agent import ConditionAgent
from agents.extended_flow_agent import ExtendedFlowAgent
from agents.user_story_agent import UserStoryAgent
from agents.utils.entity_analyzer import EntityAnalysisAgent
from models.storage import JSONStorage
from models.systemModel import Actor, UserStory

# from utils.entity_analyzer import analyze_entities
# from utils.quality_checker import quality_check

# client = ChatOpenAI(
#     model="Pro/deepseek-ai/DeepSeek-V3",
#     api_key="sk-puqduzsuowmyylabmjhimrjacmsnbkbwpzivefnpcevteuoo",
#     base_url="https://api.siliconflow.cn/v1"
# )

client = ChatOpenAI(model="gpt-4o", api_key="sk-IpLlfCLqwInStaEE6COqURZARuIVL7DfsIZMCd1UuUjJOSpC",
                    base_url="https://api.chatfire.cn/v1")

router = APIRouter()

# 初始化Agent
actor_agent = ActorAgent(llm=client)
user_story_agent = UserStoryAgent(llm=client)
condition_agent = ConditionAgent(llm=client)
basic_flow_agent = BasicFlowAgent(llm=client)
extended_flow_agent = ExtendedFlowAgent(llm=client)
entity_agent = EntityAnalysisAgent(llm=client)

storage = JSONStorage()


# actor
@router.post("/api/actors/generate")
async def generate_actors(system_desc: str):
    """生成初始参与者列表"""
    try:
        storage.update_system_description(system_desc)
        # 调用Agent生成
        raw_actors = actor_agent.generate(system_desc)
        print(raw_actors)

        # # 执行质量检测
        # if not quality_check(raw_actors, type="actor"):
        #     raise HTTPException(400, "Quality check failed")
        #
        # # 实体分析
        # entities = analyze_entities(raw_actors)

        created = []
        storage.delete_all_actors()
        for actor_data in raw_actors:
            actor = Actor(**actor_data)
            storage.add_actor(actor)
            created.append(actor.model_dump_json())

        return {"actors": storage.get_actors(), }
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/api/actors/get")
async def get_all_actors():
    actors = storage.get_actors()
    return {"actors": actors}


@router.post("/api/actors/delete")
async def delete_actor(actor: str):
    storage.delete_actor(actor)
    actors = storage.get_actors()
    return {"actors": actors}


@router.post("/api/actors/add")
async def add_actor(actor: dict):
    storage.add_actor(Actor(**actor))
    return {"actors": storage.get_actors()}


@router.post("/api/actors/update")
async def update_actor(old_actor: dict, new_actor: dict):
    storage.update_actor(Actor(**old_actor), Actor(**new_actor))
    return {"actors": storage.get_actors()}


# user_story
@router.post("/api/user_story/generate")
async def generate_user_stories(actor: dict):
    try:
        # 调用Agent生成
        raw_user_stories = user_story_agent.generate(storage.get_system_description(), storage.get_actors(), actor)
        print(raw_user_stories)

        # # 执行质量检测
        # if not quality_check(raw_actors, type="actor"):
        #     raise HTTPException(400, "Quality check failed")
        #
        # # 实体分析
        # entities = analyze_entities(raw_actors)

        storage.delete_all_user_stories(actor["actor"])

        for user_story_data in raw_user_stories:
            user_story = UserStory(**user_story_data)
            storage.add_user_story(actor["actor"], user_story)

        return {"user_stories": raw_user_stories, }
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/api/user_story/generate_all")
async def generate_all_user_stories():
    try:
        actors = storage.get_actors()
        # 调用Agent生成
        for actor in actors:
            raw_user_stories = user_story_agent.generate(storage.get_system_description(), storage.get_actors(), actor)
            print(raw_user_stories)

            storage.delete_all_user_stories(actor["actor"])

            for user_story_data in raw_user_stories:
                user_story = UserStory(**user_story_data)
                storage.add_user_story(actor["actor"], user_story)

        # # 执行质量检测
        # if not quality_check(raw_actors, type="actor"):
        #     raise HTTPException(400, "Quality check failed")
        #
        # # 实体分析
        # entities = analyze_entities(raw_actors)

        return {"actors": storage.get_actors(), }
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/api/user_story/regenerate")
async def regenerate_user_stories(actor: dict, old_user_story: dict, suggestion: str):
    try:

        # 调用Agent生成
        new_user_story = user_story_agent.regenerate(storage.get_system_description(), storage.get_actors(), actor,
                                                     old_user_story, suggestion)
        print(new_user_story)

        # # 执行质量检测
        # if not quality_check(raw_actors, type="actor"):
        #     raise HTTPException(400, "Quality check failed")
        #
        # # 实体分析
        # entities = analyze_entities(raw_actors)

        # storage.update_user_story(actor["actor"], UserStory(**old_user_story), UserStory(**new_user_story))

        return {"new_user_story": new_user_story}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/api/user_story/update")
async def update_user_story(actor: dict, old_user_story: dict, new_user_story: dict):
    try:
        # # 执行质量检测
        # if not quality_check(raw_actors, type="actor"):
        #     raise HTTPException(400, "Quality check failed")
        #
        # # 实体分析
        # entities = analyze_entities(raw_actors)

        print(storage.update_user_story(actor["actor"], UserStory(**old_user_story), UserStory(**new_user_story)))

        return {"actors": storage.get_actors(), }
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/api/user_story/add")
async def add_user_story(actor: str, new_user_story: dict):
    try:
        # # 执行质量检测
        # if not quality_check(raw_actors, type="actor"):
        #     raise HTTPException(400, "Quality check failed")
        #
        # # 实体分析
        # entities = analyze_entities(raw_actors)

        storage.add_user_story(actor, UserStory(**new_user_story))

        return {"actors": storage.get_actors(), }
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/api/user_story/delete")
async def delete_user_story(actor: str, old_user_story: dict):
    try:
        storage.delete_user_story(actor, UserStory(**old_user_story).user_story)

        return {"actors": storage.get_actors(), }
    except Exception as e:
        raise HTTPException(500, str(e))


# condition
@router.post("/api/condition/generate")
async def generate_conditions(actor: dict, user_story: dict):
    try:
        print(user_story)
        conditions = condition_agent.generate(storage.get_system_description(), storage.get_entities(), actor,
                                              user_story)

        storage.add_condition(actor["actor"], user_story, conditions)

        print(conditions)

        return conditions

    except Exception as e:
        raise HTTPException(500, str(e))


# condition
@router.post("/api/condition/generate_all")
async def generate_all_conditions(actor: dict):
    try:
        print(actor)
        user_stories = storage.get_user_stories(actor_name=actor["actor"])
        print(user_stories, actor)
        for user_story in user_stories:
            conditions = condition_agent.generate(storage.get_system_description(), storage.get_entities(), actor,
                                                  user_story)

            storage.add_condition(actor["actor"], user_story, conditions)

            print(conditions)

        return {"message": "All Conditions Generated Successfully!"}

    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/api/condition/regenerate")
async def regenerate_condition(actor: dict, user_story: dict, old_condition: dict, suggestion: str):
    try:
        new_condition = condition_agent.regenerate(storage.get_system_description(), storage.get_entities(), actor,
                                                   user_story, old_condition,
                                                   suggestion)

        # storage.delete_condition(actor["actor"], user_story)
        # storage.add_condition(actor["actor"], user_story, new_condition)

        return {"new_condition": new_condition}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/api/condition/delete")
async def delete_condition(actor: str, user_story: dict):
    try:
        storage.delete_condition(actor, user_story)
        return {"message": "Condition deleted successfully"}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/api/condition/update")
async def update_condition(actor: str, user_story: dict, new_condition: dict):
    try:
        storage.delete_condition(actor, user_story)
        storage.add_condition(actor, user_story, new_condition)
        return {"message": "Condition updated successfully"}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/api/basic_flow/generate")
async def generate_basic_flow(actor: dict, user_story: dict):
    """生成基本流程"""
    try:
        system_desc = storage.get_system_description()

        flow_steps = basic_flow_agent.generate(system_desc=system_desc, entities=storage.get_entities(), actor=actor,
                                               user_story=user_story)

        storage.delete_all_basic_flow(actor["actor"], user_story)

        # 保存生成的步骤
        for step in flow_steps:
            storage.add_basic_flow(actor["actor"], user_story, step)

        return flow_steps
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/api/basic_flow/regenerate_all")
async def regenerate_basic_flow_step(actor: dict, user_story: dict, old_steps: list[str], suggestion: str):
    """重新生成所有步骤"""
    try:
        system_desc = storage.get_system_description()

        new_steps = basic_flow_agent.regenerate(system_desc=system_desc, entities=storage.get_entities(), actor=actor,
                                                user_story=user_story,
                                                old_steps=old_steps, suggestion=suggestion)

        # 更新步骤
        # storage.update_basic_flow_step(actor["actor"], user_story, new_steps)
        return new_steps
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/api/basic_flow/regenerate")
async def regenerate_one_basic_flow_step(actor: dict, user_story: dict, old_step: str, suggestion: str):
    """重新生成单个步骤"""
    try:
        system_desc = storage.get_system_description()

        new_step = basic_flow_agent.regenerate_one_step(system_desc=system_desc, entities=storage.get_entities(),
                                                        actor=actor, user_story=user_story,
                                                        old_step=old_step, suggestion=suggestion)

        # 更新步骤
        # storage.update_basic_flow_step(actor["actor"], user_story, new_step)
        return new_step
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/api/basic_flow/delete")
async def delete_basic_flow_step(actor_name: str, user_story: dict, step: str):
    """删除指定步骤"""
    try:
        storage.delete_basic_flow(actor_name, user_story, step)
        return {"message": "Basic flow step deleted successfully"}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/api/basic_flow/update_all")
async def update_basic_flow_step(actor_name: str, user_story: dict, flow_steps: list[str]):
    """更新步骤"""
    try:
        storage.update_basic_flow_step(actor_name, user_story, flow_steps)
        return {"message": "All basic flow step updated successfully"}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/api/basic_flow/update")
async def update_basic_flow_step(actor_name: str, user_story: dict, old_step: str, new_step: str):
    """更新步骤"""
    try:
        storage.update_one_basic_flow_step(actor_name, user_story, old_step, new_step)
        return {"message": "Basic flow step updated successfully"}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/api/extended_flow/generate")
async def generate_extended_flow(actor: dict, user_story: dict):
    """生成拓展流程"""
    try:
        system_desc = storage.get_system_description()

        flows = extended_flow_agent.generate(system_desc=system_desc, entities=storage.get_entities(), actor=actor,
                                             user_story=user_story)

        storage.delete_all_extended_flow(actor["actor"], user_story)

        # 保存生成的步骤
        for flow in flows:
            storage.add_extended_flow(actor["actor"], user_story, flow)

        return flows
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/api/extended_flow/regenerate")
async def regenerate_one_extended_flow(actor: dict, user_story: dict, old_flow: dict, suggestion: str):
    """重新生成单个拓展流程"""
    try:
        system_desc = storage.get_system_description()

        new_flow = extended_flow_agent.regenerate(system_desc=system_desc, entities=storage.get_entities(), actor=actor,
                                                  user_story=user_story,
                                                  old_flow=old_flow, suggestion=suggestion)
        return new_flow
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/api/extended_flow/delete")
async def delete_extended_flow(actor_name: str, user_story: dict, flow: dict):
    """删除指定拓展流程"""
    try:
        storage.delete_extended_flow(actor_name, user_story, flow)
        return {"message": "Extended flow deleted successfully"}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/api/extended_flow/update")
async def update_extended_flow(actor_name: str, user_story: dict, old_flow: dict, new_flow: dict):
    """更新单个拓展流程"""
    try:
        storage.update_extended_flow(actor_name, user_story, old_flow, new_flow)
        return {"message": "Extended flow updated successfully"}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/api/entity/generate")
async def generate_entities(actors: list[dict]):
    """基于系统描述和用户故事自动生成实体"""
    try:
        system_desc = storage.get_system_description()

        entities = entity_agent.generate(system_desc=system_desc, actors=actors)

        print(entities)

        storage.delete_all_entity()

        # 保存生成的实体
        for entity in entities:
            storage.add_entity(entity)

        return entities
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/api/entity/regenerate_one")
async def regenerate_entity(entity: dict, suggestion: str):
    """基于系统描述和用户故事重新生成实体"""
    try:
        system_desc = storage.get_system_description()
        actors = storage.get_actors()

        new_entity = entity_agent.regenerate_one(system_desc=system_desc, actors=actors, entity=entity,
                                                 suggestion=suggestion)

        print(new_entity)
        return new_entity
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/api/entity/regenerate_new_one")
async def add_entity(suggestion: str):
    """生成一个新实体"""
    try:
        system_desc = storage.get_system_description()
        actors = storage.get_actors()
        entities = storage.get_entities()
        new_entity = entity_agent.add_one(system_desc=system_desc, actors=actors, entities=entities,
                                          suggestion=suggestion)
        return new_entity
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/api/entity/add")
async def add_entity(entity: dict):
    """添加新实体"""
    try:
        return storage.add_entity(entity)
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/api/entity/all")
async def get_all_entities():
    """获取所有实体"""
    try:
        return storage.get_entities()
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/api/entity/update")
async def update_entity(entity_name: str, entity: dict):
    """更新实体"""
    try:
        return storage.update_entity(entity_name, entity)
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/api/entity/delete")
async def delete_entity(entity_name: str):
    """删除实体"""
    try:
        storage.delete_entity(entity_name)
        return {"message": f"Entity '{entity_name}' deleted successfully"}
    except Exception as e:
        raise HTTPException(500, str(e))
