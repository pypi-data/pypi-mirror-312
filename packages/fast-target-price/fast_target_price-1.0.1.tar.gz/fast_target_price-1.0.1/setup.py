from setuptools import setup, find_packages

setup(
    name="fast_target_price",                      # Tên thư viện trên PyPI
    version="1.0.1",                       # Phiên bản thư viện
    author="TargetPrice",                    # Tác giả
    author_email="", # Email liên hệ
    description="",
    packages=find_packages(),              # Tự động tìm các package
    include_package_data=True,             # Bao gồm dữ liệu trong MANIFEST.in
    classifiers=[                          # Phân loại thư viện
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",               # Phiên bản Python yêu cầu
)
