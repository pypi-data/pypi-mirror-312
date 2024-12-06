from setuptools import setup, find_packages

setup(
    name="pipincode",
    version="1",
    packages=find_packages(),
    install_requires=[],  # Thêm các thư viện cần thiết
    description="Pip in code",
    author="Dang Vo Anh Kiet",
    author_email="himnnha23@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)