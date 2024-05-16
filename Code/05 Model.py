import re
import openpyxl
from neo4j import GraphDatabase

# 计算每种疾病与输入文本中的临床表现关键词的匹配程度
def calculate_match_score(symptoms, disease_symptoms):
    match_count = 0
    for symptom in symptoms:
        if symptom in disease_symptoms:
            match_count += 1
    return match_count

# 计算病发部位的匹配程度，如果病发部位匹配，则返回 1，否则返回 0
disease_body_part = []
def calculate_body_part_match(affected_body_part, disease_body_part):
    if affected_body_part and disease_body_part:
        return 1 if affected_body_part == disease_body_part else 0
    else:
        return 0

# 执行 Cypher 查询
def run_cypher_query(query, parameters):
    with driver.session() as session:
        result = session.run(query, parameters)
        return [record for record in result]

# 读取患者病情
text = str(input("请输入患者症状："))
age = None

# 提取年龄
age_match = re.search(r'\d+岁', text)
if age_match:
    age_str = age_match.group()
    age = int(re.search(r'\d+', age_str).group())

# 根据年龄划分人群
population_group = []
if age is not None:
    if age < 1:
        population_group = "婴儿"
    elif age < 18:
        population_group = "儿童"
    elif age < 65:
        population_group = "成人"
    else:
        population_group = "老人"

# 划分病发部位
body_parts = ["头", "手", "四肢", "颈","脚","面部","躯干","胸","背"]
affected_body_part = None
for part in body_parts:
    if part in text:
        affected_body_part = part
        break

# 读取临床表现关键词列表
symptom_keywords = []

# 读取 Excel 文件
wb = openpyxl.load_workbook("1.xlsx")
ws = wb.active

found_symptoms = []

# 遍历所有的单元格，如果读到的单元格在 text 里面，则返回当前单元格同一行的第一列单元格的内容
for row in ws.iter_rows(values_only=True):
    for cell in row:
        if str(cell) in text:
            found_symptoms.append(str(row[0]))
            break  # 找到了就跳出当前行的循环

# 去除重复项
found_symptoms = list(set(found_symptoms))

# 输出结果
result = {
    "易发人群": population_group,
    "病发部位": affected_body_part,
    "临床表现": found_symptoms
}
print(result)

# 获取临床表现列表
symptoms = result.get("临床表现", [])

# 连接到 Neo4j 数据库
uri = "bolt://localhost:7690"  # Neo4j 数据库的 URI
username = "neo4j"              # Neo4j 数据库的用户名
password = "12345678"           # Neo4j 数据库的密码

# 创建一个 Neo4j 数据库驱动程序实例
driver = GraphDatabase.driver(uri, auth=(username, password))

# 定义 Cypher 查询语句
cypher_query = (
    "MATCH (d:Disease111)-[:临床表现]->(s:Symptom) "
    "WHERE s.name IN $symptoms "
    "MATCH (d)-[:病发部位]->(l:Location) "
    "RETURN d.name AS disease_name, collect(DISTINCT s.name) AS disease_symptoms, collect(DISTINCT d) AS diseases, l.name AS disease_body_part"
)
# 执行查询
query_result = run_cypher_query(cypher_query, {"symptoms": symptoms})

# 根据匹配程度对疾病进行排序
query_result.sort(key=lambda x: (calculate_body_part_match(affected_body_part, x["disease_body_part"]),
                                  calculate_match_score(symptoms, x["disease_symptoms"])),
                   reverse=True)


# 输出查询结果
for record in query_result:
    disease_name = record["disease_name"]
    diseases = record["diseases"]
    # 只输出每种疾病名称一次
    if disease_name:
        # 输出疾病名称
        print("\n============疾病名称：============\n", disease_name)

        # 查询并输出治疗方法和反馈
        treatment_query = (
            "MATCH (d:Disease111 {name: $disease_name})-[:治疗方法]->(t:Treatment)-[:治疗反馈]->(f:Feedback) "
            "RETURN t.name AS treatment, f.name AS feedback"
        )
        treatment_result = run_cypher_query(treatment_query, {"disease_name": disease_name})

        # 如果查询结果为空，则执行下面的查询语句并且打印治疗方法
        if treatment_result:
            # 用集合来存储治疗方法和反馈，确保每种方法和反馈只输出一次
            unique_treatments_feedbacks = set()

            # 打印治疗方法和反馈
            print("\n============治疗方法和反馈：============")
            for record in treatment_result:
                treatment = record["treatment"]
                feedback = record["feedback"]
                if feedback == "":  # 只有治疗方法，没有反馈
                    print(treatment)
                else:  # 既有治疗方法，又有反馈
                    print(f"{treatment}\n（反馈：{feedback}）")

        # 执行下面的查询语句并打印治疗方法
        treatment_query = (
            "MATCH (d:Disease111 {name: $disease_name})-[:诊断]->(t:Diagnosis) "
            "RETURN t.name AS treatment"
        )
        treatment_result = run_cypher_query(treatment_query, {"disease_name": disease_name})
        print("\n============诊断：============")
        for record in treatment_result:
            print(record["treatment"])

        # 执行下面的查询语句并打印治疗方法
        treatment_query = (
            "MATCH (d:Disease111 {name: $disease_name})-[:治疗方法]->(t:Treatment) "
            "RETURN t.name AS treatment"
        )
        treatment_result = run_cypher_query(treatment_query, {"disease_name": disease_name})
        print("\n============治疗方法：============")
        for record in treatment_result:
            print(record["treatment"])



# 关闭驱动程序
driver.close()
