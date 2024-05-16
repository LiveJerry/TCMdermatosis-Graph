import json
from neo4j import GraphDatabase

# Connect to Neo4j
driver = GraphDatabase.driver("bolt://localhost:7690", auth=("neo4j", "12345678"))

# Create nodes and relationships
with driver.session() as session:
    # 假设用户输入了以下信息
    name = str(input("输入疾病名称"))
    instance = str(input("输入治疗实例"))
    feedback = str(input("输入患者治疗反馈"))

    result = session.run("MERGE (d:Disease111 {name: $name}) RETURN d.name", name=name)
    if not result.single():
        print("输入疾病名称错误")
        driver.close()
        exit()

    session.run("MERGE (c:Treatment {name: $instance})", instance=instance)
    session.run(
        "MATCH (d:Disease111 {name: $name}), (c:Treatment {name: $instance}) "
        "CREATE (d)-[:治疗方法]->(c)",
        name=name, instance=instance)

    session.run("MERGE (d:Treatment {name: $instance})", instance=instance)
    session.run("MERGE (c:Feedback {name: $feedback})", feedback=feedback)
    session.run(
        "MATCH (d:Treatment {name: $instance}), (c:Feedback {name: $feedback}) "
        "CREATE (d)-[:治疗反馈]->(c)",
         instance=instance, feedback=feedback)

driver.close()
print("successfully")
