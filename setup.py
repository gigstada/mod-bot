from setuptools import setup, find_packages

setup(
    name='mod-bot-ai',
    version='0.1.0',
    packages=find_packages(),
    py_modules=["mod", "fn_loop", "gpt_functions"],
    install_requires=[i.strip() for i in open("requirements.txt").readlines()],
    entry_points={
        'console_scripts': ['mod=mod:main']
    }
)
