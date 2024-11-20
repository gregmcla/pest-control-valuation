web: gunicorn --workers=2 --threads=1 --worker-class=uvicorn.workers.UvicornWorker --bind=0.0.0.0:$PORT --timeout=30 --worker-tmp-dir=/dev/shm app:app
