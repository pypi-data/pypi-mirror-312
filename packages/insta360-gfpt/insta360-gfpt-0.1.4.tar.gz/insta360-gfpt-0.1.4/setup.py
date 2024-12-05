from setuptools import setup, find_packages

setup(
    name='insta360-gfpt',
    version='0.1.4',
    packages=find_packages(),
    package_data={
        'insta360_gfpt': ['templates/*'],
    },
    install_requires=[
        # 列出你的依赖项
    ],
    entry_points={
        'console_scripts': [
            'create_insta360_gfpt = insta360_gfpt.cli:main',
        ],
    },
    author='rain',
    author_email='chenrunming@insta360.com',
    description='insta360 gfpt',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.insta360.com/test2/production-testing-tools/insta360_gfpt.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)