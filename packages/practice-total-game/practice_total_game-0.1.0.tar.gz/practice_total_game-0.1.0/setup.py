from setuptools import setup, find_packages

setup(
    name="practice_total_game",
    version="0.1.0",
    author="HongKiBum",
    author_email="hgb9720@hanyang.ac.kr",
    description="A collection of mini-games and utilities.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/HongKiBum/practice_total_game",  # Replace with your GitHub URL
    packages=find_packages(),
    install_requires=[
        "pygame",
        "kivy",
        "ultralytics",
        "mediapipe",
        "opencv-python-headless",
        "pytesseract",
        "Pillow",
        "SpeechRecognition",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
