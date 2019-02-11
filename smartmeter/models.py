from django.conf import settings
from django.db import models
from django.utils import timezone
import hashlib 

"""
Category of plants that are created by users
"""
class Meter(models.Model):
    channel = models.IntegerField()
    description = models.CharField(max_length=200)
    create_record_timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.channel
        
class User(models.Model):
    username = models.CharField(max_length=30)
    raw_password = models.CharField(max_length=30)
    digest_pass = models.CharField(max_length=30)
    last_send_pwd_time = models.DateTimeField(default=timezone.now)
    email = models.CharField(max_length=50)
    
    _get_md5 = lambda self, x: hashlib.md5(x.encode()).hexdigest()
    
    def _change_password(self, old_pass, new_pass):
        if self.digest_pass == self._get_md5(old_pass) or self.digest_pass == "":
            self.raw_password = new_pass
            self.digest_pass = self._get_md5(new_pass)
            self.save()
            return True
        return False
        
    def _change_email(self, pwd, email):
        if self.digest_pass == self._get_md5(pwd) or self.digest_pass == "":
            self.email = email
            self.save()
            return True
        return False
        
    def _validate_password(self, password):
        if self.digest_pass == self._get_md5(password) or self.digest_pass == "":
            return True
        return False