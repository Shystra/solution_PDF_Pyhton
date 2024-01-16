import PyPDF2
import os
import re

pdf_filepath = "Diretório"
output_directory = "Diretório"

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

        # Tente encontrar o nome após "Nome:Destino" usando regex
        match = re.search(r'INTERSEPT SEGURANCA LTDA\s*\d+\s*([\w\s]+)', page_text)

        if match:
            person_name = match.group(1).strip()
            print(f"Nome encontrado: {person_name}")

            # Removendo caracteres inválidos do nome do arquivo
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
