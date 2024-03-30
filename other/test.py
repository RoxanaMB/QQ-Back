from server.db import supabase

email: str = 'roxanababa5@gmail.com'
password: str = 'roxanababa18'

user = supabase.auth.sign_up({
  "email": email, 
  "password": password,
  "options": {
    "data": {
      "username": "roxanababa5"
    }
  }
})


print(user.user.id)
print(user.session.access_token)