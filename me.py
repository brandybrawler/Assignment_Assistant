import os
import pathlib

def create_directory(path):
    try:
        os.makedirs(path)
        print(f"Directory created: {path}")
    except FileExistsError:
        print(f"Directory already exists: {path}")

def create_file(path, content=""):
    with open(path, "w") as f:
        f.write(content)
        print(f"File created: {path}")

# Main project directory
project_dir = "my_ai_service"
create_directory(project_dir)

# App directory
app_dir = os.path.join(project_dir, "app")
create_directory(app_dir)

# API directory
api_dir = os.path.join(app_dir, "api")
create_directory(api_dir)

# Endpoints directory
endpoints_dir = os.path.join(api_dir, "endpoints")
create_directory(endpoints_dir)

# Models directory
models_dir = os.path.join(api_dir, "models")
create_directory(models_dir)

# Core directory
core_dir = os.path.join(app_dir, "core")
create_directory(core_dir)

# Services directory
services_dir = os.path.join(app_dir, "services")
create_directory(services_dir)

# Tests directory
tests_dir = "tests"
create_directory(tests_dir)

# Docker directory
docker_dir = "docker"
create_directory(docker_dir)

# Create main files
create_file(os.path.join(app_dir, "main.py"))
create_file(os.path.join(app_dir, "__init__.py"))
create_file(os.path.join(api_dir, "__init__.py"))
create_file(os.path.join(core_dir, "config.py"))
create_file(os.path.join(core_dir, "database.py"))
create_file(os.path.join(core_dir, "security.py"))
create_file(os.path.join(services_dir, "notification_service.py"))
create_file(os.path.join(tests_dir, "test_authentication.py"))
create_file(os.path.join(tests_dir, "test_user.py"))
create_file(os.path.join(tests_dir, "test_job.py"))
create_file(os.path.join(docker_dir, "Dockerfile"))
create_file(os.path.join(docker_dir, "docker-compose.yml"))
create_file("README.md")
create_file("requirements.txt", "fastapi\npydantic")

print("File system successfully created!")
