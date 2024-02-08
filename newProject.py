import PyPDF2
import os
import re
from datetime import datetime

# Diretório de entrada onde os arquivos PDF estão localizados
# input_directory = fr"C:\Users\localuser\Documents\Lucas\Python\Arquivo Entrada"
# input_directory = r"\\172.21.48.102\grupos$\RH\TOMADORES\VIGILANCIA\DIA 10\SITE\TRT - TRIBUNAL REGIONAL DO TRABALHO\Entrada - 2024\2024\012024\01 DOCUMENTOS JANEIRO 2024\COMPROVANTE"

current_directory = os.path.dirname(os.path.realpath(__file__))
input_directory = current_directory

path_directory = r'\\172.21.48.102\grupos$\RH\TOMADORES\VIGILANCIA\DIA 10\SITE\TRT - TRIBUNAL REGIONAL DO TRABALHO\Saida - 2024\{ano}\{mes} {ano}\Arquivo'
def process_pdf_files(input_directory):
    for root, dirs, files in os.walk(input_directory):
        for file in files:
            if file.endswith(".pdf"):
                pdf_filepath = os.path.join(root, file)
                print(f"Encontrado PDF: {pdf_filepath}")
                match = re.search(r'(\d{2})(\d{4})\.pdf$', file)
                if match:
                    mes, ano = match.groups()
                    mes_nome = datetime.strptime(mes, "%m").strftime("%B").upper()
                    output_directory = path_directory.format(ano=ano, mes=mes_nome)
                    if not os.path.exists(output_directory):
                        os.makedirs(output_directory)
                    process_single_pdf(pdf_filepath, output_directory)  # Ajuste aqui
                else:
                    print(f"Mês e ano não encontrados no caminho do arquivo: {pdf_filepath}")

def process_single_pdf(pdf_filepath, output_directory):
    # Abrir o arquivo PDF uma única vez
    with open(pdf_filepath, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            match = re.search(r'INTERSEPT SEGURANCA LTDA\s*\d+\s*([\w\s]+)', page_text)
            
            if match:
                person_name = match.group(1).strip()
                valid_filename = re.sub(r'[<>:"/\\|?*]', '', person_name)
                output_filepath = os.path.join(output_directory, f"{valid_filename}.pdf")

                pdf_writer = PyPDF2.PdfWriter()
                pdf_writer.add_page(page)

                with open(output_filepath, "wb") as output_pdf:
                    pdf_writer.write(output_pdf)
                    print(f"Arquivo renomeado e salvo: {output_filepath}")
            else:
                print(f"Nome não encontrado na página {page_num + 1}.")

process_pdf_files(current_directory)


