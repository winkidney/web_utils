# -*- coding:utf-8 -*-
import hashlib
import hmac
import logging
import bcrypt

__author__ = 'winkidney'

__all__ = (
        'AuthBcrypt',
        'RedirectSignature',
        'ISignaturePolicy',
)


class AuthBcrypt(object):

    """Generate Bcrypt password and check if the input
        string is vaild.
    """

    def __init__(self):
        """

        :param salt: salt to generate.
        :return:
        """
    @classmethod
    def _conv2str(cls, uchar):
        if isinstance(uchar, unicode):
            uchar = uchar.encode('utf-8')
        elif isinstance(uchar, str):
            pass
        else:
            raise TypeError('%s must be a unicode/str object.')
        return uchar

    @classmethod
    def _gensalt(cls):
        return bcrypt.gensalt()

    @classmethod
    def checkpwd(cls, user_pwd, db_pwd):
        """
        :param user_pwd: user's input password
        :type user_pwd: str
        :param db_pwd: hashed passwd in db
        :type db_pwd: str
        :return:True if success,False if authenticating fail.
        """
        user_pwd = cls._conv2str(user_pwd)
        db_pwd = cls._conv2str(db_pwd)
        if db_pwd == bcrypt.hashpw(user_pwd, db_pwd):
            return True
        return False

    @classmethod
    def genpwd(cls, input_pwd):
        """
        :param input_pwd: user input passwd.
        :return: generated pwd
        """
        input_pwd = cls._conv2str(input_pwd)
        return bcrypt.hashpw(input_pwd, cls._gensalt())

# todo : Change default DEFAULT_HMAC_SECRET
DEFAULT_HMAC_SECRET = 'hijialop365o*&jkj~'


class ISignaturePolicy(object):

    def __init__(self):
        raise NotImplementedError("Over write __init__ method of this class!")

    @staticmethod
    def _conv2str(uchar):
        if isinstance(uchar, unicode):
            uchar = uchar.encode('utf-8')
        elif isinstance(uchar, str):
            pass
        else:
            raise TypeError('%s must be a unicode/str object.')
        return uchar

    @classmethod
    def _sign_it(cls, message, secret):
        """
        :param secret: secret str to sign the url
        :param message: a string or unicode object
        :type secret: unicode
        :type secret: str
        :type message: str, unicode
        :return: generated signed hexdigest str
        """
        secret = cls._conv2str(secret)
        if secret and message:
            return hmac.HMAC(secret, message, hashlib.sha256).hexdigest()
        else:
            raise ValueError('the secret or url parameter can not be null!')


class RedirectSignature(ISignaturePolicy):

    """
    check if a redirect url is valid or generate a signed url.
    """

    def __init__(self):
        raise NotImplementedError('This class provides static methods '
                                  'to provide redirecting function, do not create instance.')

    @classmethod
    def gen_reditrct(cls, target_path):
        return ''.join((target_path, '?sign=%s' % (cls.sign_url(DEFAULT_HMAC_SECRET, target_path))))

    @classmethod
    def valid_redirect(cls, url, sign, secret=DEFAULT_HMAC_SECRET):
        """
        :param url: input url in get info
        :param sign:
        :return: url if sign is valid, '/' if sign is not valid.
        """
        if not url:
            return '/'
        if cls.sign_url(url, secret) == sign:
            return url
        else:
            return '/'

    @classmethod
    def sign_url(cls, url, secret=DEFAULT_HMAC_SECRET):
        """
        sign a given url by given secret.
        :type secret: str or unicode
        :type url: str or unicode
        """
        if secret == DEFAULT_HMAC_SECRET:
            logging.warning("URL_SING_SECRET not found in .ini, use default secret!")
        return cls._sign_it(url, secret)
