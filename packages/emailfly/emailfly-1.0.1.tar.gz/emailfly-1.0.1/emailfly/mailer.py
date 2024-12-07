"""
mailer.py
module path (mailer.mailify.mailer)

Mailer is a configurable module that handles the mailing functionalities across the app
"""

import re
import os
import email
import smtplib
import imaplib
from PIL import Image
from threading import Timer
from bs4 import BeautifulSoup
from typing import Dict, List
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from os.path import basename, splitext
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from .utils.utils import validate_path, get_files_from_dir


class Emailer:
    def __init__(self, 
                 sender_email: str,
                 password: str,
                 sender_name: str,
                 port: str,
                 smtp_server: str) -> None:
        """Initialises the mailer object

        Args:
            sender_email (str): Sender Email
            password (str): Sender Password
            sender_name (str): Sender Name
            port (str): SMTP Port 
            smtp_server (str): SMTP Server
        """
        self.sender_email = sender_email
        self.password = password
        self.sender_name = sender_name
        self.port = port
        self.smtp_server = smtp_server

    def load_html(self,
                  message: MIMEMultipart, 
                  template: str, 
                  data: Dict = {}) -> MIMEMultipart:
        """Loads the HTML Content along with the dynamic values

        Args:
            message (MIMEMultipart): Mail MIME Object
            template (str): HTML Template Path
            data (Dict, optional): Dynamic Context to send in HTML. Defaults to {}.

        Returns:
            MIMEMultipart: Mail MIME Object
        """

        # Loads the HTML Content
        template = validate_path(template)
        template_files = get_files_from_dir(f"{template}")
        html_file = [each for each in template_files if each.suffix == ".html"][0]

        image_directory = 'templates/sample/images/'
        if os.path.exists(image_directory):
            for file in os.listdir(image_directory):
                os.remove(f'{image_directory}{file}')
        else:
            os.makedirs(image_directory)

        with open(html_file, "r") as email_template:
            html = email_template.read()

            html = BeautifulSoup(html, 'html.parser')
            for img in html.findAll('img'):
                img1 = Image.open(img["src"])
                name, extension = splitext(basename(img["src"]))

                if not os.path.exists(image_directory):
                    os.makedirs(image_directory)

                img1.save(f"{image_directory}{name}{extension}")
                img['src'] = f'cid:{name}{extension}'

            for style in html.findAll('style'):
                if style.string:
                    updated_styles = []
                    lines = style.string.split(';')
                    background_image_regex = re.compile(r"background-image:\s*url\(['\"]?(.*?)['\"]?\)")

                    for line in lines:
                        if 'background-image' in line:
                            matches = background_image_regex.findall(line)
                            if matches:
                                image2 = Image.open(matches[0])
                                name, extension = splitext(basename(matches[0]))

                                if not os.path.exists(image_directory):
                                    os.makedirs(image_directory)

                                image2.save(f"{image_directory}{name}{extension}")
                                updated_styles.append(f"background-image: url({f'cid:{name}{extension}'})")
                            else:
                                updated_styles.append(line.strip())
                        else:
                            updated_styles.append(line.strip())

                    style.string = '; '.join(updated_styles)

            html = str(html)
            for key, value in data.items():
                html = html.replace(key, value)
            
        message.attach(MIMEText(html, "html"))

        # Loads the Images
        images = get_files_from_dir(f"{template}/images")
        for image in images:
            with open(f"{image}",'rb') as file:
                attached_image = MIMEImage(file.read(), 'png')
                attached_image.add_header('Content-ID', image.name)
                # attached_image.add_header('Content-Disposition', 'inline', filename=image.name)
                message.attach(attached_image)

        return message

    def attach_files(self, 
                     message: MIMEMultipart, 
                     template: str) -> MIMEMultipart:
        """Attach the files in the email

        Args:
            message (MIMEMultipart): Mail MIME Object
            template (str): HTML Template Path

        Returns:
            MIMEMultipart: Updated MIME Object
        """
        attachments = get_files_from_dir(f"{template}/attachments")
        
        for attachment in attachments:
            with open(f"{attachment}",'rb') as file:
                message.attach(MIMEApplication(file.read(), Name=attachment.name))
        
        return message
    
    def normalize_email_input(self, email_input):
        """
        Normalize the given email input into a list of valid email addresses.

        This function accepts a single email address or a list of email addresses.
        It returns a list containing only the email addresses that are valid according
        to the internal validation method.

        Args:
            email_input (str or list): An email address or a list of email addresses to normalize.

        Returns:
            list: A list of valid email addresses.
        """
        if not email_input:
            return []
        
        if isinstance(email_input, str):
            email_input = [email_input]
        
        return [email for email in email_input if self.validate_email(email)]

    def validate_email(self, email_address):
        """
        Validate email address format.

        :param email_address: Email address to validate
        :return: Boolean indicating validity
        """
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email_address) is not None

    def send_email(self, 
                   subject: str, 
                   html_template: str, 
                   recipients: List[str],
                   data: Dict = {},
                   cc_email=None, 
                   bcc_email=None) -> bool:
        
        """
        Send an email with HTML content and optional attachments.

        Args:
            subject (str): The subject of the email.
            html_template (str): Path to the HTML template for the email body.
            recipients (List[str]): List of recipient email addresses.
            data (Dict, optional): Data dictionary to render within the HTML template.
            cc_email (optional): List of CC recipient email addresses.
            bcc_email (optional): List of BCC recipient email addresses.

        Returns:
            bool: True if the email is sent successfully, otherwise raises an exception.

        Raises:
            Exception: If an error occurs during sending.
        """
        try:

            recipients = self.normalize_email_input(recipients)
            cc_email = self.normalize_email_input(cc_email)

            bcc_email = self.normalize_email_input(bcc_email)

            message = MIMEMultipart()
            message["Subject"] = subject
            message['From'] = self.sender_name
            message['To'] = ", ".join(recipients)

            if cc_email:
                print("CC", cc_email)
                message['Cc'] = ', '.join(cc_email)
            if bcc_email:
                message['Bcc'] = ', '.join(bcc_email)

            # Attach the HTML part
            message = self.load_html(message, html_template, data)

            # Include Attachments
            message = self.attach_files(message, html_template)


            all_recipients = recipients + (cc_email if cc_email else []) + (bcc_email if bcc_email else [])

            # Send the email
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls()
                server.login(self.sender_email, self.password)
                server.sendmail(self.sender_email, all_recipients, message.as_string())

            return True
        
        except Exception as e:
            raise Exception(e)


    def schedule_email(self, 
                       subject: str, 
                       html_template: str, 
                       recipients: List[str],
                       data: Dict = {},
                       cc_email=None, 
                       bcc_email=None,
                       delay_seconds=None):
        """
        Schedules an email for future sending.

        :param subject: Email subject
        :param html_template: Email HTML template
        :param recipients: List of recipient email addresses
        :param data: Data to be rendered in the HTML template
        :param cc_email: List of CC email addresses
        :param bcc_email: List of BCC email addresses
        :param delay_seconds: Number of seconds to delay the email by
        :return: Whether the email was scheduled successfully
        """
        try:
            timer = Timer(delay_seconds, self.send_email, [subject, html_template, recipients, data, cc_email, bcc_email])
            timer.start()

            return True

        except Exception as e:
            return False
        
    def _build_search_criteria(self, filter_criteria):
        """
        Build IMAP search criteria based on filter dictionary.
        
        :param filter_criteria: Dictionary of filtering options
        :return: IMAP search string
        """
        criteria_parts = []
        for key, value in filter_criteria.items():
            if key == 'from':
                criteria_parts.append(f'FROM "{value}"')
            elif key == 'subject':
                criteria_parts.append(f'SUBJECT "{value}"')
            elif key == 'since':
                criteria_parts.append(f'SINCE {value}')
        
        return ' '.join(criteria_parts) if criteria_parts else 'ALL'
    

    def _get_email_body(self, email_message):
        """
        Advanced email body extraction.
        
        :param email_message: Email message object
        :return: Email body as string
        """
        body = ""
        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                if content_type in ['text/plain', 'text/html']:
                    try:
                        body = part.get_payload(decode=True).decode()
                        break
                    except Exception:
                        continue
        else:
            try:
                body = email_message.get_payload(decode=True).decode()
            except Exception:
                body = str(email_message.get_payload())

        return body

    def _get_email_attachments(self, email_message):
        """
        Extract attachments from email.
        
        :param email_message: Email message object
        :return: List of attachment details
        """
        attachments = []
        for part in email_message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename()
            if filename:
                attachments.append({
                    'filename': filename,
                    'content': part.get_payload(decode=True)
                })
        return attachments
    
    def  read_emails(self, 
                 username,
                 password,
                folder='INBOX', 
                limit=4, 
                filter_criteria=None, 
                mark_as_read=False):
        """
        Advanced email reading with filtering and optional read marking.
        
        :param imap_server: IMAP server address
        :param folder: Email folder to read from
        :param limit: Maximum number of emails to retrieve
        :param filter_criteria: Dictionary of filtering criteria
        :param mark_as_read: Whether to mark retrieved emails as read
        :return: List of email details
        """
        try:
            with imaplib.IMAP4_SSL("imap.gmail.com") as mail:
                mail.login(username, password)
                mail.select(folder)

                search_criteria = 'ALL'
                if filter_criteria:
                    search_criteria = self._build_search_criteria(filter_criteria)

                _, search_data = mail.search(None, search_criteria)
                email_ids = search_data[0].split()

                emails = []
                for email_id in email_ids[-limit:]:
                    if mark_as_read:
                        mail.store(email_id, '+FLAGS', '\\Seen')

                    _, msg_data = mail.fetch(email_id, '(RFC822)')
                    raw_email = msg_data[0][1]
                    email_message = email.message_from_bytes(raw_email)

                    email_details = {
                        'from': email_message['From'],
                        'to': email_message['To'],
                        'subject': email_message['Subject'],
                        'date': email_message['Date'],
                        'body': self._get_email_body(email_message),
                        'attachments': self._get_email_attachments(email_message)
                    }
                    emails.append(email_details)

                return emails

        except Exception as e:
            raise Exception(e)
        

