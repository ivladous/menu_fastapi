from tests.conftest import test_client, prefix


def test_read_menus_handler():
    response = test_client.get(prefix+'/menus/')
    assert response.status_code == 200
    assert response.json() == []


def test_read_inexistent_menu():
    response = test_client.get(prefix+'/menus/1101')
    assert response.status_code == 404
    assert response.json() == {"detail": "menu not found"}


def test_create_menu_handler():
    menu_title: str = "Menu title"
    menu_description: str = "Menu description"
    json = {"title": menu_title, "description": menu_description}
    response = test_client.post(prefix+'/menus/', json=json)
    data = response.json()
    assert response.status_code == 201
    assert data['title'] == menu_title
    assert data['description'] == menu_description
    assert data['dishes_count'] == 0
    menu_id = response.json()['id']

    response = test_client.get(prefix + f'/menus/{menu_id}')
    data = response.json()
    assert response.status_code == 200
    assert data['title'] == menu_title
    assert data['description'] == menu_description
    assert data['dishes_count'] == 0

    response = test_client.delete(prefix + f'/menus/{menu_id}')
    data = response.json()
    assert response.status_code == 200
    assert data['status'] == True
    assert data['message'] == 'The menu has been deleted'



