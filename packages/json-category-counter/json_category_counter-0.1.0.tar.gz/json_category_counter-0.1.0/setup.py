# setup.py

from setuptools import setup, find_packages

setup(
    name='json_category_counter',  # 包名
    version='0.1.0',               # 版本号
    author='Zheng,yang',            # 作者
    author_email='your-email@example.com',  # 作者邮箱
    description='A package to count categories and tests from a JSON file',
    long_description=open('README.md').read(),  # 详细描述，可以通过 README.md 文件
    long_description_content_type='text/markdown',
    # url='https://github.com/yourusername/json_category_counter',  # 包的 GitHub 地址
    packages=find_packages(),  # 自动找到所有包
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # 支持的 Python 版本
)
