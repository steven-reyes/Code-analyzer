# Dockerfile

# -----------------------------------------
# Stage 1: Node environment (build front-end or run Node scripts)
# -----------------------------------------
    FROM node:18-alpine AS node_builder
    WORKDIR /app
    
    # Copy package.json and lock file for Node
    COPY package*.json ./
    # If you prefer Yarn:
    # COPY yarn.lock ./
    # RUN yarn install
    
    RUN npm install
    
    # If you have front-end code in e.g. /frontend
    # COPY ./frontend ./frontend
    # RUN npm run build
    
    # -----------------------------------------
    # Stage 2: Python environment
    # -----------------------------------------
    FROM python:3.9-slim
    
    # Create a directory for the code
    WORKDIR /code
    
    # Copy Python dependency files
    COPY requirements.txt /code/
    RUN pip install --upgrade pip
    RUN pip install -r requirements.txt
    
    # (Optional) If using Conda:
    # COPY environment.yml /code/
    # RUN conda env create -f environment.yml
    
    # Copy all code
    COPY . /code
    
    # (Optional) Copy the built Node app from Stage 1 if needed
    # COPY --from=node_builder /app/build ./some_frontend_folder
    
    # Expose ports if needed
    EXPOSE 5000 3000
    
    # Environment variables
    ENV FLASK_ENV=production
    ENV PYTHONUNBUFFERED=1
    
    # Default command: run Python script
    CMD ["python", "src/main.py"]
    