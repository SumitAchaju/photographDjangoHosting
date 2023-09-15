from django.db import models
from Account.models import User
from PIL import Image
from datetime import datetime,timedelta

message_type = (("text", "text"), ("image", "image"))
message_status = (("sent", "sent"), ("delivered", "delivered"), ("seen", "seen"))


class Message(models.Model):
    message_type = models.CharField(
        max_length=10, choices=message_type, default=message_type[0][0]
    )
    message_text = models.TextField(blank=True, null=True)
    message_img = models.ImageField(upload_to="MessageImage", blank=True, null=True)
    send_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receive_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver"
    )
    send_date = models.DateTimeField(default=datetime.now)
    msg_status = models.CharField(
        max_length=20, choices=message_status, default=message_status[0][0]
    )

    @property
    def formated_date(self):
        msg_date = self.send_date.strftime("%Y-%m-%d %H:%M").split(" ")
        msg_day = msg_date[0]
        msg_time = msg_date[1]

        today = datetime.today().date()
        one_week_ago = today - timedelta(days=7)
        one_year_ago = today - timedelta(days=365)

        date = datetime.strptime(msg_day, '%Y-%m-%d').date()

        # Convert the string to a datetime object
        time_obj = datetime.strptime(msg_time, '%H:%M')
        # Get the 12-hour formatted time with AM/PM
        formatted_time = time_obj.strftime('%I:%M %p').lower()
        if date == today:
            return formatted_time
        elif one_week_ago < date < today:
            weekday = date.strftime("%A")[0:3]
            return f'{weekday} {formatted_time}'
        elif one_year_ago < date <= one_week_ago:
            return date.strftime('%B %d')
        else:
            return date

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.message_img:
            img = Image.open(self.message_img.path)
            if img.width >= 900 or img.height >= 900:
                output_size = (900, 900)
                img.thumbnail(output_size, Image.LANCZOS)
                img.save(self.message_img.path)
            else:
                output_size = (img.width, img.height)
                img.thumbnail(output_size, Image.LANCZOS)
                img.save(self.message_img.path)

    def __str__(self):
        if self.message_type == message_type[0][0]:
            return self.message_text
        if self.message_type == message_type[1][0]:
            return self.message_img.path
