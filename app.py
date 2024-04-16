from pack.pre_processor import PreProcessor
from pack import vctr_cosine_sim
from utils.resume_files import ResumeFiles

import pypdf

jd_pdf = r"C:\Users\prakhar.pathrikar\PycharmProjects\projects\rank_resume\data\job_descriptions\fake.pdf"
resume_path = r'C:\Users\prakhar.pathrikar\PycharmProjects\projects\rank_resume\data\resumes'

# Read JD pdf
pdf_reader = pypdf.PdfReader(jd_pdf)
pdf_pages = pdf_reader.pages
jd_text = ''
for page in pdf_pages:
    jd_text = jd_text + page.extract_text()

# Read all resumes in a dictionary
resume_files = ResumeFiles(resume_path)
resume_dict = resume_files.resumes_to_dict()

# Pre-process texts
pre_processor = PreProcessor()

jd_pre_process = pre_processor.pre_process(jd_text)

for key, value in resume_dict.items():
    resume_dict[key] = pre_processor.pre_process(value)

match_dict = {}

for key, value in resume_dict.items():
    match_dict[key] = vctr_cosine_sim.smlrty_prcnt(jd_pre_process, value)

match_dict = sorted(match_dict.items(), key= lambda x:x[1], reverse=True)

print(match_dict)
