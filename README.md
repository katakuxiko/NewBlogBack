to start
APP:
	uvicorn app.main:app --reload --log-level debug
Minio:
	.\minio.exe server C:\minio --console-address :9001