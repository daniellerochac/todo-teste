# 📌 Todo Teste

Projeto de API para gerenciamento de tarefas desenvolvido com FastAPI.

---

## 🚀 Tecnologias

- [FastAPI](https://fastapi.tiangolo.com/)
- SQLAlchemy
- Alembic
- PyJWT
- Poetry
- Ruff (lint e format)
- Pytest (testes unitários)
- Taskipy (task runner)

---

## 📦 Instalação

1. **Clone o repositório**
   ```bash
   git clone https://github.com/daniellerochac/todo-teste.git
   cd todo-teste

2. **Instale as dependências**
   > Certifique-se de ter o [Poetry](https://python-poetry.org/docs/#installation) instalado.
   ```bash
   poetry install
   ```

---

## ▶️ Rodando a API localmente

1. **Ative o ambiente virtual**
   ```bash
   poetry shell
   ```

2. **Execute a API**
   ```bash
   task run
   ```

3. Acesse no navegador:  
   [http://localhost:8000/docs](http://localhost:8000/docs)

---
## 🧪 Executando os testes

1. **Ative o ambiente virtual**
   ```bash
   poetry shell
   ```

2. **Execute os testes**
   ```bash
   task test
   ```

3. **Verifique o relatório de cobertura (opcional)**
   Após rodar os testes, um relatório HTML estará disponível na pasta `htmlcov`.  
   Para abrir:
   ```bash
   open htmlcov/index.html
   ```

---

## 📄 Licença

Este projeto está sob a licença MIT.