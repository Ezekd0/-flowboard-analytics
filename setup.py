from pathlib import Path

from setuptools import find_packages, setup

BASE_DIR = Path(__file__).parent
REQUIREMENTS = [
    line.strip()
    for line in (BASE_DIR / "requirements.txt").read_text(encoding="utf-8").splitlines()
    if line.strip() and not line.strip().startswith("#")
]

setup(
    name="taskflow-analytics",
    version="1.0.0",
    description="Production-ready FastAPI backend for task management and analytics.",
    long_description=(BASE_DIR / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    author="[your-name]",
    author_email="[your-email]",
    url="https://github.com/[your-username]/taskflow-analytics",
    license="MIT",
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    install_requires=REQUIREMENTS,
    python_requires=">=3.11",
    entry_points={"console_scripts": ["taskflow-api=app.main:app"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: FastAPI",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
)
