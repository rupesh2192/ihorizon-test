from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from authentication.models import UserTypeChoices

User = get_user_model()


class RequestStatusChoices(models.TextChoices):
    IN_PROGRESS = 'in-progress', _('In Progress')
    COMPLETED = 'completed', _('Completed')


class RequestPriorityChoices(models.TextChoices):
    NORMAL = 'normal', _('Normal')
    HIGH = 'high', _('High')


class BaseModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(null=True, default=None)


class Request(BaseModel):
    created_by = models.ForeignKey(User, null=False, related_name="created_requests", on_delete=models.PROTECT,
                                   limit_choices_to={"user_type": UserTypeChoices.CUSTOMER.value})
    assigned_to = models.ForeignKey(User, null=True, related_name="assigned_requests", on_delete=models.PROTECT,
                                    default=None, limit_choices_to={"user_type": UserTypeChoices.AGENT.value})
    summary = models.CharField(null=False, max_length=512)
    description = models.TextField(null=False)
    is_high_priority = models.BooleanField(default=False)
    status = models.SlugField(null=False, max_length=16, choices=RequestStatusChoices.choices,
                              default=RequestStatusChoices.IN_PROGRESS.value)
    completed_on = models.DateTimeField(default=None, null=True, blank=True)

    class Meta:
        ordering = ["-status", "-created_on"]

    def __str__(self):
        return self.summary

    def mark_as_completed(self):
        """
        Update the status of the request to 'completed' and also the completed_on field to current date time.
        """
        self.completed_on = timezone.now()
        self.status = RequestStatusChoices.COMPLETED.value
        self.save(update_fields=['completed_on', 'status'])

    def random_reassign(self):
        """
        Reassign the request to an agent other than currently assigned agent(if any available)
        """
        if not User.objects.filter(user_type=UserTypeChoices.AGENT.value).count() > 1:
            # return if there is only one agent available
            return
        while True:
            agent = User.objects.filter(user_type=UserTypeChoices.AGENT.value).order_by("?")[0]
            if self.assigned_to and agent.id == self.assigned_to.id:
                # Continue if random selected agent is same as current agent
                continue

            self.assigned_to = agent
            self.save()
            break
