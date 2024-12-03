from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    industry = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    position = models.CharField(max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="contacts")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Opportunity(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('won', 'Won'),
        ('lost', 'Lost'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    estimated_value = models.DecimalField(max_digits=10, decimal_places=2)
    creation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="opportunities")

    def __str__(self):
        return self.title

class Interaction(models.Model):
    date = models.DateField()
    summary = models.TextField()
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name="interactions")

    def __str__(self):
        return f"Interaction on {self.date} for {self.opportunity.title}"
