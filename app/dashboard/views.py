from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView

from .forms import UploadJSONForm
from .models import Record
from .services import process_json_file


class UploadJSONView(FormView):
    template_name = "dashboard/upload.html"
    form_class = UploadJSONForm
    success_url = reverse_lazy("dashboard:list")

    def form_valid(self, form):
        file = form.cleaned_data["file"]

        is_success, message = process_json_file(file)

        if is_success:
            messages.success(self.request, message)
            return super().form_valid(form)
        else:
            messages.error(self.request, message)
            return self.form_invalid(form)


class RecordListView(ListView):
    model = Record
    template_name = "dashboard/list.html"
    context_object_name = "records"
