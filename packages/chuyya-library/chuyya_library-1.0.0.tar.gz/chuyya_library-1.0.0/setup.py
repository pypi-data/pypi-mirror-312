from setuptools import setup, find_packages

setup(
    name="chuyya_library",  # Package name
    version="1.0.0",  # Version number
    author="Siva Suriya Kandasamy",  # Your name
    author_email="kannanmahalsuriya@gmail.com",  # Your email
    description="A Python library for generating shipment invoices",
    packages=find_packages(),
    install_requires=[
        "fpdf"  # Add dependencies your library needs
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version
)
