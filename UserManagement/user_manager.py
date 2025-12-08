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
    
    def create_superuser(self, username, email, password=None):
        if not email:
            raise ValueError('Superuser must have an email')
        if not password:
            raise ValueError('Superuser must have a password')

        user = self.create_user(username=username, email=email, password=password)

        # Set common admin flags only if they exist on the model
        for flag in ("is_staff", "is_superuser", "is_admin", "is_active", "is_verified"):
            if hasattr(user, flag):
                setattr(user, flag, True)

        user.save(using=self._db)
        return user 