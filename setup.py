from setuptools import setup, find_packages

setup(
    name="taskflow-analytics",
    version="0.1.0",
    description="Task flow analytics application with FastAPI",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "sqlalchemy>=2.0.23",
        "psycopg2-binary>=2.9.9",
        "python-dotenv>=1.0.0",
        "pydantic>=2.5.0",
    ],
)
