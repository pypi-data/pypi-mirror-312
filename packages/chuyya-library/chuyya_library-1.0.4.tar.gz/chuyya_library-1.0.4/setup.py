from setuptools import setup, find_packages

setup(
    name="chuyya_library",
    version="1.0.4",
    packages=find_packages(),  # Automatically detects 'chuyya_library'
    install_requires=[
        "fpdf"  # Add required dependencies
    ],
    description="A Python library for generating shipment invoices in PDF",
    author="Siva Suriya Kandasamy",
    author_email="kannanmahalsuriya@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
