from setuptools import setup

setup(
    name="password_validators",
    version="0.1",
    description="Collections of password validators",
    author="Patryk Świderski",
    packages=["password_validators"],
    install_requires=["requests"]
)

#python setup.py sdist