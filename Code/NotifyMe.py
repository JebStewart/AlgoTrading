import smtplib
import ssl


class Notifier:
    def __init__(self):
        self.un = 'Wintrmute22@gmail.com'
        self.pw = 'Indistinguishablefrommagic'
        self.receiver_email = 'jebstewart22@gmail.com'
        self.port = 465
        self.context = ssl.create_default_context()
    
    def notify(self, noti):
        with smtplib.SMTP_SSL('smtp.gmail.com', self.port, context=self.context) as server:
            server.login(self.un, self.pw)
            server.sendmail(self.un, self.receiver_email, noti)


if __name__ == '__main__':
    n = Notifier()
    n.notify('Test, please disregard')
