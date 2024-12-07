from setuptools import setup, find_packages

setup(
    name="better-test-preview",
    version="0.0.2",
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
    author="HangoverHGV"
)
