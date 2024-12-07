from setuptools import setup, find_packages

setup(
    name="unlimited_message",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pyautogui",
        "pywhatkit",
    ],
    description="A package to send WhatsApp messages instantly using Python",
    author="Your Name",
    author_email="your_email@example.com",
    url="https://github.com/yourusername/send_whatsapp_package",  # Optional, if hosting on GitHub
)