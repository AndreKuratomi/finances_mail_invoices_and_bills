# import codecs

# # hex_values = "507974686f6e" 
# # result_string = codecs.decode(hex_values, 'hex').decode('utf-8')
# asd = "$862462030169477,A,Q,CEL,S23.5953,W046.8798,18,0,C010104,000040,4169,097,060,000,+26,000000,01,1,0,-00,+00,000000000000000*"
# result_string = codecs.decode(asd, 'hex').decode('utf-8')
 
# print(result_string)
# print(type(result_string))
import ipdb
import binascii

# hex_string = "862462030169477,A,Q,CEL,S23.595 3,W046.8798,18,0,C010104,000040,4 169,097,060,000,+26,000000,01,1,0,- 00,+00,000000000000000*"
# hex_string = "86 24 62 03 01 69 477"
hex_string1 = "50 72 6f 6a 65 74 6f 20 64 65 20 69 6e 74 65 67 72 61 63 61 6f 20 64 61 20 58 47 4c 4f 42 41 4c 20 70 61 72 61 20 6f 20 63 6f 6e 74 72 6f 6c 65 20 64 65 20 49 53 43 41 2e 0a 45 73 74 75 64 61 20 65 73 73 61 20 41 50 49 20 61 69 20 70 72 61 20 6e 6f 69 73 20 65 6e 74 72 65 67 61 72 20 65 73 73 61 20 62 61 67 61 63 61 21"
hex_string = "a5401830867869060147667011bd11228534720047154293095226130523000000000f1b3f0b0019000f001e00050000000300fa00fafa000000000000000089551700002066888490190fa3e0000003000000000000000724000000000000000000000000fa0d0a232323"

# new_hex.
# ipdb.set_trace()
# Remove any non-hex characters
hex_string1 = "".join(c for c in hex_string1 if c in "0123456789ABCDEFabcdef")
print(hex_string1)
print(len(hex_string1))
if len(hex_string1) % 2 != 0:
    hex_string1 = "0" + hex_string1

# Convert hex string to bytes
binary_data = bytes.fromhex(hex_string1)
print(binary_data)

result = binary_data.decode('Windows-1252')
print(result)


# import cv2
# import pytesseract
# from pdf2image import convert_from_path
# import ipdb


# import fitz  # PyMuPDF


# # Function to extract text from image using pytesseract
# def extract_text_from_image(image):
#     return pytesseract.image_to_string(image)

# # Function to extract text from PDF
# def extract_text_from_pdf(pdf_path):
#     try:
#         # Open the PDF file
#         with fitz.open(pdf_path) as pdf_document:
#             # Get the first page of the PDF
#             page = pdf_document.load_page(0)
            
#             # Render the page as an image
#             image = page.get_pixmap()
#             ipdb.set_trace()
#             # Extract text from the image
#             extracted_text = extract_text_from_image(image)
            
#             return extracted_text
#     except Exception as e:
#         print("Error:", e)
#         return None

# # Extract text from PDF
# extracted_text = extract_text_from_pdf(pdf_path)
# if extracted_text:
#     print(extracted_text)
# else:
#     print("Failed to extract text from the PDF.")

# # ipdb.set_trace()
# pdf_path = './NFE_17774_FIXO.pdf'

# page_image = convert_from_path(pdf_path)[0]
# # img = cv2.imread("NFE_17774_FIXO.png")
# pytesseract.pytesseract.tesseract_cmd = "C:/Users/andre.kuratomi/Downloads/tesseract-ocr-w64-setup-5.3.3.20231005.exe"


# result = pytesseract.image_to_string(page_image)


# print(result)
# # Path to your PDF file
# pdf_path = 'C:/Users/andre.kuratomi/Desktop/projetos/notas_fiscais_financeiro/NFE_17782_FIXO-MERCK.pdf'
# NFE_17779_FIXO-ECOPORTO.pdf

# IT WORKS, BUT NOT ACCURATELY:
# import fitz  # PyMuPDF
# # import easyocr
# from PIL import Image
# import io

# def extract_text_from_scanned_pdf(pdf_path: str) -> str:
#     extracted_text = ""
#     reader = easyocr.Reader(['pt'])  # Specify languages you want to recognize

#     # Open the PDF file
#     pdf_document = fitz.open(pdf_path)

#     for page in pdf_document:
#         # Convert the page to a PIL image
#         image = page.get_pixmap()

#         # Convert PIL image to bytes
#         img_byte_arr = io.BytesIO()
#         Image.frombytes("RGB", [image.width, image.height], image.samples).save(img_byte_arr, format='PNG')
#         img_byte_arr = img_byte_arr.getvalue()

#         # Perform OCR on the image and append the extracted text
#         result = reader.readtext(img_byte_arr)
#         for detection in result:
#             extracted_text += detection[1] + ' '

#     return extracted_text

# pdf_path = './NFE_17774_FIXO.pdf'

# print(extract_text_from_scanned_pdf(pdf_path))

# https://github.com/AndreKuratomi/finances_tables_to_db_and_mail
# import easyocr


# def extract_text_from_image(image_path):
#     reader = easyocr.Reader(['pt'])
#     result = reader.readtext(image_path)
#     extracted_text = ' '.join([text[1] for text in result])
#     return extracted_text

# print(extract_text_from_image(pdf_path))

# Use on readme
# https://github.com/UB-Mannheim/tesseract/wiki

# import pytesseract
# from PIL import Image

# image = Image.open(pdf_path)

# text = pytesseract.image_to_string(image)

# print(text)


# "PREFEITURA MUNICIPAL DE BARUERI BARVERI SECRETARIA FinANCAS NoTL FigAleletRonic e seruicos NoiafiscaleleTRoNICA dDE aaiua SFrveusefailiA Aaltcnlkidaje dla Nola Fiscal Elcvunka SqMc1 ACu Crnilia a Toina erublur = danen OarenaiGoendereco: U1rsa lizlauutuan PoA bnnlu> 156W.1110.8579.9960699-V r rarai s Jyc Gestao RiscosLtda Avenida tavbore W7ib cocanorus Alfhaville Sele Sel4 sitio Tanpore(uBRAN Cer 05160-DoJ Berueri Cypc Uoelbuouaheii Irsctifad Munic Oal Vekae riaione GoudencarcoTranspoRTes Logisticavtda 00.163.083'D001 30 Estrada dos Wfes Ander 06ez3-Uau RFVAL rarvfri Ctaaonc anispnenodsnensa {ssa5 ErvoNTTs 4ns374p 3730 [0 Discriminacaodos Servicos InhokmalofkkifVanufe PRESIACRO Sekvicoshelaiivos Fixodezekuko 2023 foulad ran as P4a15 726an ? VEniMenid 2102zC2 DFirnniomlrfaeni (hairano bula Wlaaari Saalar c boloocoye € Mai palj codoncytciciosmicoesljddenscos CoM.D Jalore repacee Terceiros Rs 0,00 ndenco Aaqverie VALOR TOTAL DA NOTA 9.200,00 r l o Dlea Isdau Celly Ouea Alo4 ELle 74ee nbeaihuhvln 156W,1110.8579.9960699-V Henlean {lild receberos empresa JSC gestao RiscosLIoA seryicos ConstanTES DeSTA Cenonnanesl anffatr  NoTA fiscaleletronica De Senvicos Oua (ron 
# "
# "PREFEITURA MUNICIPAL DE BARUERI BARVERI SECRETARIA FinANCAS NoTL FigAleletRonic e seruicos aafer NoiafiscaleleTRoNICA dDE aaiua SFrveusefailiA Aaltcnlkidaje dla Nola Fiscal Elcvunka SqMc1 ACu Crnilia a Toina erublur = danen OarenaiGoendereco: U1ae lizlauutuan PoA bnnlu> 1155.9721.3237.8501199-U [eoviru s Jyc Gestao RiscosLtda Avenida tavbore W7ib cocanorus Alfhaville Sele Sel4 sitio Tanpore(uBRAN Cer 05160-DoJ BARUERI - Sp 14ee Uoelbuouaheii Irsctifad Munic Oal Vekae riaione Merck sharp acid DohmF farhacfuticalIDa 03.560.9720001-16 Avdjutorcfosrizfidan 225 eaaaUlu Cordaro saopaulc 1Crl2+s540ls5a Ctaanor anispnenodrnen 3oa ErvoNTTs oulad Qor as Paoi3-8s95069 1a YENIMENIO 01zc24 Nanupari JfFUa Baarescoag;1387cC 108o1,3 Jalore repacee Terceiros Rs 0,0o ndenco auoed VALOR TOTAL DA NOTA 28.112,79 r l 7otteo olt 137/94085 Ouea G-qjanue A4 ELle 74ee nbeaihuhvln 1155,9721,3237.8501199-U Henlean {lild receberos empresa JSC gestao RiscosLIDA seryicos ConstanTES deStA Cenonnanesl anffatr  NoTA fiscaleletronica De Senvicos 7147
# "
# "PREFEITURA MUNICIPAL DE BARUERI BARVERI SECRETARIA FinANCAS NoTL FigAleletRonic e seruicos aafer NoiafiscaleleTRoNICA dDE aaiua SFrveusefailiA Aaltcnlkidaje dla Nola Fiscal Elcvunka SqMc1 ACu Crnilia a Toina erublur = danen OarenaiGoendereco: U1e lizlauutuan PoA bnnlu> 574T.8487.7393.5811199-T i s Jyc Gestao RiscosLtda Avenida tavbore W7ib cocanorus Alfhaville Sele Sel4 sitio Tanpore(uBRAN Cer 05160-DoJ BARUERI - Sp 14ee Uoelbuouaheii Irsctifad Munic Oal Vekae riaione Fcoportosantos 02.390.235 0001 15 4vengeNheirc antonio Alvesfrere sN 11010-730 SAbo sato5 onto anispnenodrnen 3oa ErvoNTTs 4ns374p 1445003 onm Discriminacaodos Servicos InhokmalofkkifVanufe PRESIACRO Sekvicoshelaiivos FIXD JanEIRC-2024 foulad a ra as P4a15 1290011 VEniMenid 01o2zC24 Firnniomlr fA Fhairno Lula Wlaaari analaro boloocoye € Mai palj codoncytciciosmicoesljddenscos CoM.D Jalore repacee Terceiros Rs 0,00 ndenco Santos VALOR TOTAL DA NOTA 14 459 90 r l 7otteo dian OLOL Ouea AA4 ELle 4ee nbeaihuhvln 5741.8487.7393,5811199-T Henlean {lild receberos empresa JSC gestao RiscosLIoA seryicos ConstanTES DeSTA Rennonnnel anffatr  NoTA fiscaleletronica De Senvicos 7179"