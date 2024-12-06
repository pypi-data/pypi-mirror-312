from setuptools import setup, find_packages

setup(
    name='dirhunter',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'colorama',
        'click'
    ],
    entry_points={
        'console_scripts': [
            'dirhunter=dirhunter.cli:main',
        ],
    },
    author='MrFidal',
    author_email='mrfidal@proton.me',
    description='A powerful directory scanning and hunting tool',
    long_description=open('README.md', encoding='utf-8').read(),  
    long_description_content_type='text/markdown',
    url='https://github.com/ByteBreach/dirhunter',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
