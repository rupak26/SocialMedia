from django.contrib.auth.models import BaseUserManager

class userManager(BaseUserManager):
    
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('User must have an email')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email)  # DON'T use self.create()
        user.set_password(password)  # This hashes the password
        user.save(using=self._db)
        return user
