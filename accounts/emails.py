from django.conf import settings
from django.core.mail import EmailMultiAlternatives

def send_verification_email(user):
    verify_url = (
        f"{settings.FRONTEND_URL}/verify-email/{user.verification_token}"
    )

    subject = "Verify Your DevTrack Account"

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin:0;padding:0;background:#090d13;font-family:'Segoe UI',Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#090d13;padding:40px 20px;">
    <tr>
      <td align="center">
        <table width="520" cellpadding="0" cellspacing="0" style="background:#0f172a;border:1px solid #1e293b;border-radius:12px;overflow:hidden;">

          <!-- Header -->
          <tr>
            <td style="padding:28px 32px;border-bottom:1px solid #1e293b;">
              <span style="font-family:'Courier New',monospace;font-size:16px;font-weight:700;color:#f1f5f9;">
                <span style="color:#38bdf8;">[</span>
                &#9679;
                DevTrack
                <span style="color:#38bdf8;">]</span>
              </span>
            </td>
          </tr>

          <!-- Body -->
          <tr>
            <td style="padding:32px;">
              <p style="font-family:'Courier New',monospace;font-size:11px;color:#38bdf8;letter-spacing:0.1em;text-transform:uppercase;margin:0 0 16px;">
                // verify your email
              </p>
              <h1 style="font-size:22px;font-weight:700;color:#f1f5f9;margin:0 0 12px;">
                Welcome to DevTrack, {user.full_name.split()[0]}
              </h1>
              <p style="font-size:14px;color:#94a3b8;line-height:1.7;margin:0 0 28px;">
                You're one step away from accessing your workspace.
                Click the button below to verify your email address and activate your account.
              </p>

              <!-- Button -->
              <table cellpadding="0" cellspacing="0">
                <tr>
                  <td style="background:#38bdf8;border-radius:8px;">
                    <a href="{verify_url}"
                       style="display:inline-block;padding:12px 28px;font-family:'Courier New',monospace;font-size:13px;font-weight:700;color:#090d13;text-decoration:none;letter-spacing:0.05em;">
                      verify my account
                    </a>
                  </td>
                </tr>
              </table>

              <p style="font-size:12px;color:#475569;margin:24px 0 0;line-height:1.6;">
                Or copy this link into your browser:<br>
                <span style="color:#38bdf8;word-break:break-all;">{verify_url}</span>
              </p>

              <p style="font-size:12px;color:#334155;margin:20px 0 0;">
                This link expires in 24 hours. If you didn't create a DevTrack account, ignore this email.
              </p>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="padding:16px 32px;border-top:1px solid #1e293b;">
              <p style="font-size:11px;color:#334155;margin:0;font-family:'Courier New',monospace;">
                DevTrack · Built for developers and students
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""