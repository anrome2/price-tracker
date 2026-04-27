# Para transformar el número de columna a letra para el Google Sheet
def numero_a_letra(n):
    if 1 <= n <= 26:
        return chr(n + 64)
    else:
        return None