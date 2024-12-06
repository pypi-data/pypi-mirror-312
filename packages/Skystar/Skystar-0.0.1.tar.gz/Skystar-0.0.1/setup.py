import setuptools  # 导入setuptools打包工具

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 读取 requirements.txt 中的依赖
with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="Skystar",
    version="0.0.1",
    author="Yonas-xin",
    author_email="linkstar443@163.com",
    description="A Deep Learning Framework For B",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/Yonas-Xin/Skystar",where python3
    packages=setuptools.find_packages(where='skystar_proj'),
    install_requires=requirements,  # 从 requirements.txt 读取依赖
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',  # Minimum Python version required
)
