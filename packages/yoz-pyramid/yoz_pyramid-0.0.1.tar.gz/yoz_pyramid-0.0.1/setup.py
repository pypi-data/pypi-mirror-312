#!usr/bin/env
import setuptools
from setuptools import setup

# long description을 README.md로 대체하기 위한 작업
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(

	# module 이름
    name='yoz-pyramid', 
    
    # version 명시
    version='0.0.1',
    
    # package에 대한 짧은 description
    description='',
    
    # package에 대한 자세한 description
    # README.md로 대체한다
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    # package 저자 이름
    author='',
    
    # package 저자 이메일 
    author_email='',
    
    # package url (ex: github)
    url='',
    license='MIT',
    packages=setuptools.find_packages(),
    
    # 파이썬 버전
    python_requires='>=3.8',  
    
  	# package 설치 시 필요한 다른 package
    # 이렇게 설정해놓은 package들은 설치 시 자동으로 설치된다.
    install_requires = [

    ],
    classifiers = [
                      "Programming Language :: Python :: 3",
    ]
)

