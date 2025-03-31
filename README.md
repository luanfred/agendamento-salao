# Projeto Leila Salão

Este é o sistema de gerenciamento para o **Leila Salão**, desenvolvido utilizando **Django** como framework web e **MySQL** como banco de dados. 

## Funcionalidades

- **Gestão de Agendamentos**: Permite que os clientes realizem agendamentos de serviços no salão, escolhendo o horário e o serviço desejado.
- **Cadastro de Usuários**:
  - **Clientes**: Podem se cadastrar no sistema sem a necessidade de fornecer uma chave. Apenas informações básicas, como nome e e-mail, são solicitadas.
  - **Funcionários**: Precisam informar uma chave de acesso para se cadastrar, garantindo que apenas usuários autorizados tenham acesso à área administrativa do salão.
  
  A **chave de acesso padrão** para funcionários é `123456`. Para alterá-la, o usuário precisa ser um **funcionário** e deve clicar no **botão lateral do menu** em **Parâmetros**, onde poderá mudar a chave conforme necessário.

## Pré-requisitos

Antes de rodar o projeto, você precisa ter os seguintes programas instalados em sua máquina:

- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/install/)
  
## Como rodar o projeto

### Passo 1: Clonar o repositório

Clone o repositório para a sua máquina local:

```bash
git clone https://github.com/luanfred/agendamento-salao.git
cd agendamento-salao
```

### Passo 2: Rodar o Docker Compose
Execute o seguinte comando para iniciar os containers do Docker:

```bash
docker-compose up -d
```

### Passo 3: Acesssar o sistema
Após iniciar os containers, você pode acessar o sistema através do seguinte link:
[http://localhost:8000](http://localhost:8000)

