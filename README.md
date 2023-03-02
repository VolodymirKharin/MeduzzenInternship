.BE-1
1. Use pip install requirements.txt
2. Configure .env file
3. Run app with  main.py in folder /app/main.py
4. Run test with command python -m pytest

.BE-2
1. Use command: docker build -t app .
2. Run app in container with command: docker run -p 8000:8000 app
3. Use command: docker container exec -it --name sh
4. Run test with command: python -m pytest


.BE-4
1. To create migrations need to use: alembic revision --autogenerate -m "migration"
2. Then use: alembic upgrade head

