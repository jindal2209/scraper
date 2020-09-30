# import PyPDF2

# def FindAllRawTextfromPDF(PdfPath):
#     A=''
#     pdf= PyPDF2.PdfFileReader(open(PdfPath, "rb"))
#     for page in pdf.pages:
#         A += page.extractText()
#     # extract all the plain text
#     return A

# path = 'abcd.pdf'
# D1=FindAllRawTextfromPDF(path).split("\n")

# def IndexexofStudentsData(D1):
#     ans=[]
#     for i in range(len(D1)):
#         if(D1[i].find('(SCHEME OF EXAMINATIONS)')>-1):
#             ans.append(i)
#     ans.append(len(D1)-1)
#     return ans
    
# LLforIndexesSD=IndexexofStudentsData(D1)
# print(len(LLforIndexesSD))
# print(LLforIndexesSD)

import tabula

fi = 'abcd.pdf'

tables = tabula.read_pdf(fi)

print(tables)