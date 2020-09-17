from porsgram.settings import TEMPLATES_DIR

USER  = TEMPLATES_DIR + '/user/'
QA    = TEMPLATES_DIR + '/qa/'
EMAIL = TEMPLATES_DIR + '/email/'



EMAIL_RESET_PASSWORD_TEMPLATE = USER + '/resetPasswordTemplate.html'
USER_CONFIRM_EMAIL_TEMPLATE   = USER + 'confirmEmailTemplate.html'

USER_GET_EMAIL = USER + 'getEmail.html'
USER_DASHBOARD = USER + 'dashboard.html'
USER_LOGIN     = USER + 'login.html'
USER_LOGOUT    = USER + 'logout.html'
USER_REGISTER  = USER + 'register.html'
USER_USERS     = USER + 'users.html'
USER_USER      = USER + 'user.html'

QA_CREATE_QUESTION = QA + 'createQuestion.html'
QA_QUESTION        = QA + 'question.html'
QA_QUESTIONS       = QA + 'questions.html'
QA_QUESTIONS_TAGED = QA + 'questionsTaged.html'
QA_EDIT_QUESTION   = QA + 'editQuestion.html'
QA_EDIT_ANSWER     = QA + 'editAnswer.html'
QA_INDEX           = QA + 'index.html'
QA_TAGS            = QA + 'tags.html'


EMAIL_PAGE_TEMPLATE  = EMAIL + '/is_confirmed-email.html'


PAGE_400 = TEMPLATES_DIR + '/400.html'
PAGE_403 = TEMPLATES_DIR + '/403.html'
PAGE_404 = TEMPLATES_DIR + '/404.html'
PAGE_500 = TEMPLATES_DIR + '/500.html'


