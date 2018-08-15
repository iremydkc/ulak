import argparse
import logging
import smtplib
import getpass


class SendMail:

    server = None
    username = None
    password = None
    to = None
    email_text = None
    subject = None
    messageText = None

    def __init__(self):

        self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        self.server.ehlo()

    def get_arguments_from_user(self):
        parser = argparse.ArgumentParser()

        parser.add_argument("--sender", help="email address you want to send mail on")
        parser.add_argument("--receiver", help="email address which get your mail")
        parser.add_argument("--file", help="txt file path for your mail message")

        arguments = parser.parse_args()
        self.messageText = arguments.file
        self.username = arguments.sender
        self.password = getpass.getpass("Enter the password for sender: ")
        self.to = arguments.receiver
        self.subject = "Sending email with python !!!"

    def get_text_from_user(self):

        file = open(self.messageText, "r")
        body = file.read()
        self.email_text = """
                From: %s
                To: %s
                Subject: %s
                Body: %s
                """ % (self.username, self.to, self.subject, body)

    def send_mail(self):

        try:
            self.server.login(self.username, self.password)
            self.server.sendmail(self.username, self.to, self.email_text)
            print("email sent!!!")
        except smtplib.SMTPAuthenticationError as e:
            logging.error("Login operation has failed!")
        except smtplib.SMTPException as e:
            logging.error("mail server has failed!")
        finally:
            self.server.close()


if __name__ == '__main__':

    mail_sender = SendMail()
    mail_sender.get_arguments_from_user()
    mail_sender.get_text_from_user()
    mail_sender.send_mail()
