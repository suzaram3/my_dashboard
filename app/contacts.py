from . import db
from .models import Contact

def update_next_contact(contacts: list) -> None:
    pass

def main():
    ZZ
    contacts = Contact.query.all()
    print(contacts[0].last_contact)


main()