from setuptools import setup, find_packages

setup(
    name="agentmq",
    version="0.0.0",
    author="AgentMQ",
    description="Python for AgentMQ",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires='>=3.6',
)
