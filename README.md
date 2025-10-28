# 📄 Gerador Automatizado de Dossiês Contábeis

🚀 **Automatize a geração de documentos contábeis em segundos!**
Este projeto oferece uma interface web simples e poderosa para criar **dossiês contábeis completos (DOCX)** — combinando dados dinâmicos, imagens e arquivos Markdown.

🧩 Baseado em **Python**, **Streamlit**, **docxtpl** e **python-docx**.

---

## 🧠 1. Visão Geral

O objetivo é **simplificar e padronizar a criação de documentos financeiros**, permitindo que o usuário:

* insira informações da empresa e dos sócios/administradores,
* envie imagens de balanços e demonstrações de resultados,
* e anexe documentos complementares (Notas Explicativas e Carta de Responsabilidade).

No final, o sistema gera **um arquivo DOCX pronto para uso profissional** 📘

---

## ⚙️ Tecnologias Utilizadas

| Tecnologia                    | Função Principal                             |
| ----------------------------- | -------------------------------------------- |
| 🐍 **Python**                 | Linguagem principal do projeto               |
| 🌐 **Streamlit**              | Interface web para entrada de dados          |
| 🧾 **docxtpl (DocxTemplate)** | Renderização dinâmica do template DOCX       |
| 📄 **python-docx**            | Manipulação avançada de documentos DOCX      |
| 🔄 **pypandoc**               | Conversão de arquivos Markdown (.md) em DOCX |

---

## 🧩 2. Pré-requisitos

Antes de rodar o projeto, instale:

* **Python 3.7+**
* **pip** (gerenciador de pacotes)
* **Pandoc** → necessário para o `pypandoc` funcionar corretamente

📥 **Instalação do Pandoc:**

```bash
sudo apt-get install pandoc
```

ou siga o guia oficial: [https://pandoc.org/installing.html](https://pandoc.org/installing.html)

---

## 🧰 3. Instalação e Configuração

### A. Instalar dependências

Dentro do seu ambiente virtual, execute:

```bash
pip install streamlit docxtpl python-docx pypandoc
```

### B. Estrutura de diretórios esperada

```
/seu_diretorio_projeto
├── app_gerador.py           # Script principal do Streamlit
└── templete_base_ofc.docx   # Template DOCX com marcadores Jinja2
```

> 💡 Se o template estiver em um caminho fixo (ex: `/home/pasta1/desafio/`), garanta que ele seja acessível ao servidor Streamlit.

---

## 🖥️ 4. Instruções de Uso

### 🏃‍♀️ A. Executando a aplicação

No terminal, rode:

```bash
streamlit run app_gerador.py
```

Isso abrirá automaticamente o app no navegador → [automatizardossie](https://automatizardossie.streamlit.app/)

---

### 🧭 B. Guia da Interface

A interface é organizada em **3 abas** principais:

#### 📁 Aba 1 — Dados da Empresa e Período

Campos:

* Nome Fantasia
* Razão Social
* CNPJ
* Período Anual
* Datas de Encerramento e Referência

#### 👥 Aba 2 — Dados dos Administradores

Campos:

* Nome completo
* Cargo (novo campo adicionado)
* CPF

#### 📎 Aba 3 — Upload de Arquivos

Uploads obrigatórios (5 arquivos):

| Tipo        | Nome no Sistema                 | Formato          | Inserção no DOCX             |
| ----------- | ------------------------------- | ---------------- | ---------------------------- |
| 📊 Imagem   | Balanço Patrimonial (Parte 1)   | `.png` ou `.jpg` | InlineImage                  |
| 📊 Imagem   | Balanço Patrimonial (Parte 2)   | `.png` ou `.jpg` | InlineImage                  |
| 📈 Imagem   | Demonstração do Resultado (DRE) | `.png` ou `.jpg` | InlineImage                  |
| 📘 Markdown | Notas Explicativas              | `.md`            | Substitui `[[EXP_DEMONSTR]]` |
| 📘 Markdown | Carta de Responsabilidade       | `.md`            | Substitui `[[CARTA_RESP]]`   |

---

### 🧾 C. Geração e Download

Após preencher tudo, clique em:

```
✅ GERAR DOCUMENTO FINAL
```

O Streamlit exibirá uma mensagem de carregamento enquanto o Python:

1. Salva os arquivos temporários
2. Converte `.md → .docx` via `pypandoc`
3. Renderiza o template `docxtpl`
4. Substitui os blocos via `python-docx`

📦 Resultado:
Um arquivo como

```
Dossie_Contabil_<NOME_EMPRESA>.docx
```

pronto para download direto da interface.

---

## 🧑‍💻 5. Notas Técnicas

### 🔹 Arquivos Temporários

O script usa o módulo `tempfile` para armazenar temporariamente todos os uploads e conversões, garantindo limpeza automática no final da execução.

### 🔹 Substituição de Conteúdo

O projeto combina:

* **docxtpl** → para variáveis simples e imagens
* **python-docx** → para inserir documentos inteiros (Notas/Carta) nos marcadores

Isso mantém a **formatação completa dos blocos Markdown** ao incorporar no DOCX final.

---

## 📜 Licença

Este projeto é distribuído sob a licença MIT.
Sinta-se à vontade para usar, adaptar e contribuir! 🤝
