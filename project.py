import PyPDF2
import os
import re
from datetime import datetime

# Caminho do arquivo PDF de exemplo
# pdf_filepath = fr"\\172.21.48.102\grupos$\RH\TOMADORES\VIGILANCIA\DIA 10\SITE\TRT - TRIBUNAL REGIONAL DO TRABALHO\2023\082023\01 DOCUMENTOS AGOSTO 2023\COMPROVANTE DE PAGAMENTO\0509 COMP 350 SALARIO.pdf"
pdf_filepath = fr"C:\Users\localuser\Documents\Lucas\Python\Arquivo Entrada\2023\082023\0509 COMP 350 SALARIO.pdf"
pdf_filepath = fr"C:\Users\localuser\Documents\Lucas\Python\Arquivo Entrada\2023\082023\0509 COMP 350 SALARIO.pdf"
# Extração do mês e ano do nome do arquivo
match = re.search(r'\\(\d{4})\\(\d{2})\d{4}\\', pdf_filepath)
if not match:
    raise ValueError("Mês e ano não encontrados no caminho do arquivo.")

ano, mes = match.groups()
mes_nome = datetime.strptime(mes, "%m").strftime("%B").upper()

# Atualização do diretório de saída com base no mês e ano extraídos
# output_directory = fr"\\172.21.48.102\grupos$\RH\TOMADORES\VIGILANCIA\DIA 10\SITE\TRT - TRIBUNAL REGIONAL DO TRABALHO\{ano}\{mes}{ano}\01 DOCUMENTOS {mes_nome} {ano}\COMPROVANTE DE PAGAMENTO\Comp Renomeados"
output_directory = fr"C:\Users\localuser\Documents\Lucas\Python\Arquivo Saida\{ano}\{mes}{ano}"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

with open(pdf_filepath, "rb") as pdf_file:
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)
    print(f"Total de páginas: {num_pages}")

    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        page_text = page.extract_text()
        print(f"Texto da página {page_num + 1}: {page_text[:228]}...")

        match = re.search(r'INTERSEPT SEGURANCA LTDA\s*\d+\s*([\w\s]+)', page_text)
        if match:
            person_name = match.group(1).strip()
            print(f"Nome encontrado: {person_name}")

            valid_filename = re.sub(r'[<>:"/\\|?*]', '', person_name)
            output_filepath = os.path.join(output_directory, f"{valid_filename}.pdf")
            print(f"Salvando arquivo em: {output_filepath}")

            pdf_writer = PyPDF2.PdfWriter()
            pdf_writer.add_page(page)

            with open(output_filepath, "wb") as output_pdf:
                pdf_writer.write(output_pdf)
                print(f"Arquivo salvo: {output_filepath}")
        else:
            print(f"Nome não encontrado na página {page_num + 1}.")
