# signup / send confirmation email

Sigunup user and sending confirmation email to the college email

 - URL: /api/v1/auth/send_confirmation_email
 - method: POST

## Arguments
 - email: email of user (college email)
 - username: string
 - year: integer, year of graduation ex 2014 or 2015

### Restriction
 - {"error": "invalid_arguments"} if missing email
 - {"error": "email_already_registered"} if email is already a verified email
 - {"error": "username_already_exists"} if username is already taken

## Success
Returns {"result": "success"} and also sends an email to the registered email


# resend confirmation email

resend confirmation email to the college email

 - URL: /api/v1/auth/resend_confirmation_email
 - method: POST

## Arguments
 - email: email of user (college email)

### Restriction
 - {"error": "invalid_arguments"} if missing email
 - {"error": "email_already_registered"} if email is already a verified email
 - {"error": "email_not_registered"} if trying to send a code to an email that didn't go through the signup procress

## Success
Returns {"result": "success"} and also sends an email to the registered email


# check confirmation code

Checking confirmation code
 - URL: /api/v1/auth/check_confirmation_code
 - method: POST

## Arguments
 - email: email of user (university email)
 - confirmation_code: six digit string

### Restriction
 - {"error": "invalid_arguments"} if missing email or confirmation code
 - {"error": email_not_registered"} if email wasn't registered yet
 - {"error": "invalid_confirmation_code"} if confirmation code is wrong

## Success
Returns {"result": "success"}


# facebook signin

Logging in with FB
 - URL: /api/v1/auth/fb_signin_v2
 - method: POST

## Arguments
 - email: email of user (university email)
 - confirmation_code: six digit string
 - fb_access_token: token we get from the FB sdk

### Restriction
 - {"error": "invalid_arguments"} if missing email or confirmation code
 - {"error": email_not_registered"} if email wasn't registered yet
 - {"error": "invalid_confirmation_code"} if confirmation code is wrong
 - {"error": "missing_access_token"} if missing fb access token
 - {"error": "authentication_failed"} if fb authentication fails
 - {"error": "not_verified"} if fb account is not verified
 - {"error": "no_email_account"} if there is no email attached to the fb account

## Success
Returns same thing that /api/v1/auth/fb_signin currently returns

eg. 
{
    "auth_token": ".eJwFwcERwCAIBMBeeIcZiaJHLZk8kDP9l5DdR9qOZoDpgKcOVipwSidnnlmxQMolvUXvN9c9Kj0A2k6OIM2Xf2Xy_tx-E7c.C6EQow.VpA492tT506H3BzsyJsh0ngfSG0",
    "user": {
        "active": true,
        "bio": null,
        "confirmed_at": 1486833172,
        "email": "yoyo716jp@gmail.com",
        "first_name": "Yohei",
        "id": "0b901881-485a-4dca-88ec-6d6ae6c978dd",
        "is_admin": false,
        "last_name": "Oka",
        "linkedin_headline": null,
        "linkedin_profile": null,
        "source": "facebook",
        "stripped_email": "yoyo716jp@gmail.com",
        "thumbnail_url": "https://scontent.xx.fbcdn.net/v/t1.0-1/p100x100/12800312_10153396661506404_4671822119048369673_n.jpg?oh=3c6d4235c7545668ea24891a13775a0e&oe=59431D32",
        "tier": "",
        "total_silver_points": 1000,
        "username": "yoheioka"
    }
}