docker run --name makeup_service --gpus all --network host -det -i -v "$PWD":/app abaraniuk/makeup_service:latest
docker exec -i makeup_service bash -c "cd /app/ && pip3 install -r requirements.txt ."
docker exec -i makeup_service bash -c "python3 /app/makeup_service/server/app.py --host 0.0.0.0 --port 5000"