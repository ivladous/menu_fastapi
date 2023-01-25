from tests.conftest import test_client, prefix


def test_read_menus_handler():
    response = test_client.get(prefix+'/menus/')
    assert response.status_code == 200
    assert response.json() == []


def test_read_menu_handler(data_menu, create_menu, get_first_menu_id):
    create_menu(**data_menu)
    menu_id = get_first_menu_id()
    response = test_client.get(prefix + f'/menus/{menu_id}')
    data = response.json()
    assert response.status_code == 200
    assert data['title'] == data_menu['title']
    assert data['description'] == data_menu['description']
    assert data['dishes_count'] == 0
    assert data['submenus_count'] == 0


def test_read_inexistent_menu():
    response = test_client.get(prefix+'/menus/1')
    assert response.status_code == 404
    assert response.json() == {"detail": "menu not found"}


def test_create_menu_handler(data_menu):
    response = test_client.post(prefix+'/menus/', json=data_menu)
    data = response.json()
    assert response.status_code == 201
    assert data['title'] == data_menu['title']
    assert data['description'] == data_menu['description']
    assert data['submenus_count'] == 0
    assert data['dishes_count'] == 0


def test_delete_menu(data_menu, create_menu, get_first_menu_id):
    create_menu(**data_menu)
    menu_id = get_first_menu_id()
    response = test_client.delete(prefix + f'/menus/{menu_id}')
    data = response.json()
    assert response.status_code == 200
    assert data['status'] is True
    assert data['message'] == 'The menu has been deleted'


def test_update_menu(data_menu, new_data_menu, create_menu, get_first_menu_id):
    create_menu(**data_menu)
    menu_id = get_first_menu_id()
    response = test_client.patch(prefix + f'/menus/{menu_id}', json=new_data_menu)
    data = response.json()
    assert response.status_code == 200
    assert data['title'] == new_data_menu['title']
    assert data['description'] == new_data_menu['description']
    assert data['submenus_count'] == 0
    assert data['dishes_count'] == 0
