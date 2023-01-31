from fastapi import FastAPI

from app.api.api_v1.api import api_router

description = """
RestaurantMenu API helps you to create, read and update menus, submenus and dishes in your restaurant 🍽

## Menus

You can:
* **read all menus**;
* **read certain menu by its id**;
* **create new menu**;
* **update menu**;
* **delete menu**;


## Submenus

Submenu is attached to the menu. You can:
* **read all submenus**;
* **read certain submenu by its id**;
* **create new submenu**;
* **update submenu**;
* **delete submenu**;


## Dishes

Dish is attached to the submenu. You can:
* **read all dishes**;
* **read certain dish by its id**;
* **create new dish**;
* **update dish**;
* **delete dish**.
"""

app = FastAPI(description=description)

app.include_router(api_router, prefix='/api/v1')
