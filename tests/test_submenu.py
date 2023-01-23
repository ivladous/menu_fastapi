from tests.conftest import test_client, prefix


def test_create_submenu_handler():
    menu_title: str = "Menu title"
    menu_description: str = "Menu description"
    json = {"title": menu_title, "description": menu_description}
    response = test_client.post(prefix + '/menus/', json=json)
    menu_id = response.json()['id']

    json = {"title": 'submenu_title', "description": 'submenu_description'}
    response = test_client.post(prefix + f'/menus/{menu_id}/submenus', json=json)
    data = response.json()
    assert response.status_code == 201
    assert data['title'] == 'submenu_title'
    assert data['description'] == 'submenu_description'
    assert data['dishes_count'] == 0

    submenu_id = data['id']
    response = test_client.delete(prefix + f'/menus/{menu_id}/submenus/{submenu_id}')
    data = response.json()
    assert response.status_code == 200
    assert data['status'] == True
    assert data['message'] == 'The submenu has been deleted'

    test_client.delete(prefix + f'/menus/{menu_id}')
