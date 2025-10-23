# EchoAuth ELS (Email Login System)

EchoAuth ELS is a system that allows users to send emails to a specific email address to log in to a service. The system verifies the email and grants access based on the content of the email.

## Expected Flow

- User gives email address to Application
- Application gives a code to the user
  - Unique code per email per device
- User sends an email to a specific email address
  - Subject: Login
  - Body: Code (keep it plain text)
- ELS verifies the email
- Application grants access

