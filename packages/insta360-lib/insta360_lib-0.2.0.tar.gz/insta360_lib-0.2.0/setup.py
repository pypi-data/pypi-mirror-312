from setuptools import setup, find_packages

setup(
    name='insta360_lib',
    version='0.2.0',
    packages=find_packages(),
    package_data={
        'insta360_lib': ['dlls/*.dll', 'dlls/iac3/*.dll'],
    },
    include_package_data=True,
    install_requires=[
        "loguru"
        # 列出你的依赖项
    ],
    entry_points={
        # 如果有命令行工具，可以在这里定义
    },
    author='rain',
    author_email='chenrunming@insta360.com',
    description='insta360 算法库调用封装库',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.insta360.com/test2/production-testing-tools/insta360_lib.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)