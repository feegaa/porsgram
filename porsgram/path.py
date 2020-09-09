from porsgram.settings import TEMPLATES_DIR

USER  = TEMPLATES_DIR + '/user/'
QA    = TEMPLATES_DIR + '/qa/'
EMAIL = TEMPLATES_DIR + '/email/'



EMAIL_RESET_PASSWORD_TEMPLATE = USER + '/resetPasswordTemplate.html'
USER_CONFIRM_EMAIL_TEMPLATE   = USER + 'confirmEmailTemplate.html'

USER_GET_EMAIL_RESET_PASSWORD = USER + 'dashboard.html'
USER_DASHBOARD                = USER + 'dashboard.html'
USER_LOGIN                    = USER + 'login.html'
USER_LOGOUT                   = USER + 'logout.html'
USER_REGISTER                 = USER + 'register.html'
USER_USERS                    = USER + 'users.html'
USER_USER                     = USER + 'user.html'

QA_CREATE_QUESTION = QA + 'createQuestion.html'
QA_QUESTION        = QA + 'question.html'
QA_QUESTIONS       = QA + 'questions.html'
QA_EDIT_QUESTION   = QA + 'editQuestion.html'
QA_EDIT_ANSWER     = QA + 'editAnswer.html'
QA_INDEX           = QA + 'index.html'


EMAIL_PAGE_TEMPLATE  = EMAIL + '/is_confirmed-email.html'
