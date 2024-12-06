import setuptools

with open("README.md") as file:
    read_me_description = file.read()

setuptools.setup(
    name="executor-invest-helper",
    version="0.1.2",
    author="Invest Guru",
    author_email="example@gmail.com",
    description="Database Executor for Invest Helper",
    long_description=read_me_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sazonovvladimir/invest_helper_bot",
    packages=['executor'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)