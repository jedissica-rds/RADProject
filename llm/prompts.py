def create_prompt(text: str):
    prompt_final = f"""Resuma o texto abaixo em português formal e acadêmico, de no máximo 800 alavras, organizando em três seções:

### Objetivo
Descreva o propósito e finalidade do documento original.

### Resumo Geral
Apresente os principais argumentos, conceitos e desenvolvimento lógico do conteúdo. Explore tópicos, seções e acontecimentos relevantes mantendo a estrutura organizacional do texto.

### Conclusão
Sintetize os pontos-chave e implicações apresentadas.

Diretrizes:
- Use tom impessoal e voz passiva
- Empregue vocabulário técnico apropriado
- Evite simplificações ou opiniões pessoais
- Não use primeira pessoa (eu, nós)

Texto: {text}

Resumo:"""

    return prompt_final


def create_fast_prompt(text: str):
    prompt_final = f"""Resuma formalmente este trecho em português acadêmico:

{text}

Resumo formal e objetivo:"""

    return prompt_final