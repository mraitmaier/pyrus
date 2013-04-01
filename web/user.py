"""
    user.py
"""

import web
from pyrus.core.user import User, Role

urls = ("/user", "User",
        "/chpwd", "ChangePwd",
        "/login", "Login"
    )

render = web.template.render("templates/")

app = web.application(urls, globals())

# user form data
_ROLE_VALS = ["User", "Admin", "Guest", "Tester", "Developer", "Manager"]

vemail = web.form.regexp(r".*@.*", "Must be a valid email address")

userForm = web.form.Form(
        web.form.Textbox("user", description="Username"),
        web.form.Password("passwd", description="Password"),
        web.form.Textbox("fullname", description="Full name"),
        web.form.Dropdown("role",  args=_ROLE_VALS, value="User", 
            description="User role"),
        web.form.Textbox("email", vemail, description="E-mail address"),
        web.form.Button("submit", description="Submit", type="submit"),
        web.form.Button("reset", description="Reset", type="reset")
        )

# change password data
chpwdForm = web.form.Form(
        web.form.Password("old", description="Old password"),
        web.form.Password("new", description="New password"),
        web.form.Password("retype", description="Retype new"),
        web.form.Button("submit", description="Change", type="submit"),
        web.form.Button("reset", description="Reset", type="reset"),
        validators = [
            web.form.Validator("Passwords do not match", 
                            lambda f: f.new == f.retype)
            ]
        )

# login form data
loginForm = web.form.Form(
        web.form.Textbox("user", description="Username"),
        web.form.Password("passwd", description="Password"),
        web.form.Button("submit", description="Login", type="submit"),
        )

class Login:

    def GET(self):
        return render.login(loginForm)

class User:

    def GET(self):
        return render.user(userForm, "")

    def POST(self):
        s = "Form data"
        if not userForm.validates():
            return render.user(userForm, "Some err message!")
        return str(userForm.value)

class ChangePwd:

    def GET(self):
        i = web.input(user="Unknown")
        return render.chpwd(chpwdForm, i.user)

    def POST(self):
        return "Password changed."

if __name__ == "__main__":
    app.run()
