def success(message: str, data=None):
    return {"status": "sucesso", "mensagem": message, "dados": data}

def error(message: str):
    return {"status": "erro", "mensagem": message}
