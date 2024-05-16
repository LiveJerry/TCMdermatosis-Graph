import json
from neo4j import GraphDatabase

# Connect to Neo4j
driver = GraphDatabase.driver("bolt://localhost:7690", auth=("neo4j", "12345678"))

# Read json file
with open('E:/MathModel/Graph/ZhenJun.json', 'r', encoding='gbk') as f:
    data = json.loads(f.read())

# Create nodes and relationships
with driver.session() as session:
    for item in data:
        name = item['疾病名称']
        # 创建疾病节点
        session.run("MERGE (d:Disease111 {name: $name})", name=name)

        # 获取其他信息
        location_list = item['病发部位']
        population_list = item['易发群体']
        season_list = item['易发季节']
        symptom_list = item['临床表现']
        diagnosis_list = item['诊断']
        treatment_list = item['治疗方法']
        prescription_list = item['药方']
        differentiation_list = item['辩证']
        prevention_list = item['预防']
        cause_list = item['病因']  # 从item中获取病因列表

        # 处理病因，如果有多个值，则拆分建立节点和关系，单个值直接处理
        if isinstance(cause_list, list):
            for cause in cause_list:
                # 建立节点
                session.run("MERGE (c:Cause {name: $cause})", cause=cause.strip())
                # 建立关系
                session.run(
                    "MATCH (d:Disease111 {name: $name}), (c:Cause {name: $cause}) "
                    "CREATE (d)-[:病因]->(c)",
                    name=name, cause=cause.strip())
        else:
            session.run("MERGE (c:Cause {name: $cause})", cause=cause_list.strip())
            session.run(
                "MATCH (d:Disease111 {name: $name}), (c:Cause {name: $cause}) "
                "CREATE (d)-[:病因]->(c)",
                name=name, cause=cause_list.strip())

        # 处理病发部位，如果有多个值，则拆分建立节点和关系，单个值直接处理
        if isinstance(location_list, list):
            for location in location_list:
                #建立节点
                session.run("MERGE (l:Location {name: $location})", location=location.strip())
                #建立关系
                session.run(
                    "MATCH (d:Disease111 {name: $name}), (l:Location {name: $location}) "
                    "CREATE (d)-[:病发部位]->(l)",
                    name=name, location=location.strip())
        else:
            session.run("MERGE (l:Location {name: $location})", location=location_list.strip())
            session.run(
                "MATCH (d:Disease111 {name: $name}), (l:Location {name: $location}) "
                "CREATE (d)-[:病发部位]->(l)",
                name=name, location=location_list.strip())

        # 处理易发群体
        if isinstance(population_list, list):
            for population in population_list:
                session.run("MERGE (p:Population {name: $population})", population=population.strip())
                session.run(
                    "MATCH (d:Disease111 {name: $name}), (p:Population {name: $population}) "
                    "CREATE (d)-[:易发群体]->(p)",
                    name=name, population=population.strip())
        else:
            session.run("MERGE (p:Population {name: $population})", population=population_list.strip())
            session.run(
                "MATCH (d:Disease111 {name: $name}), (p:Population {name: $population}) "
                "CREATE (d)-[:易发群体]->(p)",
                name=name, population=population_list.strip())

        # 处理易发季节
        if isinstance(season_list, list):
            for season in season_list:
                session.run("MERGE (s:Season {name: $season})", season=season.strip())
                session.run(
                    "MATCH (d:Disease111 {name: $name}), (s:Season {name: $season}) "
                    "CREATE (d)-[:易发季节]->(s)",
                    name=name, season=season.strip())
        else:
            session.run("MERGE (s:Season {name: $season})", season=season_list.strip())
            session.run(
                "MATCH (d:Disease111 {name: $name}), (s:Season {name: $season}) "
                "CREATE (d)-[:易发季节]->(s)",
                name=name, season=season_list.strip())

        # 处理临床表现
        if isinstance(symptom_list, list):
            for symptom in symptom_list:
                session.run("MERGE (s:Symptom {name: $symptom})", symptom=symptom.strip())
                session.run(
                    "MATCH (d:Disease111 {name: $name}), (s:Symptom {name: $symptom}) "
                    "CREATE (d)-[:临床表现]->(s)",
                    name=name, symptom=symptom.strip())
        else:
            session.run("MERGE (s:Symptom {name: $symptom})", symptom=symptom_list.strip())
            session.run(
                "MATCH (d:Disease111 {name: $name}), (s:Symptom {name: $symptom}) "
                "CREATE (d)-[:临床表现]->(s)",
                name=name, symptom=symptom_list.strip())

        # 处理诊断
        if isinstance(diagnosis_list, list):
            for diagnosis in diagnosis_list:
                session.run("MERGE (dgn:Diagnosis {name: $diagnosis})", diagnosis=diagnosis.strip())
                session.run(
                    "MATCH (d:Disease111 {name: $name}), (dgn:Diagnosis {name: $diagnosis}) "
                    "CREATE (d)-[:诊断]->(dgn)",
                    name=name, diagnosis=diagnosis.strip())
        else:
            session.run("MERGE (dgn:Diagnosis {name: $diagnosis})", diagnosis=diagnosis_list.strip())
            session.run(
                "MATCH (d:Disease111 {name: $name}), (dgn:Diagnosis {name: $diagnosis}) "
                "CREATE (d)-[:诊断]->(dgn)",
                name=name, diagnosis=diagnosis_list.strip())

        # 处理治疗方法
        if isinstance(treatment_list, list):
            for treatment in treatment_list:
                session.run("MERGE (t:Treatment {name: $treatment})", treatment=treatment.strip())
                session.run(
                    "MATCH (d:Disease111 {name: $name}), (t:Treatment {name: $treatment}) "
                    "CREATE (d)-[:治疗方法]->(t)",
                    name=name, treatment=treatment.strip())
        else:
            session.run("MERGE (t:Treatment {name: $treatment})", treatment=treatment_list.strip())
            session.run(
                "MATCH (d:Disease111 {name: $name}), (t:Treatment {name: $treatment}) "
                "CREATE (d)-[:治疗方法]->(t)",
                name=name, treatment=treatment_list.strip())

        # 处理药方
        if isinstance(prescription_list, list):
            for prescription in prescription_list:
                session.run("MERGE (p:Prescription {name: $prescription})", prescription=prescription.strip())
                session.run(
                    "MATCH (d:Disease111 {name: $name}), (p:Prescription {name: $prescription}) "
                    "CREATE (d)-[:药方]->(p)",
                    name=name, prescription=prescription.strip())
        else:
            session.run("MERGE (p:Prescription {name: $prescription})", prescription=prescription_list.strip())
            session.run(
                "MATCH (d:Disease111 {name: $name}), (p:Prescription {name: $prescription}) "
                "CREATE (d)-[:药方]->(p)",
                name=name, prescription=prescription_list.strip())

        # 处理辩证
        if isinstance(differentiation_list, list):
            for differentiation in differentiation_list:
                session.run("MERGE (dtn:Differentiation {name: $differentiation})",
                            differentiation=differentiation.strip())
                session.run(
                    "MATCH (d:Disease111 {name: $name}), (dtn:Differentiation {name: $differentiation}) "
                    "CREATE (d)-[:辩证]->(dtn)",
                    name=name, differentiation=differentiation.strip())
        else:
            session.run("MERGE (dtn:Differentiation {name: $differentiation})",
                        differentiation=differentiation_list.strip())
            session.run(
                "MATCH (d:Disease111 {name: $name}), (dtn:Differentiation {name: $differentiation}) "
                "CREATE (d)-[:辩证]->(dtn)",
                name=name, differentiation=differentiation_list.strip())

        # 处理预防
        if isinstance(prevention_list, list):
            for prevention in prevention_list:
                session.run("MERGE (pvn:Prevention {name: $prevention})", prevention=prevention.strip())
                session.run(
                    "MATCH (d:Disease111 {name: $name}), (pvn:Prevention {name: $prevention}) "
                    "CREATE (d)-[:预防]->(pvn)",
                    name=name, prevention=prevention.strip())
        else:
            session.run("MERGE (pvn:Prevention {name: $prevention})", prevention=prevention_list.strip())
            session.run(
                "MATCH (d:Disease111 {name: $name}), (pvn:Prevention {name: $prevention}) "
                "CREATE (d)-[:预防]->(pvn)",
                name=name, prevention=prevention_list.strip())

driver.close()
print("successfully")
