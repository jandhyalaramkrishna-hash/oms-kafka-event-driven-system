from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables
load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))

def send_email(subject, body, to_email):
    try:
        # Create a multipart message container to allow HTML styling
        msg = MIMEMultipart("alternative")
        msg['Subject'] = f"🚨 SYSTEM ALERT: {subject}"
        msg['From'] = EMAIL_USER
        msg['To'] = to_email

        # Professional HTML template for your Gmail inbox alert
        html_content = f"""
        <html>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #333; line-height: 1.6; margin: 0; padding: 20px; background-color: #f9f9f9;">
            <div style="max-width: 600px; margin: 0 auto; background: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                
                <div style="background-color: #d9534f; padding: 20px; text-align: center; color: #ffffff;">
                    <h2 style="margin: 0; font-size: 22px; font-weight: 600; letter-spacing: 0.5px;">ORDER PIPELINE FAILURE</h2>
                </div>
                
                <div style="padding: 25px;">
                    <p style="font-size: 16px; margin-top: 0;">Hello Administrator,</p>
                    <p style="font-size: 15px; color: #555;">An automated validation threshold was breached. A transaction payload has failed processing limits and has been successfully routed to the <strong>Dead Letter Queue (DLQ)</strong> for isolation.</p>
                    
                    <hr style="border: 0; border-top: 1px solid #eeeeee; margin: 20px 0;" />
                    
                    <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
                        <tr>
                            <td style="padding: 8px 0; font-weight: bold; color: #666; width: 30%;">Incident Type:</td>
                            <td style="padding: 8px 0; color: #d9534f; font-weight: bold;">{subject}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; font-weight: bold; color: #666;">Description:</td>
                            <td style="padding: 8px 0; color: #333; background-color: #fff5f5; padding-left: 8px; border-left: 3px solid #d9534f;">{body}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; font-weight: bold; color: #666;">Target Inbox:</td>
                            <td style="padding: 8px 0; color: #0066cc; font-family: monospace;">{to_email}</td>
                        </tr>
                    </table>
                    
                    <hr style="border: 0; border-top: 1px solid #eeeeee; margin: 20px 0;" />
                    
                    <p style="font-size: 14px; color: #777; margin-bottom: 0;">
                        <strong>Next Steps:</strong> Please inspect your active <code>dlq_monitor.py</code> streams or access your Grafana dashboard to check your metrics state panels.
                    </p>
                </div>
                
                <div style="background-color: #f4f4f4; padding: 15px; text-align: center; font-size: 12px; color: #888; border-top: 1px solid #e0e0e0;">
                    Automated Event-Driven Monitoring Engine • Swadesi Enterprises
                </div>
            </div>
        </body>
        </html>
        """

        # Attach HTML body data to the message
        msg.attach(MIMEText(html_content, "html"))

        # Initialize secure SMTP connection loop
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()

        print("✅ Email sent successfully")

    except Exception as e:
        print("❌ Email failed:", str(e))