from tests.conftest import test_client, prefix


def test_read_dishes_handler(
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
    response = test_client.get(prefix+f'/menus/{menu_id}/submenus/{submenu_id}/dishes')
    assert response.status_code == 200
    assert response.json() == []


def test_read_dish_handler(
        data_menu,
        create_menu,
        get_first_menu_id,
        data_submenu,
        create_submenu,
        get_first_submenu_id,
        data_dish,
        create_dish,
        get_first_dish_id,
):
    create_menu(**data_menu)
    menu_id = get_first_menu_id()
    data_submenu['menu_id'] = menu_id
    create_submenu(**data_submenu)
    submenu_id = get_first_submenu_id()
    data_dish['submenu_id'] = submenu_id
    create_dish(**data_dish)
    dish_id = get_first_dish_id()
    response = test_client.get(prefix + f'/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    data = response.json()
    assert response.status_code == 200
    assert data['title'] == data_dish['title']
    assert data['description'] == data_dish['description']


def test_read_inexistent_dish(
        data_menu,
        create_menu,
        get_first_menu_id,
        data_submenu,
        create_submenu,
        get_first_submenu_id,
):
    create_menu(**data_menu)
    menu_id = get_first_menu_id()
    data_submenu['menu_id'] = menu_id
    create_submenu(**data_submenu)
    submenu_id = get_first_submenu_id()
    response = test_client.get(prefix+f'/menus/{menu_id}/submenus/{submenu_id}/dishes/1')
    assert response.status_code == 404
    assert response.json() == {"detail": "dish not found"}


def test_create_dish_handler(
        data_menu,
        create_menu,
        get_first_menu_id,
        data_submenu,
        create_submenu,
        get_first_submenu_id,
        data_dish,
        create_dish
):
    create_menu(**data_menu)
    menu_id = get_first_menu_id()
    data_submenu['menu_id'] = menu_id
    create_submenu(**data_submenu)
    submenu_id = get_first_submenu_id()
    data_dish['submenu_id'] = submenu_id
    create_dish(**data_dish)
    response = test_client.post(prefix + f'/menus/{menu_id}/submenus/{submenu_id}/dishes/', json=data_dish)
    data = response.json()
    assert response.status_code == 201
    assert data['title'] == data_dish['title']
    assert data['description'] == data_dish['description']
    assert data['price'] == data_dish['price']


def test_update_dish_handler(
        data_menu,
        create_menu,
        get_first_menu_id,
        data_submenu,
        create_submenu,
        get_first_submenu_id,
        data_dish,
        create_dish,
        get_first_dish_id,
        new_data_dish

):
    create_menu(**data_menu)
    menu_id = get_first_menu_id()
    data_submenu['menu_id'] = menu_id
    create_submenu(**data_submenu)
    submenu_id = get_first_submenu_id()
    data_dish['submenu_id'] = submenu_id
    create_dish(**data_dish)
    dish_id = get_first_dish_id()
    response = test_client.patch(
        prefix + f'/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', json=new_data_dish
    )
    data = response.json()
    assert response.status_code == 200
    assert data['title'] == new_data_dish['title']
    assert data['description'] == new_data_dish['description']
    assert data['price'] == new_data_dish['price']


def delete_dish(
        data_menu,
        create_menu,
        get_first_menu_id,
        data_submenu,
        create_submenu,
        get_first_submenu_id,
        data_dish,
        create_dish,
        get_first_dish_id,
):
    create_menu(**data_menu)
    menu_id = get_first_menu_id()
    data_submenu['menu_id'] = menu_id
    create_submenu(**data_submenu)
    submenu_id = get_first_submenu_id()
    data_dish['submenu_id'] = submenu_id
    create_dish(**data_dish)
    dish_id = get_first_dish_id()
    response = test_client.delete(prefix + f'/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    data = response.json()
    assert response.status_code == 200
    assert data['status'] is True
    assert data['message'] == 'The dish has been deleted'
