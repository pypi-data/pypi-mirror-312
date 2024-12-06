from setuptools import setup, Extension

setup(
    name="fast_targetprice",                       # Tên thư viện của bạn
    version="0.0.1",                           # Phiên bản thư viện
    packages=["fast_targetprice"],                 # Thư mục chứa mã nguồn của thư viện
    ext_modules=[],                          # Các file .pyd đã được biên dịch sẽ không cần thiết ở đây, vì chúng đã sẵn sàng
    include_package_data=True,               # Đảm bảo bao gồm các file khác như README.md
    install_requires=[],                     # Các thư viện phụ thuộc nếu có
    python_requires=">=3.6",                 # Phiên bản Python yêu cầu
)
