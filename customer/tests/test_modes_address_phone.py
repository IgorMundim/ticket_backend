from customer.models import Address, Telephone


def test_create_address_with_account(create_address_account):
    new_address = create_address_account
    get_address = Address.objects.all().first()
    assert new_address.id == get_address.id
    assert new_address.account_id.username == get_address.account_id.username


def test_telephone_wite_account(telephone_wite_account):
    new_telephone = telephone_wite_account
    get_telephone = Telephone.objects.all().first()
    assert new_telephone.id == get_telephone.id
    assert (
        new_telephone.account_id.username == get_telephone.account_id.username
    )
