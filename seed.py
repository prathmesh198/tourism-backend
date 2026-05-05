import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import Destination

def seed():
    destinations = [
        {"name": "Taj Mahal", "location": "Agra, Uttar Pradesh", "description": "An ivory-white marble mausoleum on the right bank of the river Yamuna.", "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Taj_Mahal_in_March_2004.jpg/1200px-Taj_Mahal_in_March_2004.jpg"},
        {"name": "Jaipur City Palace", "location": "Jaipur, Rajasthan", "description": "A palace complex in Jaipur.", "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/City_Palace_Jaipur_1.jpg/1200px-City_Palace_Jaipur_1.jpg"},
        {"name": "Kerala Backwaters", "location": "Kerala", "description": "A network of brackish lagoons and lakes lying parallel to the Arabian Sea coast.", "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Houseboat_in_Kerala.jpg/1200px-Houseboat_in_Kerala.jpg"},
        {"name": "Varanasi Ghats", "location": "Varanasi, Uttar Pradesh", "description": "Riverfront steps leading to the banks of the River Ganges.", "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Ahilya_Ghat_by_the_Ganges%2C_Varanasi.jpg/1200px-Ahilya_Ghat_by_the_Ganges%2C_Varanasi.jpg"}
    ]
    
    for dest in destinations:
        Destination.objects.get_or_create(name=dest['name'], defaults=dest)
        
    print("Database seeded with sample destinations.")

if __name__ == '__main__':
    seed()
