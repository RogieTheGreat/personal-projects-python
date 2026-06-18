from project import valid_tel, format_name, valid_rating

def test_valid_tel():
    assert valid_tel("12345678") == True
    assert valid_tel("123") == False
    assert valid_tel("abc12345") == False

def test_format_name():
    assert format_name(" rogIE ") == "Rogie"
    assert format_name("mcdonalds") == "Mcdonalds"

def test_valid_rating():
    assert valid_rating(5) == True
    assert valid_rating(0) == False
    assert valid_rating(6) == False
