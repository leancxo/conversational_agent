from setuptools import setup, find_packages

setup(
    name="conversational_agent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "python-multipart>=0.0.5",
        "jinja2>=3.0.1",
        "pytest>=6.2.5",
        "pytest-cov>=2.12.1",
        "httpx>=0.28.0",
    ],
    python_requires=">=3.8",
) 