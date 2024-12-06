from setuptools import setup, find_packages

setup(
    name='pyzrpc',
    version='2.3',
    description="pyzrpc",
    long_description=open('README.rst').read(),
    # long_description_content_type='text/plain',
    include_package_data=True,
    author='YanPing',
    author_email='zyphhxx@foxmail.com',
    maintainer='YanPing',
    maintainer_email='zyphhxx@foxmail.com',
    license='MIT License',
    url='https://gitee.com/ZYPH/zerorpc',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires=">=3.7,<3.11",
    install_requires=[
        'nameko==2.14.1',
        'pika==1.3.2',
        'pytz>=2024.1',
        'pymongo==4.8.0',
        'kombu==5.4.0',
        'pycryptodomex==3.14.1',
        'streamlit==1.40.1'
    ]
)
