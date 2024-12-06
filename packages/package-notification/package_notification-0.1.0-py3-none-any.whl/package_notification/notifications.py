from django.core.mail import send_mail

def send_status_update_email(receiver_name, tracking_id, receiver_email):
    subject = f"Package Delivered: {tracking_id}"
    message = (
        f"Dear {receiver_name},\n\n"
        f"Your package with Tracking ID {tracking_id} has been delivered.\n"
        f"Thank you for using our service!"
    )
    send_mail(subject, message, 'noreply@logistics.com', [receiver_email])
