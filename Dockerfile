# Stage 1: Build the Angular app
FROM node:14 as build
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build --prod

# Stage 2: Set up the FastAPI app
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY --from=build /app/dist /app/app/static
COPY backend/*.py /app/app/
    
# Command to run the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]