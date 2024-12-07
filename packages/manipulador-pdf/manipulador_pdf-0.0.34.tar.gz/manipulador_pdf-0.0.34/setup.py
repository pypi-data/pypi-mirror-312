from setuptools import setup, find_packages

setup(
    name="manipulador_pdf",
    version="0.0.34",
    description="Uma biblioteca para manipulação de arquivos .pdf.",
    author="Luiz Gustavo Queiroz",
    author_email="luizgusqueiroz@gmail.com",
    packages=find_packages(),
    install_requires=[
        "google-auth",
        "google-auth-oauthlib",
        "google-api-python-client",
        "PyPDF2",
        "pytesseract",
        "opencv-python",
        "PyMuPDF",
        "pandas",
        "Pillow",
        "tqdm",
    ],
)
