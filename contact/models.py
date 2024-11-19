from django.db import models

class ContactForm(models.Model):
    TITLE_CHOICES = [
        ('Mr', 'Mr'),
        ('Miss', 'Miss'),
        ('Mrs', 'Mrs'),
        ('Ms', 'Ms'),
        ('Dr', 'Dr'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=10, choices=TITLE_CHOICES, default='Mr')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)  # Phone field
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} from {self.name}"


class FAQs(models.Model):
    question = models.CharField(max_length=300)
    answer = models.TextField()

    def __str__(self):
        return self.question
