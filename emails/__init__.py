from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from os import environ
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from_email = environ['SENDGRID_FROM_EMAIL']
send_grid_key = environ['SEDNGRID_API_KEY']
print(from_email, send_grid_key)

def send_template_email(template, to, subj, **kwargs):
    """Sends an email using a template."""
    env = Environment(
        loader=FileSystemLoader('emails/templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template(template)
    send_email(to, subj, template.render(**kwargs))

def send_email(to, subj, body):
    message = Mail(
        from_email=from_email,
        to_emails=to,
        subject=subj,
        html_content=body
        )
    try:
        sg = SendGridAPIClient(send_grid_key)
        response = sg.send(message)
    except Exception as e:
        print(e)
