from setuptools import setup, find_packages

setup(
    name='kafka-avro-helper',
    version='0.1.9',
    description='A package for Kafka and AVRO processing',
    author='Andrei Boiko',
    author_email='dushes.nadym@gmail.com',
    url='https://github.com/idushes/kafka-helper-package',
    packages=find_packages(),
    install_requires=[
        'aiokafka>=0.8.1,<1.0.0',
        'httpx>=0.23.0,<1.0.0',
        'dataclasses-avroschema>=0.63.7,<=0.65.3'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
