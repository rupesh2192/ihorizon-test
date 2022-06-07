from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView

from authentication.models import UserTypeChoices
from supportdesk.forms import CreateRequestForm
from supportdesk.mixins import RoleRequiredMixin
from supportdesk.models import Request


class CustomerRequests(LoginRequiredMixin, RoleRequiredMixin, TemplateView):
    template_name = "supportdesk/customer_requests.html"
    user_type = UserTypeChoices.CUSTOMER.value

    def get_context_data(self, **kwargs):
        requests = Request.objects.filter(created_by=self.request.user)
        return {"requests": requests, "request_count": requests.count()}


class CustomerCreateTicket(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    template_name = "supportdesk/create_ticket.html"
    success_url = reverse_lazy("supportdesk_customer_requests")
    form_class = CreateRequestForm
    login_url = reverse_lazy('login')
    user_type = UserTypeChoices.CUSTOMER.value

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        temp = super(CustomerCreateTicket, self).form_valid(form)
        self.object.random_reassign()
        return temp

    def get_context_data(self, **kwargs):
        context = super(CustomerCreateTicket, self).get_context_data(**kwargs)
        context["request_count"] = Request.objects.filter(created_by=self.request.user).count()
        return context


class AgentRequests(LoginRequiredMixin, RoleRequiredMixin, TemplateView):
    template_name = "supportdesk/agent_requests.html"
    user_type = UserTypeChoices.AGENT.value

    def get_context_data(self, **kwargs):
        requests = Request.objects.filter(assigned_to=self.request.user)
        return {"requests": requests}


class AgentViewRequest(LoginRequiredMixin, RoleRequiredMixin, DetailView, UpdateView):
    template_name = "supportdesk/view_request.html"
    success_url = reverse_lazy("supportdesk_agent_requests")
    login_url = reverse_lazy('login')
    fields = ["status"]
    user_type = UserTypeChoices.AGENT.value

    def get_queryset(self):
        return Request.objects.filter(assigned_to=self.request.user)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.mark_as_completed()
        return HttpResponseRedirect(self.get_success_url())


class AgentReAssignRequest(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    success_url = reverse_lazy("supportdesk_agent_requests")
    login_url = reverse_lazy('login')
    user_type = UserTypeChoices.AGENT.value
    fields = ["assigned_to"]

    def get_queryset(self):
        return Request.objects.filter(assigned_to=self.request.user)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.random_reassign()
        return HttpResponseRedirect(self.get_success_url())
