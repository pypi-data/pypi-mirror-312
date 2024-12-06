from setuptools import setup, find_packages

setup(
    name='telegraph-sdk',  # 包的名称
    version='0.1.3',  # 包的版本
    packages=find_packages(),  # 自动找到包内的所有模块
    install_requires=[  # 依赖的其他包
        'httpx',  # 示例，实际根据需要添加
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
