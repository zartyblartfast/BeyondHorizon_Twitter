# Gmail SMTP Authentication Issue

## Current Status
- Gmail SMTP authentication failing with error: "Application-specific password required"
- 2-Factor authentication has been set up
- App Password has been generated but not working yet

## Steps Taken
1. Set up dedicated Gmail account: longlineofsight@gmail.com
2. Enabled 2-Factor Authentication
3. Generated App Password for "BeyondHorizon_Bot": bvzi lone oqcz fpus
4. Updated .env file with credentials

## Error Message
```
Error sending via Gmail SMTP: (534, b'5.7.9 Application-specific password required. For more information, go to\n5.7.9  https://support.google.com/mail/?p=InvalidSecondFactor')
```

## Next Steps
1. Verify App Password is correctly formatted in .env file (no spaces)
2. Check if Gmail's SMTP settings need to be explicitly enabled
3. Verify PythonAnywhere's firewall is allowing Gmail SMTP (port 587)
4. Consider testing locally first to isolate if issue is PythonAnywhere-specific

## Resources
- [Gmail SMTP Settings](https://support.google.com/mail/answer/7126229)
- [PythonAnywhere Gmail SMTP Guide](https://help.pythonanywhere.com/pages/SMTPForFreeUsers/)
