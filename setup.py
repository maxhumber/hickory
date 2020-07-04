from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="hickory",
    version="0.1",
    description="🕰 Hickory, dickory, dock. The mouse ran up the clock.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 1 - Planning"
    ],
    keywords=["schedule", "cron", "crontab"],
    url="https://github.com/maxhumber/hickory",
    author="Max Humber",
    author_email="max.humber@gmail.com",
    license="MIT",
    py_modules=["hickory"],
    python_requires=">=3.6",
    setup_requires=["setuptools>=38.6.0"],
)
