from setuptools import setup, find_packages

setup(
    name="OSD_LibraryPython",                 # Nombre de tu paquete
    version="1.1.0",                    # Versión
    description="Generic Library OSDental LLC",  # Breve descripción
    long_description=open("README.md").read(),  # Descripción larga
    long_description_content_type="text/markdown",  # Formato de README
    author="OSD Team_Develop",
    author_email="project_development@osdental.ai",
    url="",  # URL del proyecto
    packages=find_packages(),           # Encuentra automáticamente los módulos
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'azure-core==1.32.0',
        'azure-servicebus==7.13.0',
        'certifi==2024.8.30',
        'cffi==1.17.1',
        'charset-normalizer==3.4.0',
        'cryptography==43.0.3',
        'idna==3.10',
        'isodate==0.7.2',
        'pyasn1==0.6.1',
        'pycparser==2.22',
        'pycryptodome==3.21.0',
        'PyJWT==2.9.0',
        'pyodbc==5.2.0',
        'python-dotenv==1.0.1',
        'pytz==2024.2',
        'requests==2.32.3',
        'six==1.16.0',
        'typing_extensions==4.12.2',
        'urllib3==2.2.3'   # Versión mínima y máxima
    ],
    python_requires=">=3.11.9"
    
)

