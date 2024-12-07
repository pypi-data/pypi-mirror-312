from setuptools import setup, find_packages

setup(
    name="image_filter_library",
    version="1.0.0",
    description="A library for applying image filters with emotion detection using FER.",
    author="nanayeong",
    author_email="na22384593@gmail.com",
    packages=["image_filter_library"],
    install_requires=[
        "Pillow",
        "fer",
        "opencv-python-headless",
        "tensorflow",
        "moviepy>=1.0.3",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
