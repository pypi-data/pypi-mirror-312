from setuptools import setup, find_packages

setup(
    name="meta_qubit",  # Όνομα της βιβλιοθήκης
    version="1.0.0",  # Έκδοση
    author="Το Όνομά Σου",
    author_email="your_email@example.com",
    description="Βιβλιοθήκη για δημιουργία και εκτέλεση κβαντικών κυκλωμάτων",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your_username/meta_qubit",  # Προαιρετικά, GitHub URL
    packages=find_packages(),
    ext_modules=[],  # Δεν χρειάζεται να δηλώσεις explicitly το .pyd ή .so εδώ
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
