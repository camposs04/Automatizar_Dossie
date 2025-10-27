📄 Gerador Automatizado de Dossiês Contábeis

Este projeto fornece uma interface web simples e eficaz para automatizar a geração de dossiês contábeis em formato DOCX, combinando dados variáveis de texto, uploads de imagens e conteúdos Markdown. Utiliza as bibliotecas Python docxtpl e python-docx para renderização e o Streamlit para a interface.

1. Visão Geral do Projeto

O objetivo principal é simplificar o processo de criação de documentos financeiros padronizados. O sistema permite que o usuário insira informações da empresa, dados de sócios/administradores, e faça o upload de representações visuais (balanços, DREs) e documentos complementares (Notas Explicativas, Carta de Responsabilidade) para gerar um documento final pronto para uso.

Tecnologias Utilizadas:

Python: Linguagem de programação principal.

Streamlit: Para a interface web de entrada de dados.

DocxTemplate (docxtpl): Para preencher o template DOCX com dados e imagens.

python-docx: Para manipulação avançada e inserção de conteúdo dinâmico (Markdown convertido).

pypandoc: Para converter arquivos Markdown (.md) em formato DOCX.

2. Pré-requisitos

Para executar este projeto, você precisará ter instalado:

Python 3.7+

Pip (gerenciador de pacotes do Python)

Pandoc: Ferramenta de conversão de documentos necessária para que o pypandoc funcione.

Instalação do Pandoc: Siga as instruções oficiais em [https://pandoc.org/installing.html]. No Linux/Debian, geralmente é sudo apt-get install pandoc.

3. Configuração e Instalação

A. Instalação de Dependências

No seu terminal, dentro do ambiente virtual do projeto, execute:

pip install streamlit docxtpl python-docx pypandoc


B. Estrutura de Arquivos

Certifique-se de que a estrutura de arquivos do seu projeto esteja configurada corretamente. O arquivo principal app_gerador.py e o template base devem estar acessíveis:

/seu_diretorio_projeto
├── app_gerador.py        # O script Streamlit com toda a lógica
└── templete_base_ofc.docx # O template DOCX com os marcadores Jinja2


Observação: Se o templete_base_ofc.docx estiver em outro caminho fixo, como /home/camposs/Desktop/estagio/desafio/, certifique-se de que este caminho está acessível pelo servidor que roda o Streamlit.

4. Instruções de Uso

A. Executando a Aplicação

Para iniciar a interface web, navegue até o diretório do projeto no terminal e execute:

streamlit run app_gerador.py


O Streamlit iniciará um servidor local e abrirá automaticamente a aplicação no seu navegador padrão (geralmente em http://localhost:8501).

B. Guia da Interface (Três Abas)

A interface é dividida em três abas principais para organizar a entrada dos dados:

Aba 1: Dados da Empresa/Períodos

Preencha os campos de texto que serão mapeados diretamente para o template, incluindo:

Nome Fantasia

Razão Social

CNPJ (formato sugerido)

Período Anual (descrição)

Datas de Encerramento e Referência

Aba 2: Dados dos Administradores

Preencha os dados dos dois sócios/administradores:

Nome completo

Cargo (Este é um novo campo adicionado ao template)

CPF (formato sugerido)

Aba 3: Upload de Arquivos

Esta é a seção mais crucial. Você deve fazer o upload de cinco (5) arquivos obrigatórios que serão incorporados ao documento final:

Tipo de Conteúdo

Nome do Campo

Formato Esperado

Uso no Documento

Imagens

Balanço Patrimonial (Parte 1)

PNG ou JPG

Inserido como InlineImage

Imagens

Balanço Patrimonial (Parte 2)

PNG ou JPG

Inserido como InlineImage

Imagens

Demonstração do Resultado (DRE)

PNG ou JPG

Inserido como InlineImage

Conteúdo

Notas Explicativas

Arquivo Markdown (.md)

Convertido para DOCX e substituído no marcador [[EXP_DEMONSTR]]

Conteúdo

Carta de Responsabilidade

Arquivo Markdown (.md)

Convertido para DOCX e substituído no marcador [[CARTA_RESP]]

C. Geração e Download

Após preencher todos os campos e fazer o upload de todos os 5 arquivos, clique no botão:

✅ GERAR DOCUMENTO FINAL

O Streamlit exibirá uma mensagem de "Gerando documento..." enquanto o Python salva os uploads, executa o pypandoc, renderiza o template docxtpl, e realiza a substituição dos blocos DOCX.

Em caso de sucesso, será exibido um botão de Download com o nome do arquivo personalizado (ex: Dossie_Contabil_TESTE do Nome.docx).

Em caso de erro (ex: falha no pypandoc por falta do Pandoc, ou arquivo de template não encontrado), uma mensagem de erro será exibida.

5. Notas Técnicas sobre o Código

Arquivos Temporários: A função generate_document utiliza o módulo tempfile para salvar temporariamente todos os arquivos de upload e os documentos intermediários gerados pelo pypandoc. Isso garante que o disco do servidor seja limpo após cada geração (bloco finally).

Substituição de Conteúdo: O projeto usa uma abordagem híbrida: docxtpl para variáveis simples e imagens, e python-docx (função insert_docx_at_placeholder) para incorporar documentos DOCX completos (Notas e Carta) no lugar de marcadores de texto ([[MARCADOR]]), preservando formatação complexa.