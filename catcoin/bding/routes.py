from bding.handlers import login, register

def setup_routes(app):
    app.router.add_post('/login/',login.handle_login)
    app.router.add_post('/register/',register.handle_register)
    app.router.add_post('/sms/netease/{app_name}/send_template',
                        netease.handle_send_template)
    app.router.add_post('/sms/twilio/{app_name}/send',
                        twilio.handle_send_sms)
    app.router.add_post('/email/{app_name}/send',
                        smtp.handle_send_email)
