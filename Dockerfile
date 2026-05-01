FROM python:3.10-slim
WORKDIR /app
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "-m", "backend.server"]