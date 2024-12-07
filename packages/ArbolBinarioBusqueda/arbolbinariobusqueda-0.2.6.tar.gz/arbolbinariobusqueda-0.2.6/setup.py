from setuptools import setup, find_packages

setup(
    name="ArbolBinarioBusqueda",  # Nombre del paquete (único en PyPI)
    version="0.2.6",    # Versión del paquete
    author="Felipe Morales",
    author_email="felipe.morales.querol@gmail.com",
    description="Mostrar una implementación simple y totalmente en español con fines académicos",
    long_description=open("README.md").read(),  # Descripción larga desde README.md
    long_description_content_type="text/markdown",
    url="https://github.com/felipemoralesquerol/arbolbinariobusqueda",  # URL del repositorio
    packages=find_packages(where="src"),  # Busca automáticamente los submódulos
    package_dir={"": "src"},  # Define src/ como raíz de los paquetes
    include_package_data=True,  # Incluye archivos indicados en MANIFEST.in
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',  # Versión mínima de Python requerida
    install_requires=[        # Dependencias del paquete
        
    ],
)
