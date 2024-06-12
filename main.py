"""
This is a simple script for deleting one post at a time on your twitter/x account, it's slow and not implemented the
best possible, I know, but im just learning, it feels cool to actually be able to build something like this and deploy
it... I'll fix all the problems eventually, busy with finals at the moment.
"""

import datetime, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask_bootstrap import Bootstrap5

# TODO: Fix inputs so that the bot doesn't run/crash when user provides incorrect login details
# TODO: Change main page to display confirmation or complete messages when submitting info
# TODO: Add addresses to the footer, fix the footer too actually, maybe add images instead of words for links
# TODO: Add a checkbox for confirm receiving email for other stuff we build.
# TODO: Add comments and Doc strings.
# TODO: Look at X's api to see if we can implement this a different way
# TODO: Find more things to do in this code... it's messy and clunky
# TODO: Decide to either expand what this can do or keep it simple

current_year = str(datetime.date.today()).split('-')[0]

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config["SECRET_KEY"] = "GigaSecretKeyOfHell"


class XForm(FlaskForm):
    # TODO: Fix validators and add restrictions to inputs
    email = StringField("Enter your email:", )
    #username = StringField("Enter your username:")
    password = PasswordField("Enter your password:")
    submit = SubmitField("Delete")


@app.route("/", methods=["GET", "POST"])
def home():
    form = XForm()
    if form.validate_on_submit():
        email = form.data.get("email")
        username = form.data.get("username")
        password = form.data.get("password")
        # Add options so that the browser doesn't auto close
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)

        driver = webdriver.Chrome(chrome_options)

        driver.get("https://www.x.com/login")
        time.sleep(5)
        # Enter email
        email_field = driver.find_element(By.TAG_NAME, value='input')
        email_field.click()
        email_field.send_keys(email)
        email_field.send_keys(Keys.ENTER)
        time.sleep(2)

        # Enter password
        password_field = driver.find_element(By.CSS_SELECTOR, value='[type="password"]')
        password_field.send_keys(password)
        password_field.send_keys(Keys.ENTER)
        time.sleep(5)

        # Clicks on profile
        driver.find_element(By.CSS_SELECTOR, value='[aria-label="Profile"]').click()
        time.sleep(5)

        # Continues to Select the first post and clicks through the delete menus
        while True:
            try:
                driver.find_element(By.CSS_SELECTOR, value='[data-testid="caret"]').click()
                time.sleep(2)
                driver.find_element(By.CSS_SELECTOR, value='[role="menuitem"]').click()
                time.sleep(2)
                driver.find_element(By.CSS_SELECTOR, value='[data-testid="confirmationSheetConfirm"]').click()
                driver.refresh()
                time.sleep(4)
            except NoSuchElementException:
                break
        driver.quit()

    return render_template("index.html", form=form, current_year=current_year)


if __name__ == "__main__":
    app.run(debug=True)


# Leaving this in for debugging at the moment, instead of launching flask and server everytime I can tinker here.

# email = "YOUR EMAIL HERE"
# password = "YOUR PASSWORD HERE"
# username = "YOUR USERNAME HERE"
#
# Add options so that the browser doesn't auto close
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_experimental_option("detach", True)
#
# driver = webdriver.Chrome(chrome_options)
#
# driver.get("https://www.x.com/login")
# time.sleep(5)
# # Enter email
# email_field = driver.find_element(By.TAG_NAME, value='input')
# email_field.click()
# email_field.send_keys(email)
# email_field.send_keys(Keys.ENTER)
# time.sleep(2)
#
# # Enter username
# username_field = driver.find_element(By.TAG_NAME, value='input')
# username_field.send_keys(username)
# username_field.send_keys(Keys.ENTER)
# time.sleep(2)
#
# # Enter password
# password_field = driver.find_element(By.CSS_SELECTOR, value='[type="password"]')
# password_field.send_keys(password)
# password_field.send_keys(Keys.ENTER)
# time.sleep(5)
#
# # Clicks on profile
# driver.find_element(By.CSS_SELECTOR, value='[aria-label="Profile"]').click()
# time.sleep(5)
#
# # Continues to Select the first post and clicks through the delete menus
# while True:
#     try:
#         driver.find_element(By.CSS_SELECTOR, value='[data-testid="caret"]').click()
#         time.sleep(2)
#         driver.find_element(By.CSS_SELECTOR, value='[role="menuitem"]').click()
#         time.sleep(2)
#         driver.find_element(By.CSS_SELECTOR, value='[data-testid="confirmationSheetConfirm"]').click()
#         driver.refresh()
#         time.sleep(4)
#     except NoSuchElementException:
#         break
# driver.quit()
