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

```bash
pip install streamlit docxtpl python-docx pypandoc
```

### B. Estrutura de diretórios

```
/seu_diretorio_projeto
├── app_gerador.py
└── templete_base_ofc.docx
```

---

## 🖥️ 4. Instruções de Uso

Você pode usar o gerador diretamente pelo site oficial publicado no Streamlit:
👉 [automatizar_dossie](https://automatizardossie.streamlit.app/)

Caso prefira rodar localmente, siga as instruções abaixo:

### IMPORTANTE ⚠️

Para o correto funcionamento da aplicação, o usuário **DEVE obrigatoriamente seguir os formatos exigidos para cada arquivo enviado**, conforme as especificações abaixo. **Arquivos fora do formato serão rejeitados.**

Além disso, **é proibido incluir títulos** dentro dos arquivos:

* **Notas Explicativas (.md)** → não deve conter título como "Notas Explicativas" no início
* **Carta de Responsabilidade (.md)** → não deve conter título como "Carta de Responsabilidade" dentro do arquivo

Os títulos já são gerados automaticamente pelo sistema no documento final.

---

### 🏃‍♀️ A. Executando a aplicação

```bash
streamlit run app_gerador.py
```

---

### 🧭 B. Guia da Interface

A interface possui 3 abas:

#### 📁 Aba 1 — Dados da Empresa e Período

* Nome Fantasia
* Razão Social
* CNPJ
* Período Anual
* Datas de Encerramento e Referência

#### 👥 Aba 2 — Dados dos Administradores

* Nome completo
* Cargo
* CPF

#### 📎 Aba 3 — Upload de Arquivos

| Tipo                            | Formato obrigatório | Inserção no DOCX | Observação importante        |
| ------------------------------- | ------------------- | ---------------- | ---------------------------- |
| Balanço Patrimonial (Parte 1)   | .png/.jpg           | Imagem           | seguir orientação de tamanho |
| Balanço Patrimonial (Parte 2)   | .png/.jpg           | Imagem           | seguir orientação de tamanho |
| Demonstração do Resultado (DRE) | .png/.jpg           | Imagem           | seguir orientação de tamanho |
| Notas Explicativas              | .md                 | Conteúdo textual | **sem título interno**       |
| Carta de Responsabilidade       | .md                 | Conteúdo textual | **sem título interno**       |

---

## 🧾 5. Geração do Documento Final

Após o preenchimento:

1. Salva uploads temporários
2. Converte `.md → .docx`
3. Renderiza o template
4. Insere seções no DOCX final

Saída: `Dossie_Contabil_<NOME_EMPRESA>.docx`

---

## 📜 Licença

Projeto sob licença MIT.
