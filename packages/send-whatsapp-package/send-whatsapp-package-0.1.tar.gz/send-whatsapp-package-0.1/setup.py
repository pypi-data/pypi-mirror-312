from setuptools import setup, find_packages

setup(
    name='send-whatsapp-package',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pywhatkit',
        'pyautogui',
    ],
    entry_points={
        'console_scripts': [
            'send-whatsapp = send_whatsapp_package.main:send_whatsapp_instant_message',
        ],
    },
)
