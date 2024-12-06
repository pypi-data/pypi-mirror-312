from setuptools import setup, find_packages

setup(
    authors=['赵锐'],
    author_email='3505469466@qq.com',
    description='黑河学院软开社团PFAI项目',
    long_description=open('./README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/xiaorui3',
    license='MIT',
    name='hhxy',
    version='0.2.1',
    packages=find_packages(),
    install_requires=[
        # 这里添加你的包依赖
        'pandas'
        # 其他依赖...
    ],
    entry_points={
        'console_scripts': [
            'hhxy-rk-pfai= mymodule.main:install_and_run',  # 调用main.py中的install_and_run函数
        ],
    },
)