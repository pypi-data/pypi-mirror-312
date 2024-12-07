from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import urlencode
from django.views import generic
from django.views.decorators.cache import never_cache

from mpi_cbs.mediforms.forms import (ConsentAgreementForm,
                                     MRTForm, MRTBegleitungForm, PersonalDataForm,
                                     QuestionsMRTForm, QuestionsTMSForm,
                                     QuestionsWomenForm, QuestionsWomenMRTForm,
                                     TMSForm, TokenForm)
from mpi_cbs.mediforms.models import PDFRenderingJob, Token


def get_questions_form_classes(method):
    if method.startswith('mrt'):
        return dict(general=QuestionsMRTForm, women=QuestionsWomenMRTForm)
    elif method == 'tms':
        return dict(general=QuestionsTMSForm, women=QuestionsWomenForm)


class Index(LoginRequiredMixin, generic.FormView):
    form_class = TokenForm
    template_name = 'mediforms/index.html'

    def get_context_data(self):
        context_data = super().get_context_data()
        context_data['method'] = self.request.GET.get('method', '')
        context_data['token'] = self.request.GET.get('token', '')
        return context_data

    def post(self, request, *args, **kwargs):
        token, _created = Token.objects.get_or_create(
            method_id=request.POST.get('method'),
            pseudonym=request.POST.get('pseudonym'),
            defaults=dict(created_by=self.request.user),
        )
        params = urlencode(dict(
            token=token.id,
            method=token.method,
        ))
        return HttpResponseRedirect('{}?{}'.format(reverse('index'), params))


class TokenListView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'tokens'
    model = Token
    template_name = 'mediforms/token_list.html'


@method_decorator(never_cache, name='dispatch')
class FormView(generic.FormView):
    success_url = reverse_lazy('success')

    def dispatch(self, request, *args, **kwargs):
        self.token = get_object_or_404(Token, pk=kwargs.get('token'))
        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):
        return [f'mediforms/pages/form_{self.token.method.key}.html']

    def get_context_data(self, **kwargs):
        questions_form_classes = get_questions_form_classes(self.token.method.key)

        context = super().get_context_data(**kwargs)
        context['method'] = self.token.method
        form_data = None if self.request.method == 'GET' else self.request.POST
        context['personal_data_form'] = PersonalDataForm(form_data)
        context['questions_form'] = questions_form_classes['general'](form_data, initial={'mrtanzahl': 0})
        context['questions_form_women'] = questions_form_classes['women'](form_data)
        context['consent_agreement_form'] = ConsentAgreementForm()

        return context

    def get_form_class(self):
        method = self.token.method.key
        if method == 'mrt':
            return MRTForm
        elif method == 'mrtbegleitung':
            return MRTBegleitungForm
        elif method == 'tms':
            return TMSForm

    def form_valid(self, form):
        form_data = form.save(commit=False)
        form_data.pseudonym = self.token.pseudonym
        form_data.token_created_by = self.token.created_by
        form_data.save()

        PDFRenderingJob.objects.create(
            method=self.token.method,
            form_data=form_data,
            language=self.request.LANGUAGE_CODE,
        )

        self.token.delete()

        return super().form_valid(form)


class DataStorageConsentView(generic.TemplateView):
    template_name = 'mediforms/pages/data_storage_consent.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        method = self.kwargs.get('method')
        if method.startswith('mrt'):
            context['method'] = 'MRT'
        elif method == 'tms':
            context['method'] = 'TMS/tDCS'
        return context
