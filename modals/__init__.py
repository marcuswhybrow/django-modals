from django.template.loader import render_to_string
from django.forms.models import ModelForm
from django.shortcuts import get_object_or_404

class Modal(object):
    form_class = None
    template_name = 'modals/modal.html'
    pk_fields = []
    queryset = None

    def __init__(self, queryset=None):
        self.queryset = queryset

    @property
    def hash(self):
        """A unique name to represent this type of modal"""
        return hashlib.sha224(self.__class__.__name__).hexdigest()

    # Overridable methods

    def valid(self, form):
        """Called if data is submitted to the form, and it is valid"""
        form.save()

    def invalid(self, form):
        """Called if data is submitted to the form, and it is invalid"""
        pass

    # Private methods

    def __str__(self):
        """Allows {{ modal }} to be use in template to output HTML"""
        return self._html_output()

    def _get_form_class(self):
        """Get the form_class attribute or throw error if None"""
        if self.form_class is None:
            raise ImproperlyConfigured('from_class attribute must be set')
        return self.form_class

    def _get_form(self, data, *args, **kwargs):
        """Get this modal's form, supplied with POST/GET data"""
        # Try and get a modal instance that this modal is editing
        if 'instance' not in kwargs:
            kwargs['instance'] = self._get_instance(data)
        return self._get_form_class()(data, *args, **kwargs)

    def _get_template_name(self):
        """Get the name of the template to use, or throw error if None"""
        if self.template_name is None:
            raise ImproperlyConfigured('template_name attribute must be set')
        return self.template_name

    def _html_output(self):
        """Use template to render modal to HTML"""
        return self.render_to_string(self._get_template_name(), {
            'modal': self,
        })

    def _get_identifier(self, data):
        """Get modal instance identifier from POST/GET data"""
        for field in pk_fields + ['id', 'pk']:
            if field in data:
                return field, data[field]
        return None, None

    def _get_instance(self, data):
        """Return the instance this modal is editing, or None"""
        queryset = self._get_queryset()
        if queryset is not None:
            field_name, value = _get_identifier(data)
            if value is None:
                return None
            else:
                fields = {}
                fields[field_name] = value
                try:
                    return self.queryset.get(**fields)
                except:
                    return None

    def _get_queryset(self):
        """Get the queryset this modal can access, or None"""
        form_class = self._get_form_class()
        if issubclass(form_class, ModelForm):
            if self.queryset is not None:
                return self.queryset
            else:
                return form_class.model.objects.all()


class ModalMixin(object):
    """
    Expects:
      * django.views.generic.base.TemplateResponseMixin

    """
    modals_context_name = 'modals'

    def post(self, request, *args, **kwargs):
        """Handles valid and invalid modal submissions"""
        for modal in modals:
            # Expects modal hash as form submit button name
            if modal._get_modal_hash() in request.POST:
                form = modal._get_form(request, *args, **kwargs)
                if form.is_valid():
                    modal.valid(form)
                else:
                    modal.invalid(form)
        return super(ModalMixin, self).post(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        """Adds modals to the template context"""
        context = super(ModalMixin, self).get_context_data(*args, **kwargs)
        context[self.modals_context_name] = self.modals
        return context

    def get_modals(self):
        """Return an iterable of Modal instances for inclusion in context"""
        raise ImproperlyConfigured('get_modals must be overriden') 


