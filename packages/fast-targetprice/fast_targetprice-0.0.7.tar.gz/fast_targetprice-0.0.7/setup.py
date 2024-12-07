from setuptools import setup, find_packages
from Cython.Build import cythonize

setup(
    name="fast_targetprice",  # Tên thư viện
    version="0.0.7",  # Phiên bản thư viện
    author="targetprice",  # Tên tác giả
    packages=find_packages(), 
    classifiers=[  
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    ext_modules=cythonize("fast_targetprice/*.py"), 
    install_requires=[],
    setup_requires=["Cython>=0.29.36"],
    python_requires='>=3.6',  # Yêu cầu phiên bản Python tối thiểu
)
