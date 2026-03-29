from django.db import models
from users.models import Account
# Create your models here.
class Attendance(models.Model):
    
    
    name = models.ForeignKey(Account,on_delete=models.CASCADE,null=False,blank=False)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(choices=[('p','Present'),('a',"Absent")])
    
    def __str__(self):
        parts = []
        
        if self.name.spiritual_title:
            parts.append(self.name.spiritual_title.title)
        if self.name.secular_title:
            parts.append(self.name.secular_title.title)
        parts.append(self.name.name)
        return f"{' '.join(parts)} - {self.date.strftime('%d-%m-%Y')} - {self.status}"    