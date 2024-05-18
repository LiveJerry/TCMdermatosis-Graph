# TCMdermatosis-Graph
真菌性中医皮肤病知识图谱及辅助诊断系统

文件清单及其说明：
data
  --Zhenjun.json	      数据文件，记录疾病信息
  --MedicalRecord.json	病例例子
  --1.xlsx              词典

Code
  --01 CreatGraph.py	  构建知识图谱
  --02 Export.py	      提取疾病名称和病因、临床表现、药方和治疗方法
  --03 HierarchicalClustering.py	  层次聚类
  --04 AssociationRules.py	        关联规则分析
  --05 Model.py	        诊断系统，包括智能问诊、辅助诊断、治疗方案推荐
  --06 After.py	        疗效评估与反馈
代码如果要运行，先修改读取文件的路径、Neo4j数据库的账号密码、输出结果的路径

Result
  --病因.jpg      病因层次聚类树状图
  --临床表现.jpg  临床表现层次聚类树状图
  --药方.jpg      药方层次聚类树状图
  --治疗方法.jpg  治疗方法层次聚类树状图
  --药方_Transposed.xlsx      用于数据分析的表格
  --临床表现_Transposed.xlsx  用于数据分析的表格
  --药方_Transposed.xlsx      用于数据分析的表格
  --治疗方法_Transposed.xlsx  用于数据分析的表格
