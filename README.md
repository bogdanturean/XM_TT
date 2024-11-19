# XM_TT
XM Technical Task

Execution setup steps:

1. Open project in PyCharm
2. Open XM_TT in terminal
3. Run command: docker build -t fastapi-app:latest .
4. Run command: docker run -p 8080:8080 fastapi-app 
5. Open in tesrminal TestSuite
6. Run pytest testSuite_functional.py testSuite_performance.py --html="report.html"
7. Report is generated in report.html (folder TestSuite)

Swagger documentataion present in repo as yaml
