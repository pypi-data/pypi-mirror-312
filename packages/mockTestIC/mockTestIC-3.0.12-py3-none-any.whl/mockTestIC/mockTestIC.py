import re
from faker import Faker
from typing import Dict

# Cria uma instância da classe Faker
fake = Faker()

# Mapeamento de tipos de dados para funções Faker
tipo_dados_mapper = {
    "primeiro nome": fake.first_name,
    "sobrenome": fake.last_name,
    "nome completo": fake.name,
    "nome usuario": fake.user_name,
    "prefixo": fake.prefix,
    "sufixo": fake.suffix,
    "endereco": fake.address,
    "cidade": fake.city,
    "estado": fake.state,
    "pais": fake.country,
    "codigo postal": fake.zipcode,
    "endereco rua": fake.street_address,
    "latitude": fake.latitude,
    "longitude": fake.longitude,
    "numero telefone": fake.phone_number,
    "numero celular": fake.phone_number,
    "email": fake.email,
    "email seguro": fake.safe_email,
    "data nascimento": fake.date_of_birth,
    "data seculo": fake.date_this_century,
    "data decada": fake.date_this_decade,
    "horario": fake.time,
    "data hora": fake.date_time,
    "hora ISO": fake.iso8601,
    "frase": fake.sentence,
    "paragrafo": fake.paragraph,
    "texto": fake.text,
    "empresa": fake.company,
    "cargo": fake.job,
    "seguranca social": fake.ssn,
    "numero inteiro": fake.random_int,
    "elemento": fake.random_element,
    "amostra": fake.random_sample,
    "numero flutuante": fake.pyfloat,
    "url": fake.url,
    "ipv4": fake.ipv4,
    "ipv6": fake.ipv6,
    "numero cartao": fake.credit_card_number,
    "cartao vencimento": fake.credit_card_expire,
}

def fake_json(json_data: Dict[str, str]) -> Dict[str, str]:
    """
    Gera dados fictícios para os campos fornecidos no dicionário.
    """
    result_data = json_data.copy()

    for key, value in json_data.items():
        value_lower = value.lower()
        if value_lower in tipo_dados_mapper:
            result_data[key] = tipo_dados_mapper[value_lower]()
        else:
            raise ValueError(f"Tipo de dado não suportado para a chave '{key}': {value}")

    return result_data

def fake_sql(texto: str) -> Dict[str, str]:
    """
    Localiza e substitui palavras-chave no texto por dados fictícios gerados com Faker.
    """
    # Mapeia as palavras-chave para os métodos correspondentes do Faker
    palavras_chave = {
        "id": lambda: fake.random_int(min=1, max=9999),
        "nome": fake.first_name,
        "idade": lambda: fake.random_int(min=0, max=120),
        "cidade": fake.city,
        "profissao": fake.job,
        "sobrenome": fake.last_name,
        "completo": fake.name,
        "usuario": fake.user_name,
        "prefixo": fake.prefix,
        "sufixo": fake.suffix,
        "endereco": fake.address,
        "estado": fake.state,
        "pais": fake.country,
        "cep": fake.zipcode,
        "rua": fake.street_address,
        "latitude": fake.latitude,
        "longitude": fake.longitude,
        "celular": fake.phone_number,
        "telefone": fake.phone_number,
        "email": fake.email,
        "nascimento": lambda: fake.date_of_birth().strftime('%Y-%m-%d'),
        "cadastro": lambda: fake.date_time().strftime('%Y-%m-%d'),
        "horario": fake.time,
        "descricao": fake.text,
        "empresa": fake.company,
        "cargo": fake.job,
        "site": fake.url,
        "linkedin": fake.url,
        "ipv4": fake.ipv4,
        "ipv6": fake.ipv6,
        "cartao": fake.credit_card_number,
        "credito": fake.credit_card_number,
        "cpf": lambda: str(fake.random_int(min=11111111111, max=99999999999)),
        "rg": lambda: str(fake.random_int(min=111111111, max=999999999)),
        "estoque": lambda: fake.random_int(min=0, max=99999),
        "texto": fake.text,
        "salario": lambda: fake.random_int(min=100, max=99999),
        "ativo": fake.boolean,
    }

    # Usa expressão regular para encontrar e substituir as palavras-chave
    dados_gerados = {}

    def substituir_palavra_chave(match):
        palavra = match.group(0)
        if palavra in palavras_chave:
            valor_ficticio = palavras_chave[palavra]()
            dados_gerados[palavra] = valor_ficticio
            return str(valor_ficticio)
        return palavra

    padrao = re.compile(r'\b(' + '|'.join(re.escape(p) for p in palavras_chave.keys()) + r')\b')
    texto_substituido = padrao.sub(substituir_palavra_chave, texto.lower())

    return {"texto": texto_substituido, "dados_gerados": dados_gerados}

# Exemplo de uso
if __name__ == "__main__":
    json_data = {
        "Nome": "primeiro nome",
        "Sobrenome": "sobrenome",
        "Email": "email",
    }
    print(fake_json(json_data))

    texto_sql = "SELECT nome, idade, cidade FROM usuarios WHERE ativo = 1"
    print(fake_sql(texto_sql))
