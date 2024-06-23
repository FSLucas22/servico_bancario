# Desafio
Cada versão do aplicativo está em uma branch do projeto. A branch main terá a última versão do projeto. Atualmente, o projeto está na versão 2.

# V1
Fomos contratados por um grande banco para desenvolver o seu novo sistema bancário. Esse banco deseja modernizar suas operações e para isso escolheu a linguagem Python. Para a primeira versão do sistema devemos implementar apenas 3 operações: depósito, saque e extrato.

## Operação de depósito
Deve ser possível depositar valores positivos para a minha conta bancária. A versão 1 do projeto trabalha apenas com 1 usuário, dessa forma não precisamos nos preocupar em identificar qual é o número da agência e conta bancária. Todos os depósitos devem ser armazenados em uma variável e exibidos na operação de extrato.

## Operação de saque
O sistema deve permitir realizar 3 saques diários com limite máximo de R$ 500,00 por saque. Caso o usuário não tenha saldo em conta, o sistema deve exibir uma mensagem informando que não será possível sacar o dinheiro por falta de saldo. Todos os saques devem ser armazenados em uma variável e exibidos na operação de extrato.

## Operação de extrato
Essa operação deve listar todos os depósitos e saques realizados na conta. No fim da listagem deve ser exibido o saldo atual da conta. Se o extrato estiver em branco, exibir a mensagem: Não foram realizadas movimentações.

Os valores devem ser exibidos utilizando o formato R$ xxx.xx,
Exemplo: 1500.45 = R$ 1500.45

# V2
Para esta segunda versão, devemos implementar duas novas funções: criar usuário (cliente do banco) e criar conta corrente (vincular com usuário). As funções do código deverão seguir regras para a forma de seus argumentos.

- A função de saque somente deve receber argumentos de forma keyword only
- A função depósito somente deve receber argumentos de forma positional only
- A função de extrato deve receber argumentos de forma positional only e keyword only. Argumentos posicionais: saldo, argumentos nomeados: extrato.
- O programa deve armazenar os usuários em uma lista. Um usuário é composto por nome, data de nascimento, cpf e endereço. O endereço é uma string com o formato: logradouro, nro - bairro - cidade/sigla estado. Deve ser armazenado somente os números do CPF. Não podemos cadastrar 2 usuários com o mesmo CPF.
- O programa deve armazenar contas em uma lista. Uma conta é composta por: Agência, número da conta e usuário. O número da conta é sequencial, iniciado em 1. O número da agência é fixo: "0001". O usuário pode ter mais de uma conta, mas uma conta pertence a somente um usuário.