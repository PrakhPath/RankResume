import pypdf
import os
import docx2txt

from config import config


class ResumeFiles:
    def __init__(self, resume_path):
        self.resume_dict = {}
        self.resume_list = os.listdir(resume_path)
        self.resume_list = [os.path.join(resume_path, resume) for resume in self.resume_list]
        print("Total Resumes submitted: ", len(self.resume_list))

        self.resume_list, self.discarded_res = self._discard_large_files(self.resume_list)
        print("Total Resumes under consideration: ", len(self.resume_list))

        self.resume_list_docx = [resume for resume in self.resume_list
                                 if os.path.basename(resume).split('.')[1] == 'docx']
        self.resume_list_pdf = [resume for resume in self.resume_list
                                if os.path.basename(resume).split('.')[1] == 'pdf']

    def _discard_large_files(self, file_list):
        discarded_files = []
        for file_name in file_list[:]:
            file_size = os.path.getsize(file_name)
            if file_size > 1000000:
                discarded_files.append(file_name)
                file_list.remove(file_name)

        return file_list, discarded_files

    def _read_resume_pdf(self):
        for resume in self.resume_list_pdf:
            pdf_reader = pypdf.PdfReader(resume)
            pdf_pages = pdf_reader.pages
            pdf_text = ''
            for page in pdf_pages:
                pdf_text = pdf_text + page.extract_text()
            self.resume_dict[os.path.basename(resume)] = pdf_text

    def _read_resume_docx(self):
        for resume in self.resume_list_docx:
            docx_text = docx2txt.process(resume)
            self.resume_dict[os.path.basename(resume)] = docx_text

    def resumes_to_dict(self) -> dict:
        self._read_resume_pdf()
        self._read_resume_docx()

        return self.resume_dict
