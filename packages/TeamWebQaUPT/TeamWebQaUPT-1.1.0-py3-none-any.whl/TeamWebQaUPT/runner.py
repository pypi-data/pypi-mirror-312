import pytest

def main():
    """
    Ejecuta todas las pruebas usando pytest.
    """
    exit_code = pytest.main([
        "-n", "3",                     # Ejecuta pruebas en paralelo.
        "--alluredir=./allure-results" # Genera reportes en Allure.
    ])
    exit(exit_code)
