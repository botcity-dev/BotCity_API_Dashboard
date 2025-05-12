# Dashboard - How To Use

## 1. Configuração de Credenciais

- Configure as credenciais no arquivo `app/configurations.py`, definindo os seguintes parâmetros:
  - `MAESTRO_KEY`
  - `MAESTRO_WORKSPACE`
  - `MAESTRO_LOGIN`

- Consulte a documentação oficial para obter essas informações: [Documentação BotCity - Ambiente de Desenvolvimento] (https://documentation.botcity.dev/pt/maestro/features/dev-environment/).

### Observações importantes:
- Caso as variáveis ainda não estejam criadas no ambiente do sistema, será necessário **reiniciar a máquina** após a criação para que o sistema reconheça as novas variáveis.
- O **nome das variáveis** deve ser exatamente o mesmo utilizado no código. Elas podem ser customizadas, mas devem manter a consistência na chamada da função que lê essas variáveis.

---

## 2. Preparação do Ambiente

- Crie um ambiente virtual (venv) para o projeto:
  ```bash
  python -m venv venv
