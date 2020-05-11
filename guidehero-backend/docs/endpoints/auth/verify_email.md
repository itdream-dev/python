# verify_email

When user signup we send him verification code on his emal. User should use this endpoint to validate it.
When user validate his email, we activate his account and reset verification code to ''


 - URL: /api/v1/auth/verify_email
 - method: POST

## Arguments
 - email - email of user
 - code - Verification code geting by email (for testing, you can find verification code in response of *signup* endpoint

## Success

Returns {}
