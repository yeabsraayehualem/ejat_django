from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SpiritualTitle(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class SecularTitle(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title



    



class AccountManager(BaseUserManager):
    def create_user(self,phone,password=None,**ef):
        if not phone:
            raise ValueError("Phone Number is required")
        
        user = self.model(phone=phone,**ef)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,phone,password=None,**ef):
        ef.setdefault('is_staff',True)
        ef.setdefault('is_superuser',True)
        
        return self.create_user(phone,password,**ef)
    


class Account(AbstractBaseUser,PermissionsMixin):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20,unique=True)
    name_of_baptism = models.CharField(max_length=50)
    spiritual_title = models.ForeignKey(SpiritualTitle,on_delete=models.SET_NULL,null=True,  blank=True)
    secular_title = models.ForeignKey(SecularTitle,on_delete=models.SET_NULL,null=True,blank=True  )
    department = models.ForeignKey(Department,on_delete=models.SET_NULL,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_staff  = models.BooleanField(default=False)
    
    
    objects  = AccountManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']
    
    def __str__(self):
        parts = []
        
        
        if self.spiritual_title:
            parts.append(self.spiritual_title.title)
        
        if self.secular_title:
            parts.append(self.secular_title.title)
        
        parts.append(self.name)
        
        return " ".join(parts)
