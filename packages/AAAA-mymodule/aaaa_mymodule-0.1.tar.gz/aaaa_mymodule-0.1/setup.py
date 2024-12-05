from setuptools import setup, find_packages

setup(
    name="AAAA_mymodule",  # 包的名字
    version="0.1",  # 版本号
    packages=find_packages(),  # 自动查找包
    install_requires=[
        'numpy',  # 依赖包
        'pandas',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    author="Nixer,lv",
    author_email="582848910@qq.com",
    description="A simple reusable Python module",
    long_description=open('README.md').read(),  # 从 README 文件加载详细描述
    long_description_content_type="text/markdown",  # 文件格式
    # url="https://github.com/yourusername/mymodule",  # 项目主页
    # project_urls={  # 额外链接
    #     "Bug Tracker": "https://github.com/yourusername/mymodule/issues",
    #     "Documentation": "https://yourmodule.readthedocs.io/",
    # },
    include_package_data=False,  # 包含额外的文件
    python_requires='>=3.8',  # Python 版本要求
)