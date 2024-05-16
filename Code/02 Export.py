from neo4j import GraphDatabase
import pandas as pd

# Neo4j数据库连接信息
uri = "bolt://localhost:7690"
username = "neo4j"
password = "12345678"

# Neo4j数据库查询语句
queries = {
    "治疗方法": """
    MATCH (d:Disease111)-[:治疗方法]->(t:Treatment)
    RETURN d.name AS disease, t.name AS item
    """,
    "药方": """
    MATCH (d:Disease111)-[:药方]->(t:Prescription)
    RETURN d.name AS disease, t.name AS item
    """,
    "病因": """
    MATCH (d:Disease111)-[:病因]->(t:Cause)
    RETURN d.name AS disease, t.name AS item
    """,
    "临床表现": """
    MATCH (d:Disease111)-[:临床表现]->(t:Symptom)
    RETURN d.name AS disease, t.name AS item
    """
}


# 连接Neo4j数据库并执行查询
def run_query(uri, username, password, query):
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        with driver.session() as session:
            result = session.run(query)
            return result.data()
    except Exception as e:
        print("An error occurred while connecting to Neo4j:", e)
        return None


# 获取查询结果并构建二维列表
def build_adjacency_matrix(data):
    items = set()
    disease_item_map = {}

    for record in data:
        disease = record['disease']
        item = record['item']
        items.add(item)
        disease_item_map.setdefault(disease, set()).add(item)

    items = sorted(list(items))
    disease_list = sorted(list(disease_item_map.keys()))

    adjacency_matrix = [[0] * len(disease_list) for _ in range(len(items))]

    for i, item in enumerate(items):
        for j, disease in enumerate(disease_list):
            if disease in disease_item_map and item in disease_item_map[disease]:
                adjacency_matrix[i][j] = 1

    return items, disease_list, adjacency_matrix


# 将结果保存为Excel文件
def save_to_excel(items, disease_list, adjacency_matrix, filename):
    df = pd.DataFrame(adjacency_matrix, index=items, columns=disease_list)
    try:
        df.to_excel(filename)
        print("Excel file saved successfully:", filename)
    except Exception as e:
        print("An error occurred while saving the Excel file:", e)


# 执行查询并保存结果到Excel文件
if __name__ == "__main__":
    for query_name, query_string in queries.items():
        data = run_query(uri, username, password, query_string)
        if data:
            items, disease_list, adjacency_matrix = build_adjacency_matrix(data)
            save_to_excel(items, disease_list, adjacency_matrix, f"{query_name}_Transposed.xlsx")
