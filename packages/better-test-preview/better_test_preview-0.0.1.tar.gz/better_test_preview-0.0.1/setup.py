from setuptools import setup, find_packages

setup(
    name="api",
    version="0.1.0",
    description="FastAPI app",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "jinja2",
        "pydantic",
        "pytest",
        "pytest-html",
        "ansi2html",
    ],
)
