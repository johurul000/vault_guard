from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, username, email=None, password = None, **extra_fields):

        user = self.model(username = username, email = email, **extra_fields)
        user.set_password(password)
        user.save(using = self.db)

        return user
    

    def create_superuser(self, username, password = None, **extra_fields):

        extra_fields.setdefault('is_staff' , True)
        extra_fields.setdefault('is_superuser' , True)
        extra_fields.setdefault('is_active' , True)

        return self.create_user(username= username, password=password, **extra_fields)