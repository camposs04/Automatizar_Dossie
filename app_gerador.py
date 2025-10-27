import streamlit as st
import os
import tempfile
from docxtpl import DocxTemplate, InlineImage
from docx import Document
from docx.shared import Inches
import pypandoc
from io import BytesIO

# --- 1. Mover a Lógica de Geração para uma Função ---

# Seu código de geração de documento deve ser uma função isolada
def generate_document(input_data):
    # Dicionário para armazenar caminhos temporários de arquivos de upload
    temp_paths = {}
    
    # === A) Preparar Caminhos Temporários para Imagens e MDs ===
    
    # Salvar uploads em disco temporariamente para que o docxtpl/pypandoc possa acessá-los
    for key, uploaded_file in input_data['uploads'].items():
        if uploaded_file is not None:
            # 1. Criar um arquivo temporário
            suffix = os.path.splitext(uploaded_file.name)[1]

            # Use 'NamedTemporaryFile' para obter um caminho real no sistema de arquivos
            # delete=False é necessário para que outros processos possam usar o arquivo antes que ele seja fechado
            # Usar 'with' ou garantir a exclusão é crucial
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                temp_paths[key] = tmp_file.name
        else:
            # Caso algum upload seja opcional ou queira usar um placeholder
            # Você precisará tratar isso dependendo se o arquivo é obrigatório ou não.
            st.error(f"O arquivo {key} é obrigatório!")
            return None, None # Retorna erro
    
    # === B) Definir os Caminhos Finais para a Lógica de Geração ===
    
    # Adaptar seus caminhos fixos (apenas o template principal pode ser fixo aqui)
    CAMINHO_TEMPLETE = "/home/camposs/Desktop/estagio/desafio/templete_base_ofc.docx" # Coloque seu template na mesma pasta
    
    # Criar caminhos temporários para os arquivos gerados (DOCX temporários)
    TEMP_BASE_DOCX = os.path.join(tempfile.gettempdir(), "temporario_base.docx")
    TEMP_CART_DOCX = os.path.join(tempfile.gettempdir(), "temp_cart.docx")
    TEMP_RENDERED = os.path.join(tempfile.gettempdir(), "temp_rendered.docx")
    
    final_docx_buffer = BytesIO() # Usar buffer in-memory para o arquivo final

    try:
        # === 1. Converter os arquivos Markdown para DOCX temporários ===
        pypandoc.convert_file(temp_paths['explic_demonstr_file'], 'docx', outputfile = TEMP_BASE_DOCX)
        pypandoc.convert_file(temp_paths['carta_responsb_file'], 'docx', outputfile = TEMP_CART_DOCX)
        
        # === 2. Carregar o template principal e Inserir imagens ===
        doc = DocxTemplate(CAMINHO_TEMPLETE)

        balanco_pt1_img = InlineImage(doc, temp_paths['balanco_pt1_file'], width=Inches(6))
        balanco_pt2_img = InlineImage(doc, temp_paths['balanco_pt2_file'], width=Inches(6))
        demstr_result_img = InlineImage(doc, temp_paths['demstr_result_file'], width=Inches(6))

        # === 3. Contexto do template (com dados da UI) ===
        context = {
            'nome_empresa': input_data['nome_empresa'],
            'periodo_anual': input_data['periodo_anual'],
            'cnpj_empresa': input_data['cnpj_empresa'],
            'data_dem_encerradas': input_data['data_dem_encerradas'],
            'razao_social_empresa': input_data['razao_social_empresa'],
            'periodo_em_data': input_data['periodo_em_data'],
            'balanco_patrimonial_pt1': balanco_pt1_img,
            'balanco_patrimonial_pt2': balanco_pt2_img,
            'demontr_resultado': demstr_result_img,
            'nome_socio1': input_data['nome_socio1'],
            'nome_socio2': input_data['nome_socio2'],
            'cargo_socio1': input_data['cargo_socio1'],
            'cargo_socio2': input_data['cargo_socio2'],
            'cpf_socio1': input_data['cpf_socio1'],
            'cpf_socio2': input_data['cpf_socio2'],
            # Marcadores do método de substituição manual
            'explic_demonstr': '[[EXP_DEMONSTR]]', 
            'carta_responsb': '[[CARTA_RESP]]'
        }

        # === 4. Renderizar e Salvar Temporariamente ===
        doc.render(context)
        doc.save(TEMP_RENDERED)

        # === 5. Inserir os blocos DOCX (Lógica de Substituição) ===
        final_doc = Document(TEMP_RENDERED)
        
        # Sua função 'insert_docx_at_placeholder' deve ser definida fora de 'generate_document'
        # ou importada, mas para simplificar, a usaremos aqui:
        # NOTE: Vou assumir que 'insert_docx_at_placeholder' está no escopo ou importada.
        # Por simplicidade, vou replicá-la rapidamente aqui (sem print's)

        # Esta função precisa ser separada ou importada
        def insert_docx_at_placeholder(main_doc: Document, placeholder: str, insert_doc_path: str):
            insert_doc = Document(insert_doc_path)
            for paragraph in main_doc.paragraphs:
                if placeholder in paragraph.text:
                    paragraph.text = paragraph.text.replace(placeholder, "")
                    for element in reversed(insert_doc.element.body):
                        paragraph._element.addnext(element)
                    return True # Termina após a primeira substituição

        insert_docx_at_placeholder(final_doc, '[[EXP_DEMONSTR]]', TEMP_BASE_DOCX)
        insert_docx_at_placeholder(final_doc, '[[CARTA_RESP]]', TEMP_CART_DOCX)

        # === 6. Salvar no Buffer de Memória para Download ===
        final_doc.save(final_docx_buffer)
        final_docx_buffer.seek(0)
        
        return final_docx_buffer.getvalue(), None

    except Exception as e:
        return None, f"Erro durante a geração: {e}"
    
    finally:
        # === 7. Limpeza (Crucial para o Servidor!) ===
        temp_files_to_clean = [
            TEMP_BASE_DOCX, TEMP_CART_DOCX, TEMP_RENDERED, 
            temp_paths.get('balanco_pt1_file'), temp_paths.get('balanco_pt2_file'), 
            temp_paths.get('demstr_result_file'), temp_paths.get('explic_demonstr_file'), 
            temp_paths.get('carta_responsb_file')
        ]
        
        for temp_file in [f for f in temp_files_to_clean if f]:
            try:
                os.remove(temp_file)
            except Exception:
                pass # Ignorar erro se o arquivo não existe ou já foi limpo


# --- 2. Interface Streamlit ---

st.set_page_config(page_title="Gerador de Demonstrações Contábeis", layout="wide")
st.title("📄 Gerador Automático de Documentos Contábeis")
st.markdown("Preencha os campos e faça o upload dos arquivos para gerar o dossiê final.")

# Estrutura de abas para organizar (Melhora a UI/UX)
tab1, tab2, tab3 = st.tabs(["Dados da Empresa/Períodos", "Dados dos Administradores", "Upload de Arquivos"])

# Dicionário para armazenar todos os inputs
input_data = {}

# === Tab 1: Dados da Empresa/Períodos ===
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        input_data['nome_empresa'] = st.text_input("Nome Fantasia da Empresa", value="TESTE do Nome")
        input_data['razao_social_empresa'] = st.text_input("Razão Social", value="TESTE RAZAO EMPRESA LTDA SCP VTG")
        input_data['cnpj_empresa'] = st.text_input("CNPJ", value="23.766.826/0001-61", help="Formato: 00.000.000/0000-00")

    with col2:
        input_data['periodo_anual'] = st.text_input("Período Anual (Descrição)", value="Junho a Agosto 2030")
        input_data['data_dem_encerradas'] = st.text_input("Data das Demos. Encerradas", value="07/02/2005", help="Formato: DD/MM/AAAA")
        input_data['periodo_em_data'] = st.text_input("Período de Referência", value="07 a 12/2030")

# === Tab 2: Dados dos Sócios ===
with tab2:
    st.subheader("Dados dos Administradores")
    col3, col4 = st.columns(2)
    
    with col3:
        input_data['nome_socio1'] = st.text_input("Nome do Sócio 1", value="Nome TesTE 1")
        input_data['cargo_socio1'] = st.text_input("Cargo do Sócio 1", value = "Cargo Teste 1")
        input_data['cpf_socio1'] = st.text_input("CPF do Sócio 1", value="089.038.947-98")
    
    with col4:
        input_data['nome_socio2'] = st.text_input("Nome do Sócio 2", value="Nome TesTE 2")
        input_data['cargo_socio2'] = st.text_input("Cargo do Sócio 2", value = "Cargo Teste 2")
        input_data['cpf_socio2'] = st.text_input("CPF do Sócio 2", value="089.128.947-97")

# Dicionário para uploads
input_data['uploads'] = {}

# === Tab 3: Upload de Arquivos ===
with tab3:
    st.subheader("Imagens de Demonstrações (PNG ou JPG)")
    col5, col6 = st.columns(2)
    
    with col5:
        input_data['uploads']['balanco_pt1_file'] = st.file_uploader("Balanco Patrimonial (Parte 1)", type=["png", "jpg"], key='balanco_1')
        input_data['uploads']['balanco_pt2_file'] = st.file_uploader("Balanco Patrimonial (Parte 2)", type=["png", "jpg"], key='balanco_2')
    with col6:
        input_data['uploads']['demstr_result_file'] = st.file_uploader("Demonstração do Resultado (DRE)", type=["png", "jpg"], key='dre')

    st.subheader("Arquivos de Texto (Markdown)")
    col7, col8 = st.columns(2)
    with col7:
        input_data['uploads']['explic_demonstr_file'] = st.file_uploader("Notas Explicativas", type=["md"], key='notas')
    with col8:
        input_data['uploads']['carta_responsb_file'] = st.file_uploader("Carta de Responsabilidade", type=["md"], key='carta')


# --- 3. Botão de Execução e Download ---

if st.button("✅ GERAR DOCUMENTO FINAL"):
    # Verifica se todos os arquivos obrigatórios foram upados
    required_files = [
        'balanco_pt1_file', 'balanco_pt2_file', 'demstr_result_file', 
        'explic_demonstr_file', 'carta_responsb_file'
    ]
    
    all_files_uploaded = all(input_data['uploads'][f] is not None for f in required_files)
    
    if all_files_uploaded:
        with st.spinner("Gerando documento... Isso pode levar alguns segundos."):
            file_data, error = generate_document(input_data)
        
        if file_data:
            st.success("Documento gerado com sucesso!")
            st.download_button(
                label="Clique para Baixar Document.docx",
                data=file_data,
                file_name=f"Dossie_Contabil_{input_data['nome_empresa']}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        else:
            st.error(f"Falha na geração do documento. Detalhes: {error}")
            
    else:
        st.warning("Por favor, faça o upload de todos os 5 arquivos antes de gerar.")