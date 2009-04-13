""" Django settings for stager project. """
import os
from datetime import date

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'
DATABASE_NAME = 'stager'
DATABASE_USER = 'root'
DATABASE_PASSWORD = 'root' 
DATABASE_HOST = 'localhost'
DATABASE_PORT = ''

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1
USE_I18N = False


BASE_URL = "http://127.0.0.1:8000/"

MEDIA_PREFIX = 'static'
MEDIA_URL = BASE_URL + MEDIA_PREFIX + "/"

MEDIA_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), 
                "../" + MEDIA_PREFIX)
BASE_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../")

ADMIN_MEDIA_PREFIX = '/media/'
SECRET_KEY = '+3&#_r^#t8jr%h6(6ec(f6am!0lu%y%&*29t_z-#+kfv9ofg@l'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'stager.urls'

TEMPLATE_DIRS = [os.path.join(os.path.dirname(__file__), "../templates")]

AUTH_PROFILE_MODULE = 'stager.Client'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'stager.staging', 
    'svn_revision',
    'django_evolution',
    'export'
)

# Stager Settings
FILE_UPLOAD = 'upload'
MAX_UPLOAD_SIZE = 5242880
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Export Settings
MYSQLDUMP_CMD = 'mysqldump -h %s --opt --compact --skip-add-locks -u %s -p%s %s'
DATABASE_FILENAME = date.today().__str__()+'_db.sql'

# Active Directory / LDAP Settings
AUTHENTICATION_BACKENDS = (
    # Uncomment this for Active Directory / LDAP support
    # 'stager.backends.ActiveDirectoryGroupMembershipSSLBackend',
    'django.contrib.auth.backends.ModelBackend',
)

AD_DNS_NAME='ai.lan'

# If using non-SSL use these
AD_LDAP_PORT=389
AD_LDAP_URL='ldap://%s:%s' % (AD_DNS_NAME,AD_LDAP_PORT)

# If using SSL use these:
#AD_LDAP_PORT=636
#AD_LDAP_URL='ldaps://%s:%s' % (AD_DNS_NAME,AD_LDAP_PORT)

AD_SEARCH_DN='OU=SBSUsers,OU=Users,OU=MyBusiness,DC=ai,DC=lan'
AD_NT4_DOMAIN='AI'
AD_SEARCH_FIELDS= ['mail','givenName','sn','sAMAccountName','memberOf']
AD_MEMBERSHIP_REQ=['AlexanderInteractive']
AD_CERT_FILE='/path/to/your/cert.txt'

AD_DEBUG=True
AD_DEBUG_FILE='ldap.debug'

