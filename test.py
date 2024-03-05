from pyresparser import ResumeParser

data = ResumeParser("Aman resume for y2.pdf").get_extracted_data()

print(data)