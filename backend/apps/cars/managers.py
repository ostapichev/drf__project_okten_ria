from django.db import models


class CarManager(models.Manager):
    def get_cars_by_auto_user_id(self, pk):
        return self.filter(user_id=pk)

    def all_with_cars(self):
        return self.select_related('user')
    