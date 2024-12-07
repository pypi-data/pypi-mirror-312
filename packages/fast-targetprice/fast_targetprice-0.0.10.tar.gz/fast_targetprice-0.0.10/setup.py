from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension("fast_targetprice.client", ["fast_targetprice/client.py"]),
]
# setup(
#     name="fast_targetprice",  # Tên thư viện
#     version="0.0.9",  # Phiên bản thư viện
#     author="targetprice",  # Tên tác giả
#     packages=["fast_targetprice"],
#     package_data={
#         "fast_targetprice": ["*.pkl"],  # Bao gồm các file cần thiết
#     },
#     classifiers=[  
#         "Programming Language :: Python :: 3",
#         "Programming Language :: Python :: 3.7",
#         "Programming Language :: Python :: 3.8",
#         "Programming Language :: Python :: 3.9",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
#     ext_modules=cythonize(extensions,compiler_directives={'language_level': "3"}), 
#     setup_requires=["Cython>=0.29.36"],
#     python_requires='>=3.6',  # Yêu cầu phiên bản Python tối thiểu
#     include_package_data=True,
#     zip_safe=False,
# )
setup(
    name="fast_targetprice",
    version="0.0.10",
    packages=["fast_targetprice"],
    package_data={
        "fast_targetprice": ["*.pyd", "*.so", "*.pkl"],  # Bao gồm các file cần thiết
    },
    include_package_data=True,
    zip_safe=False,  # Để False nếu thư viện cần nạp từ đĩa
)