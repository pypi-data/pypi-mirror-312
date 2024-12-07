"""
Classes supporting the management of user credentials and certificates.
"""
from datetime import datetime
from typing import Optional, TypeVar
from . import root
from dateutil import parser as dateparser # Change to use datetime.fromisoformat when we stop supporting Python 3.10.
from .util import now
from enum import Enum

class CredentialsLifespan(Enum):
    """The lifespan of the credentials. SHORT_LIVED refers to access tokens and other dynamically generated credentials
    with a typically short-term expiry and may automatically refresh. LONG_LIVED refers to manually created credentials
    that have no expiry or a long-term expiry and do not refresh automatically."""
    SHORT_LIVED = 10
    LONG_LIVED = 20


class Credentials(root.AbstractDesktopObject):
    """
    Stores a user's secrets, passwords, and keys, and makes them available to applications.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__account: str | None = None
        self.__where: str | None = None
        self.__password: str | None = None
        self.__role: str | None = None
        self.__expiration: datetime | None = None
        self.__lifespan = CredentialsLifespan.LONG_LIVED

    @property  # type: ignore
    def account(self) -> Optional[str]:
        """
        The username or account name.
        """
        return self.__account

    @account.setter  # type: ignore
    def account(self, account: Optional[str]) -> None:
        self.__account = str(account) if account is not None else None

    @property  # type: ignore
    def where(self) -> Optional[str]:
        """
        The hostname, URL, service, or other location of the account.
        """
        return self.__where

    @where.setter  # type: ignore
    def where(self, where: Optional[str]) -> None:
        self.__where = str(where) if where is not None else None

    @property  # type: ignore
    def password(self) -> Optional[str]:
        """
        The account password or secret
        """
        return self.__password

    @password.setter  # type: ignore
    def password(self, password: Optional[str]) -> None:
        self.__password = str(password) if password is not None else None

    @property
    def type_display_name(self) -> str:
        return "Credentials"

    @property
    def role(self) -> str | None:
        """A role to assume while logged in with these credentials."""
        return self.__role

    @role.setter
    def role(self, role: str | None):
        self.__role = str(role) if role is not None else None

    @property
    def expiration(self) -> datetime | None:
        """
        The session's expiration time. Setting this property with an ISO 8601 string will also work -- the ISO string
        will be parsed automatically as a datetime object. If the provided datetime has no timezone information, it is
        assumed to be in local time.
        """
        return self.__expiration

    @expiration.setter
    def expiration(self, expiration: str | datetime | None) -> None:
        date_obj = None
        if isinstance(expiration, datetime):
            date_obj = expiration
        elif isinstance(expiration, str):
            # Change to use datetime.fromisoformat when we stop supporting Python 3.10.
            date_obj = dateparser.isoparse(expiration)
        elif expiration:
            raise ValueError("Invalid Expiration type")

        self.__expiration = date_obj

    def has_expired(self, exp_diff = 0):
        """
        Returns whether these credentials have expired. If this object's expiration attribute is None, has_expired()
        always returned True.

        :param exp_diff: the difference between expiration and current time in minutes (default to zero).
        :return: whether these credentials have expired or not.
        """
        if not self.expiration:
            #if not field not set allow credentials to generated to set it
            return True
        diff = self.expiration.astimezone() - now()
        return (diff.total_seconds() / 60) < exp_diff

    @property
    def lifespan(self) -> CredentialsLifespan:
        """The credentials' lifespan, by default CredentialsLifespan.LONG_LIVED."""
        return self.__lifespan

    @lifespan.setter
    def lifespan(self, lifespan: CredentialsLifespan):
        self.__lifespan = lifespan if isinstance(lifespan, CredentialsLifespan) else CredentialsLifespan[str(lifespan)]

    def set_lifespan_from_str(self, lifespan: str):
        """
        Sets the lifespan from a string.

        :param lifespan: CredentialsLifespan.SHORT_LIVED or CredentialsLifespan.LONG_LIVED.
        """
        self.__lifespan = CredentialsLifespan[str(lifespan)]

CredentialTypeVar = TypeVar('CredentialTypeVar', bound=Credentials)


class AWSCredentials(Credentials):
    """
    Credentials object extended with AWS-specific attributes. The role attribute should contain the role ARN.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__session_token: Optional[str] = None
        self.__managed = False
        self.__role: str | None = None
        self.__account_id: str | None = None

    @property
    def session_token(self) -> Optional[str]:
        """
        The session token.
        """
        return self.__session_token

    @session_token.setter
    def session_token(self, session_token: Optional[str]):
        self.__session_token = str(session_token) if session_token is not None else None

    @property
    def temporary(self) -> bool:
        """Whether or not to use AWS' temporary credentials generation mechanism. The default value is False. Setting
        this property to False sets the lifespan property to LONG_LIVED. Setting it to True sets the lifespan property
        to SHORT_LIVED. Likewise, setting the lifespan property to LONG_LIVED sets this property to False, and setting
        the lifespan property to SHORT_LIVED sets this property to True."""
        return self.lifespan == CredentialsLifespan.SHORT_LIVED

    @temporary.setter
    def temporary(self, temporary: bool):
        self.lifespan = CredentialsLifespan.SHORT_LIVED if bool(temporary) else CredentialsLifespan.LONG_LIVED

    @property
    def managed(self) -> bool:
        """Flag to determine if AWS credential's lifecycle is managed by system. The default value is False."""
        return self.__managed

    @managed.setter
    def managed(self, managed: bool):
        self.__managed = bool(managed)

    @property
    def type_display_name(self) -> str:
        return "AWS Credentials"

    @property
    def role(self) -> str | None:
        """The role ARN."""
        return self.__role

    @role.setter
    def role(self, role: str | None):
        if role is not None:
            self.__role = str(role)
            try:
                _, partition, service, region, acct_id, rest = role.split(':', maxsplit=5)
                self.__account_id = acct_id if acct_id != '' else None
            except IndexError as e:
                raise ValueError('Invalid role ARN') from e
        else:
            self.__role = None
            self.__account_id = None


    @property
    def account_id(self) -> str | None:
        """The AWS account number extracted from the role ARN."""
        return self.__account_id


class CredentialsView(root.AbstractDesktopObject, root.View):
    def __init__(self) -> None:
        super().__init__()
        self.__actual_object_id: str | None = None
        self.__actual_object_type_name: str | None = None
        self.__type_display_name: str | None = None

    @property
    def actual_object_id(self) -> str | None:
        return self.__actual_object_id

    @actual_object_id.setter
    def actual_object_id(self, actual_object_id: str | None):
        self.__actual_object_id = str(actual_object_id) if actual_object_id is not None else None
        self.id = f'{self.actual_object_type_name}^{self.__actual_object_id}'

    @property
    def actual_object_type_name(self) -> str | None:
        return self.__actual_object_type_name

    @actual_object_type_name.setter
    def actual_object_type_name(self, actual_object_type_name: str | None):
        self.__actual_object_type_name = str(actual_object_type_name) if actual_object_type_name is not None else None
        self.id = f'{self.__actual_object_type_name}^{self.actual_object_id}'

    @property
    def type_display_name(self) -> str:
        if self.__type_display_name is not None:
            return self.__type_display_name
        if (actual := self.actual_object_type_name) is not None:
            return root.desktop_object_type_for_name(actual).__name__
        else:
            return 'Credentials'

    @type_display_name.setter
    def type_display_name(self, type_display_name: str):
        self.__type_display_name = str(type_display_name) if type_display_name is not None else None
