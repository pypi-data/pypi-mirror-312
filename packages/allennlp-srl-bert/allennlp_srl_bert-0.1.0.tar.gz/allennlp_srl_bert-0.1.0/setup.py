from setuptools import setup, find_packages

setup(
    name="allennlp_srl_bert",  # Replace with your package name
    version="0.1.0",
    author="Austin Light",
    author_email="austin.light@wgu.edu",
    description="Semantic Role Labeling using AllenNLP trained BERT model",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/WGU-edu/allennlp_srl_bert",  # Replace with your repo
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
