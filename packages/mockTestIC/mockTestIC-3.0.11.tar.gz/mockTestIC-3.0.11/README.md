description='Este projeto é uma biblioteca Python chamada mockTestIC que utiliza a biblioteca Faker para gerar dados fictícios com base em um mapeamento pré-definido. Ela permite que desenvolvedores criem rapidamente dados simulados para testes e desenvolvimento, facilitando a validação de sistemas e reduzindo a necessidade de dados reais durante o desenvolvimento.'

install_requires=[
    'faker',
    'setuptools',
]

# mockTestIC
Este script Python utiliza a biblioteca Faker para gerar dados fictícios de acordo com as chaves especificadas em um dicionário de entrada. As principais funções são `fake_json`, `fake_json_for` e `fake_sql`, cada uma atendendo a diferentes necessidades de geração de dados.

## Como usar

### Passo 1: Instalação
Para utilizar a biblioteca `mockTestIC`, primeiro é necessário instalá-la. Você pode fazer isso executando o seguinte comando no terminal:

```sh
pip install mockTestIC
```

### Passo 2: Importando e Utilizando as Funções
Após a instalação, importe a biblioteca ou a função que deseja utilizar em seu código da seguinte maneira:

```python
from mockTestIC import fake_json, fake_json_for, fake_sql
```

Abaixo, veja exemplos de uso de cada função.

## Funções Disponíveis

### 1. fake_json
A função `fake_json()` gera dados fictícios para um dicionário de entrada onde os valores especificam o tipo de dado desejado.

**Exemplo de uso:**

```python
from mockTestIC import fake_json

dados_json = {
    "Nome": "primeiro nome",
    "Sobrenome": "sobrenome",
    "Email": "email"
}

dados_gerados = fake_json(dados_json)
print(dados_gerados)
```

**Resultado esperado:**
```python
{
    "Nome": "John",
    "Sobrenome": "Doe",
    "Email": "john.doe@example.com"
}
```

### 2. fake_json_for
A função `fake_json_for()` funciona de forma semelhante ao `fake_json`, mas permite a implementação em um loop `for`, facilitando a geração de múltiplas entradas.

**Exemplo de uso:**

```python
from mockTestIC import fake_json_for

dados_json = {
    "primeiro nome": "primeiroNome",
    "sobrenome": "sobreNome",
    "nome completo": "nomeCompleto",
    "nome usuario": "nomeUser",
    "prefixo": "prefixo",
    "suffix": "suffix"
}

dados_gerados = fake_json_for(dados_json)
print(dados_gerados)
```

**Resultado esperado:**
```python
{
    "primeiro nome": "Daniel",
    "sobrenome": "Hays",
    "nome completo": "Lindsey Wilson",
    "nome usuario": "marissahill",
    "prefixo": "Sr.",
    "suffix": "MD"
}
```

### 3. fake_sql
A função `fake_sql()` permite gerar dados fictícios para consultas SQL, substituindo palavras-chave específicas por valores gerados com Faker.

**Exemplo de uso:**

```python
from mockTestIC import fake_sql

sql_string = "INSERT INTO usuarios (id, nome, idade, cidade);"

dados_gerados = fake_sql(sql_string)

print("Dados gerados:", dados_gerados)

sql_com_dados = sql_string.format(**dados_gerados)
print(sql_com_dados)
```

**Resultado esperado:**
```python
Dados gerados: {
    "id": 9170,
    "nome": "Patrick",
    "idade": 34,
    "cidade": "North Katie"
}

INSERT INTO usuarios (9170, 'Patrick', 34, 'North Katie');
```

### Tipos de Dados Suportados

#### Dicionário para `fake_json_for`
Abaixo estão os tipos de dados suportados pela função `fake_json_for`, que podem ser usados como valores no dicionário `dados_json`:

```python
{
    "primeiro nome": "primeiroNome",
    "sobrenome": "sobreNome",
    "nome completo": "nomeCompleto",
    "nome usuario": "nomeUser",
    "prefixo": "prefixo",
    "suffix": "suffix",
    "endereco": "endereco",
    "cidade": "cidade",
    "estado": "estado",
    "pais": "pais",
    "codigo postal": "codigoPostal",
    "endereco rua": "enderecoRua",
    "latitude": "latitude",
    "longitude": "longitude",
    "numero telefone": "numeroTelefone",
    "email": "email",
    "email seguro": "emailSeguro",
    "data nascimento": "dataNasc",
    "data seculo": "dataSec",
    "data decada": "dataDec",
    "horario": "horario",
    "data hora": "dataHora",
    "hora ISO": "horaISO",
    "frase": "frase",
    "paragrafo": "paragrafo",
    "texto": "texto",
    "empresa": "empresa",
    "cargo": "cargo",
    "seguranca social": "segurancaSocial",
    "numero inteiro": "numeroInteiro",
    "elemento": "elemento",
    "amostra": "amostra",
    "numero flutuante": "numeroFlutuante",
    "url": "url",
    "ipv4": "ipv4",
    "ipv6": "ipv6",
    "numero cartao": "numeroCartao",
    "cartao vencimento": "cartaoVencimento"
}
```

#### Dicionário de Palavras-chave para `fake_sql`

A função `fake_sql` suporta as seguintes palavras-chave, que serão substituídas por valores fictícios gerados pela biblioteca Faker:

```python
{
    "id": fake.random_int(min=1, max=9999),
    "nome": fake.first_name(),
    "idade": fake.random_int(min=0, max=120),
    "cidade": fake.city(),
    "profissao": fake.job(),
    "sobrenome": fake.last_name(),
    "completo": fake.name(),
    "usuario": fake.user_name(),
    "prefixo": fake.prefix(),
    "sufixo": fake.suffix(),
    "endereco": fake.address(),
    "estado": fake.state(),
    "pais": fake.country(),
    "cep": fake.zipcode(),
    "rua": fake.street_address(),
    "latitude": fake.latitude(),
    "longitude": fake.longitude(),
    "celular": fake.phone_number(),
    "telefone": fake.phone_number(),
    "email": fake.email(),
    "nascimento": fake.date_of_birth().strftime('%Y-%m-%d'),
    "cadastro": fake.date_time().strftime('%Y-%m-%d'),
    "horario": fake.time(),
    "descricao": fake.text(),
    "empresa": fake.company(),
    "cargo": fake.job(),
    "site": fake.url(),
    "linkedin": fake.url(),
    "ipv4": fake.ipv4(),
    "ipv6": fake.ipv6(),
    "cartao": fake.credit_card_number(),
    "credito": fake.credit_card_number(),
    "cpf": str(fake.random_int(min=11111111111, max=99999999999)),
    "rg": str(fake.random_int(min=111111111, max=999999999)),
    "estoque": fake.random_int(min=0, max=99999),
    "texto": fake.text(),
    "salario": fake.random_int(min=100, max=99999),
    "ativo": fake.boolean()
}
```

## Contato
Caso tenha dúvidas ou precise de mais informações, você pode entrar em contato:

- **Email**: victoraugustodocarmo32@gmail.com
- **LinkedIn**: [Victor Augusto](https://www.linkedin.com/in/victor-augusto-2b01a71a6/)
- **GitHub**: [@Augustoo22](https://github.com/Augustoo22)
