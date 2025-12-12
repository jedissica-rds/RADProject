# RAD: Resumidor de Arquivos e Documentos

Sistema inteligente para análise e resumo automático de documentos PDF utilizando modelos de linguagem.

## Sobre o Projeto

O RAD é uma ferramenta de linha de comando que processa arquivos PDF, extraindo métricas relevantes e gerando resumos estruturados e formais do conteúdo. Utiliza o modelo Gemma-2-2b-it do Google para produzir resumos coerentes em português brasileiro.

## Funcionalidades

- **Análise de Métricas**: Extração de estatísticas do documento (páginas, palavras, vocabulário)
- **Extração de Imagens**: Salva todas as imagens contidas no PDF
- **Geração de Resumos**: Criação de resumos formais e estruturados
- **Dois Modos de Processamento**:
  - Normal: Resumo detalhado e coerente (mais lento)
  - Batch: Processamento rápido em lotes (mais rápido)
- **Relatório Completo**: Exportação de relatório em Markdown com todas as análises

## Instalação

### Requisitos

- Python 3.8+
- CUDA (opcional, para aceleração por GPU)

### Dependências

```bash
pip install torch transformers pymupdf
```

### Instalação do Projeto

```bash
git clone https://github.com/seu-usuario/RADProject.git
cd RADProject
```

## 💻 Uso

### Modo Interativo

```bash
python main.py
```

O sistema solicitará o caminho do arquivo PDF.

### Modo com Argumento

```bash
python main.py caminho/para/arquivo.pdf
```

### Fluxo de Execução

1. O sistema carrega o PDF e exibe as métricas
2. Extrai as imagens do documento
3. Solicita o modo de processamento (Normal ou Batch)
4. Gera o resumo estruturado
5. Oferece a opção de salvar relatório completo em Markdown

## Métricas Analisadas

- Número de páginas
- Total de palavras
- Tamanho do vocabulário (palavras únicas)
- Top 10 palavras mais frequentes
- Tamanho do arquivo
- Quantidade de imagens extraídas

## Formato do Resumo

Os resumos são gerados seguindo uma estrutura formal com três seções obrigatórias:

- **Objetivo**: Propósito central do documento
- **Resumo**: Desenvolvimento lógico e principais argumentos
- **Conclusão**: Síntese final do conteúdo

## Estrutura do Projeto

```
rad/
├── main.py                 # Ponto de entrada da aplicação
├── cli/
│   └── arguments.py        # Tratamento de argumentos
├── llm/
│   ├── model.py           # Carregamento do modelo
│   ├── prompts.py         # Templates de prompts
│   └── summarize.py       # Lógica de sumarização
├── pdf/
│   ├── extractor.py       # Extração de texto e métricas
│   └── images.py          # Extração de imagens
└── utils/
    ├── formatter.py       # Formatação de saída
    ├── reporter.py        # Geração de relatórios
    ├── stopwords.py       # Lista de stopwords
    └── validators.py      # Validação de arquivos
```

## Configurações

### Modelo de Linguagem

Por padrão, utiliza o `google/gemma-2-2b-it`. Para alterar:

```python
loader = ModelLoader(model_id="seu-modelo-preferido")
```

## Saídas

### Imagens

Salvas em: `./images/[titulo_do_pdf]/`

### Relatórios

Salvos em: `./reports/relatorio_[nome_do_arquivo].md`

## Avaliação

Gostaria que fossem avaliadas:

- Estrutura, Arquitetura e Modularização
- Utilização do prompt, modelo escolhido e configuração de tokens.

## Licença

Este projeto está sob a licença MIT.

## Autor

Desenvolvido para facilitar a análise e compreensão de documentos acadêmicos e profissionais.

## Agradecimentos

- Google pela disponibilização do modelo Gemma
- Comunidade Hugging Face
- Biblioteca PyMuPDF

---
