from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Red', animal_type='Maine_Coon', age='1', pet_photo='images\cat_red.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_update_info_pet(name='Snow', animal_type='Cat', age='3'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_info_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("Нет питомцев")


def test_delete_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Boris", "cat", "1", "images\cat.jpeg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()


# 10 тестов для задания HW 24.7.2

def test_get_all_pets_with_invalid_key(filter=''):
    '''Test 1: Получение списка питомцев с несуществующим api-ключом
    (замена api-ключа на несуществующий у существующего пользователя)'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    auth_key = invalid_auth_key

    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status != 200


def test_get_api_key_for_invalid_user(email="not_real_email@1secmail.net", password="not_real_password"):
    '''Test 2: Получение api-ключа с данными незарегистрированного пользователя'''
    status, result = pf.get_api_key(email, password)
    assert status != 200
    assert 'key' not in result


def test_get_api_key_for_valid_user_invalid_password(email=valid_email, password="sf_test"):
    '''Test 3: Получение api-ключа с данными зарегистрированного пользователя с неверным паролем'''
    status, result = pf.get_api_key(email, password)
    assert status != 200
    assert 'key' not in result


def test_get_api_key_for_invalid_user_valid_password(email="sf_pet_chukicheva@1secmail.da", password=valid_password):
    '''Test 4: Получение api-ключа с опечаткой в электронной почте и правильным паролем'''
    status, result = pf.get_api_key(email, password)
    assert status != 200
    assert 'key' not in result


def test_get_my_pets_with_valid_key(filter='my_pets'):
    '''Test 5: Получение списка "моих питомцев" зарегистрированного пользователя'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) >= 0


def test_create_pet_simple_successfully(name="Пушок", animal_type="кот", age="4"):
    '''Test 6: Проверка метода простого добавления питомца (без фото) с валидными данными'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_add_photo_to_pet_with_valid_data(pet_photo="images/cat.jpeg"):
    '''Test 7: Проверка метода добавления фото к существующему питомцу с валидными данными'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.create_pet_simple(auth_key, "Boris", "Cat", "3")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_to_pet(auth_key, pet_id, pet_photo)

    assert status == 200
    assert result['pet_photo'] is not None


def test_create_pet_simple_wrong_age(name="Bob", animal_type="hamster", age="очень мало"):
    '''Test 8: Добавление питомца (без фото) с неверно написанным возрастом.
    Баг. Должен быть негативный результат, потому что возраст должен быть введен числом.'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['age'] == age


def test_post_new_pet_with_invalid_photo(name="Текст", animal_type="текстовый файл",
                                      age='5 мин', pet_photo="images/photo.txt"):
    '''Test 9: Добавления питомца с текстовым файлом вместо фото.
    Баг. Должен быть негативный результат, потому что в качестве фото должен быть
    файл в формате JPG, JPEG, PNG.'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['pet_photo'] is not None


def test_create_pet_simple_invalid_data(name="", animal_type="", age=""):
    '''Test 10: Проверка метода простого добавления питомца (без фото) с пустыми полями.
    Баг. Должен быть негативный результат, потому что заполнение данных полей обязательно.'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


