from setuptools import setup,find_packages
setup(
    name = 'STT_Module',
    version = '1.0',
    author='Abhay Mallik',
    author_email='abhaymallik5566@gmail.com',
    description='A Python library by Abhay Mallik for automating speech-to-text transcription using Selenium. This library interacts with browser-based speech recognition apps, captures transcriptions, and saves them to a file for further use.Key Featuresare: i. Automates browser interaction for speech-to-text tasks. ii. Configured for headless Chrome with custom options. iii. Captures and writes transcribed output to a local file.'
)
packages = find_packages(),
install_requirements = [
    'selenium',
    'webdriver_manager',
    'Python 3.8+'
]
