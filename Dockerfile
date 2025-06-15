
FROM python:3.11-slim

# work directory
WORKDIR /app

# Copy the file requirements
COPY requirements.txt .

# install dependences
RUN pip install --no-cache-dir -r requirements.txt

# Cpy all the code
COPY . .

# Eposig using FastAPI(8000) 
EXPOSE 8000

# Comand to run the app with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
