from django.core.mail import send_mail
import environ

env = environ.Env()
# reading .env file
environ.Env.read_env()


def sendMailToUser(name, send_to):
    subject = "Thanks for contacting us"
    message = "Hello "+name+"! \n\nWe have successfully received your message.\n\nWe will get back to you as soon as possible.\n\nRegards\n- GMS"
    try:
        send_mail(
            subject,
            message,
            env("EMAIL"),
            [send_to],
            fail_silently=False,
        )
    except:
        print("EMAIL NOT SENT")


def sendMailToGMS(name, email, subject, message):
    message = "A new message has been received on our website:\n\nName: "+name + \
        "\nEmail Id: "+email+"\nSubject: "+subject+"\nMessage: "+message+"\n\n\nRegards"
    subject = "A message has been received on Grocery Managamenet System"
    send_mail(
        subject,
        message,
        env("EMAIL"),
        ['bagladivyang03@gmail.com'],
        fail_silently=False,

    )


def OrderDetailtoCustomer(name,send_to,tot_amount,expected_date):
    subject = "Order Placed Succesfully !"
    message = "Hello "+name+"! \n\nWe have successfully received your Order.\n\nWe will get delivered your order by or before "+expected_date+".\nPay "+str(tot_amount)+"₹ at time of delivery.\nRegards\n- GMS"
    try:
        send_mail(
            subject,
            message,
            env("EMAIL"),
            [send_to],
            fail_silently=False,
        )
    except:
        print("EMAIL NOT SENT")
