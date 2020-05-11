# signup

Sigunup user

 - URL: /api/v1/auth/signup
 - method: POST

## Arguments
 - username - Username of user
 - email - email of user

### Restriction

 - If email already exists in DB we returns {'error': 'email_exists'}
 - If email does not belong to registered school, we return {'error': 'no_school'}
     For testing, all emails ended with `@noschool.edu' will return this error
 - If username name exists, we return {'error': 'username_exists'}
     For testing, all emails ended with `@noschool.edu' will return this error

## Success

Returns {'verification_code': 'aaaaaaa'}

For testing, we  return code, so we can use it later
