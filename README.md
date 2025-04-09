to start
APP:
	uvicorn app.main:app --reload --log-level debug
Minio:
	Download
	https://min.io/docs/minio/windows/index.html
	Start in Powershell
	.\minio.exe server C:\minio --console-address :9001
Elastic
	Download
	https://www.elastic.co/downloads/elasticsearch
	Start bin/elasticsearch.bat
	