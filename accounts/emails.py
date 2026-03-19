from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
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
    text_content = f"Verify your DevTrack account:\n{verify_url}"

    msg = EmailMultiAlternatives(
        subject,
        text_content,
        settings.EMAIL_HOST_USER,
        [user.email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def send_welcome_email(user):
    subject = "You're in — welcome to DevTrack"

    html_content = f"""
<!DOCTYPE html>
<html>
<body style="margin:0;padding:0;background:#090d13;font-family:'Segoe UI',Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#090d13;padding:40px 20px;">
    <tr>
      <td align="center">
        <table width="520" cellpadding="0" cellspacing="0" style="background:#0f172a;border:1px solid #1e293b;border-radius:12px;overflow:hidden;">
          <tr>
            <td style="padding:28px 32px;border-bottom:1px solid #1e293b;">
              <span style="font-family:'Courier New',monospace;font-size:16px;font-weight:700;color:#f1f5f9;">
                <span style="color:#38bdf8;">[</span> &#9679; DevTrack <span style="color:#38bdf8;">]</span>
              </span>
            </td>
          </tr>
          <tr>
            <td style="padding:32px;">
              <p style="font-family:'Courier New',monospace;font-size:11px;color:#34d399;letter-spacing:0.1em;text-transform:uppercase;margin:0 0 16px;">
                // account verified
              </p>
              <h1 style="font-size:22px;font-weight:700;color:#f1f5f9;margin:0 0 12px;">
                You're all set, {user.full_name.split()[0]}
              </h1>
              <p style="font-size:14px;color:#94a3b8;line-height:1.7;margin:0 0 24px;">
                Your DevTrack account is now active. Here's what you can do:
              </p>
              <table cellpadding="0" cellspacing="0" width="100%" style="margin-bottom:24px;">
                <tr><td style="padding:8px 0;border-bottom:1px solid #1e293b;">
                  <span style="color:#38bdf8;font-family:'Courier New',monospace;font-size:12px;">→</span>
                  <span style="font-size:13px;color:#94a3b8;margin-left:10px;">Track your projects and skills</span>
                </td></tr>
                <tr><td style="padding:8px 0;border-bottom:1px solid #1e293b;">
                  <span style="color:#38bdf8;font-family:'Courier New',monospace;font-size:12px;">→</span>
                  <span style="font-size:13px;color:#94a3b8;margin-left:10px;">Capture ideas in your vault</span>
                </td></tr>
                <tr><td style="padding:8px 0;border-bottom:1px solid #1e293b;">
                  <span style="color:#38bdf8;font-family:'Courier New',monospace;font-size:12px;">→</span>
                  <span style="font-size:13px;color:#94a3b8;margin-left:10px;">Monitor assignment deadlines</span>
                </td></tr>
                <tr><td style="padding:8px 0;">
                  <span style="color:#38bdf8;font-family:'Courier New',monospace;font-size:12px;">→</span>
                  <span style="font-size:13px;color:#94a3b8;margin-left:10px;">Plan your week every Monday</span>
                </td></tr>
              </table>
              <table cellpadding="0" cellspacing="0">
                <tr>
                  <td style="background:#38bdf8;border-radius:8px;">
                    <a href="{settings.FRONTEND_URL}/dashboard"
                       style="display:inline-block;padding:12px 28px;font-family:'Courier New',monospace;font-size:13px;font-weight:700;color:#090d13;text-decoration:none;">
                      go to dashboard
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
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

    text_content = f"Welcome to DevTrack! Go to your dashboard: {settings.FRONTEND_URL}/dashboard"

    msg = EmailMultiAlternatives(
        subject,
        text_content,
        settings.EMAIL_HOST_USER,
        [user.email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def send_overdue_reminder(user, assignments):
    if not assignments:
        return

    rows = ""
    for a in assignments:
        rows += f"""
        <tr>
          <td style="padding:10px 0;border-bottom:1px solid #1e293b;">
            <span style="font-size:13px;color:#fca5a5;font-weight:600;">{a.title}</span><br>
            <span style="font-size:11px;color:#475569;font-family:'Courier New',monospace;">{a.subject or 'No subject'}</span>
          </td>
        </tr>
        """

    subject = f"⚠️ You have {len(assignments)} overdue assignment{'s' if len(assignments) > 1 else ''}"

    html_content = f"""
<!DOCTYPE html>
<html>
<body style="margin:0;padding:0;background:#090d13;font-family:'Segoe UI',Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#090d13;padding:40px 20px;">
    <tr><td align="center">
      <table width="520" cellpadding="0" cellspacing="0" style="background:#0f172a;border:1px solid #1e293b;border-radius:12px;overflow:hidden;">
        <tr><td style="padding:28px 32px;border-bottom:1px solid #1e293b;">
          <span style="font-family:'Courier New',monospace;font-size:16px;font-weight:700;color:#f1f5f9;">
            <span style="color:#38bdf8;">[</span> &#9679; DevTrack <span style="color:#38bdf8;">]</span>
          </span>
        </td></tr>
        <tr><td style="padding:32px;">
          <p style="font-family:'Courier New',monospace;font-size:11px;color:#f87171;letter-spacing:0.1em;text-transform:uppercase;margin:0 0 16px;">
            // overdue assignments
          </p>
          <h1 style="font-size:20px;font-weight:700;color:#f1f5f9;margin:0 0 8px;">
            Hey {user.full_name.split()[0]}, you have overdue work
          </h1>
          <p style="font-size:14px;color:#94a3b8;margin:0 0 24px;">
            The following assignments are past their deadline:
          </p>
          <table width="100%" cellpadding="0" cellspacing="0">
            {rows}
          </table>
          <table cellpadding="0" cellspacing="0" style="margin-top:24px;">
            <tr><td style="background:#f87171;border-radius:8px;">
              <a href="{settings.FRONTEND_URL}/assignments"
                 style="display:inline-block;padding:12px 28px;font-family:'Courier New',monospace;font-size:13px;font-weight:700;color:#090d13;text-decoration:none;">
                view assignments
              </a>
            </td></tr>
          </table>
        </td></tr>
        <tr><td style="padding:16px 32px;border-top:1px solid #1e293b;">
          <p style="font-size:11px;color:#334155;margin:0;font-family:'Courier New',monospace;">DevTrack · Built for developers and students</p>
        </td></tr>
      </table>
    </td></tr>
  </table>
</body>
</html>
    """

    text_content = f"You have {len(assignments)} overdue assignments. Visit: {settings.FRONTEND_URL}/assignments"
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [user.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    
def send_stale_skills_reminder(user, skills):
    if not skills:
        return

    rows = ""
    for s in skills:
        rows += f"""
        <tr>
          <td style="padding:10px 0;border-bottom:1px solid #1e293b;">
            <span style="font-size:13px;color:#fde68a;font-weight:600;">{s.name}</span><br>
            <span style="font-size:11px;color:#475569;font-family:'Courier New',monospace;">{s.category} · depth {s.depth_level}</span>
          </td>
        </tr>
        """

    subject = f"🧠 {len(skills)} skill{'s' if len(skills) > 1 else ''} going stale — time to practice"

    html_content = f"""
<!DOCTYPE html>
<html>
<body style="margin:0;padding:0;background:#090d13;font-family:'Segoe UI',Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#090d13;padding:40px 20px;">
    <tr><td align="center">
      <table width="520" cellpadding="0" cellspacing="0" style="background:#0f172a;border:1px solid #1e293b;border-radius:12px;overflow:hidden;">
        <tr><td style="padding:28px 32px;border-bottom:1px solid #1e293b;">
          <span style="font-family:'Courier New',monospace;font-size:16px;font-weight:700;color:#f1f5f9;">
            <span style="color:#38bdf8;">[</span> &#9679; DevTrack <span style="color:#38bdf8;">]</span>
          </span>
        </td></tr>
        <tr><td style="padding:32px;">
          <p style="font-family:'Courier New',monospace;font-size:11px;color:#fbbf24;letter-spacing:0.1em;text-transform:uppercase;margin:0 0 16px;">
            // stale skills
          </p>
          <h1 style="font-size:20px;font-weight:700;color:#f1f5f9;margin:0 0 8px;">
            {user.full_name.split()[0]}, some skills need attention
          </h1>
          <p style="font-size:14px;color:#94a3b8;margin:0 0 24px;">
            These skills haven't been practiced in over 7 days:
          </p>
          <table width="100%" cellpadding="0" cellspacing="0">
            {rows}
          </table>
          <table cellpadding="0" cellspacing="0" style="margin-top:24px;">
            <tr><td style="background:#fbbf24;border-radius:8px;">
              <a href="{settings.FRONTEND_URL}/skills"
                 style="display:inline-block;padding:12px 28px;font-family:'Courier New',monospace;font-size:13px;font-weight:700;color:#090d13;text-decoration:none;">
                practice now
              </a>
            </td></tr>
          </table>
        </td></tr>
        <tr><td style="padding:16px 32px;border-top:1px solid #1e293b;">
          <p style="font-size:11px;color:#334155;margin:0;font-family:'Courier New',monospace;">DevTrack · Built for developers and students</p>
        </td></tr>
      </table>
    </td></tr>
  </table>
</body>
</html>
    """

    text_content = f"You have {len(skills)} stale skills. Visit: {settings.FRONTEND_URL}/skills"
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [user.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

