from tests.conftest import test_client, prefix


def test_read_submenus_handler(data_menu, create_menu, get_first_menu_id):
    create_menu(**data_menu)
    menu_id = get_first_menu_id()
    response = test_client.get(prefix+f'/menus/{menu_id}/submenus')
    assert response.status_code == 200
    assert response.json() == []


def test_read_submenu_handler(
        data_menu,
        create_menu,
        get_first_menu_id,
        data_submenu,
        create_submenu,
        get_first_submenu_id
):
    create_menu(**data_menu)
    menu_id = get_first_menu_id()
    data_submenu['menu_id'] = menu_id
    create_submenu(**data_submenu)
    submenu_id = get_first_submenu_id()
    response = test_client.get(prefix + f'/menus/{menu_id}/submenus/{submenu_id}')
    data = response.json()
    assert response.status_code == 200
    assert data['title'] == data_submenu['title']
    assert data['description'] == data_submenu['description']
    assert data['dishes_count'] == 0


def test_read_inexistent_submenu(data_menu, create_menu, get_first_menu_id):
    create_menu(**data_menu)
    menu_id = get_first_menu_id()
    response = test_client.get(prefix+f'/menus/{menu_id}/submenus/1')
    assert response.status_code == 404
    assert response.json() == {"detail": "submenu not found"}


def test_create_submenu_handler(data_menu, create_menu, get_first_menu_id, data_submenu):
    create_menu(**data_menu)
    menu_id = get_first_menu_id()
    data_submenu['menu_id'] = menu_id
    response = test_client.post(prefix + f'/menus/{menu_id}/submenus', json=data_submenu)
    data = response.json()
    assert response.status_code == 201
    assert data['title'] == data_submenu['title']
    assert data['description'] == data_submenu['description']
    assert data['dishes_count'] == 0


def delete_submenu(data_menu, create_menu, get_first_menu_id, data_submenu):
    create_menu(**data_menu)
    menu_id = get_first_menu_id()
    data_submenu = data_submenu.update({'menu_id': menu_id})
    response = test_client.post(prefix + f'/menus/{menu_id}/submenus', json=data_submenu)
    data = response.json()
    submenu_id = data['id']
    response = test_client.delete(prefix + f'/menus/{menu_id}/submenus/{submenu_id}')
    data = response.json()
    assert response.status_code == 200
    assert data['status'] is True
    assert data['message'] == 'The submenu has been deleted'


def test_update_submenu(
        data_menu,
        create_menu,
        get_first_menu_id,
        data_submenu,
        create_submenu,
        get_first_submenu_id,
        new_data_submenu
):
    create_menu(**data_menu)
    menu_id = get_first_menu_id()
    data_submenu['menu_id'] = menu_id
    create_submenu(**data_submenu)
    submenu_id = get_first_submenu_id()
    response = test_client.patch(prefix + f'/menus/{menu_id}/submenus/{submenu_id}', json=new_data_submenu)
    data = response.json()
    assert response.status_code == 200
    assert data['title'] == new_data_submenu['title']
    assert data['description'] == new_data_submenu['description']
    assert data['dishes_count'] == 0
