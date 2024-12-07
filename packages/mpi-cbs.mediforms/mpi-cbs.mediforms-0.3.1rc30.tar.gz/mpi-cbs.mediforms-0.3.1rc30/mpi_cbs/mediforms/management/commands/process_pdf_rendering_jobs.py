from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils import translation

from weasyprint import HTML

from mpi_cbs.mediforms import models
from mpi_cbs.mediforms.forms import (MRTForm, MRTBegleitungForm, PersonalDataForm,
                                     QuestionsMRTForm, QuestionsTMSForm,
                                     QuestionsWomenForm, QuestionsWomenMRTForm,
                                     TMSForm)


class Command(BaseCommand):
    help = 'help text'

    def handle(self, *args, **options):
        for job in models.PDFRenderingJob.objects.all():
            self.process_rendering_job(job)

    def process_rendering_job(self, job):
        self.method = job.method
        self.form_data = job.form_data
        self.language = job.language

        pdf_file = self.create_pdf_file()
        self.send_mail(pdf_file)

        job.delete()

    def create_pdf_file(self):
        rendered_html = self.render_template()
        rendered_pdf = HTML(string=rendered_html).write_pdf()
        return self.persist_pdf_file(rendered_pdf)

    def render_template(self):
        questions_form_class, questions_women_form_class = self.get_questions_form_classes()

        with translation.override(self.language):
            return render_to_string(f'mediforms/pdfs/{self.method.key}.html', {
                'method': self.method,
                'form': self.get_form_class(),
                'form_data': self.form_data,
                'personal_data_form': PersonalDataForm(instance=self.form_data),
                'questions_form': questions_form_class(instance=self.form_data),
                'questions_form_women': questions_women_form_class(instance=self.form_data),
            })

    def get_questions_form_classes(self):
        if isinstance(self.form_data, (models.FormDataMRT, models.FormDataMRTBegleitung)):
            return QuestionsMRTForm, QuestionsWomenMRTForm
        elif isinstance(self.form_data, models.FormDataTMS):
            return QuestionsTMSForm, QuestionsWomenForm

    def get_form_class(self):
        if isinstance(self.form_data, models.FormDataMRT):
            return MRTForm
        elif isinstance(self.form_data, models.FormDataMRTBegleitung):
            return MRTBegleitungForm
        elif isinstance(self.form_data, models.FormDataTMS):
            return TMSForm

    def persist_pdf_file(self, rendered_pdf):
        filename = '_'.join([
            'consent',
            self.method.key,
            models.sanitize_string(self.form_data.last_name),
            models.sanitize_string(self.form_data.first_name),
            # self.form_data.date_of_birth.strftime("%Y%m%d")
        ]) + '.pdf'
        file_handle = SimpleUploadedFile(name=filename, content=rendered_pdf,
                                         content_type='application/pdf')

        return self.get_pdf_model().objects.create(form_data=self.form_data,
                                                   file_handle=file_handle)

    def get_pdf_model(self):
        if isinstance(self.form_data, models.FormDataMRT):
            return models.PDFMRT
        elif isinstance(self.form_data, models.FormDataMRTBegleitung):
            return models.PDFMRTBegleitung
        elif isinstance(self.form_data, models.FormDataTMS):
            return models.PDFTMS

    def send_mail(self, pdf_file):
        email_text = render_to_string(f'mediforms/emails/{self.method.key}.txt', {
            'first_name': self.form_data.first_name,
            'last_name': self.form_data.last_name,
            'method': self.method,
            'host': 'https://mediforms.cbs.mpg.de',
        })

        email = EmailMessage(
            subject=settings.MEDIFORMS_EMAIL_SUBJECT,
            body=email_text,
            from_email=settings.MEDIFORMS_EMAIL_FROM,
            bcc=settings.MEDIFORMS_EMAIL_RECIPIENTS_LIST_BCC,
            reply_to=settings.MEDIFORMS_EMAIL_RECIPIENTS_LIST_REPLY_TO,
        )

        if self.form_data.email:
            email.to = [self.form_data.email]
            email.send()

        email.to = settings.MEDIFORMS_EMAIL_RECIPIENTS_LIST_TO
        email.attach_file(pdf_file.file_handle.path)
        email.send()
