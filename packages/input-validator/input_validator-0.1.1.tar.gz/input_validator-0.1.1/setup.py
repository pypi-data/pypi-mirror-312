from setuptools import setup, find_packages

setup(
    name='input_validator',
    version='0.1.1',
    author='Pradeep Kumar',
    author_email='pradeepkumar.r10321@gmail.com',
    description='This library aims to validate inputs to prevent common security vulnerabilities that are prevalent due to bad inputs',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/PradeepKumar10321/input-validator',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        ],
        python_requires='>=3.6',
    )