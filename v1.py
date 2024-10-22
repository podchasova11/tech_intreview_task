 def __init__(self, token):  
 self.token = token self.headers = {  
 'Content-Type': 'application/json',  
 'Accept': 'application/json',  
 'Authorization': f'OAuth {self.token}'  
 }  

 def create_folder(self, path):  
 url_create = 'https://cloud-api.yandex.net/v1/disk/resources'  
 response = requests.put(f'{url_create}?path={path}', headers=self.headers)  
 if response.status_code !=201 and response.status_code !=409: #201,409 (folder already exists)  
 raise Exception(f"Error creating folder: {response.json()}")  

 def upload_photos_to_yd(self, path, url_file, name):  
 url = "https://cloud-api.yandex.net/v1/disk/resources/upload"  
 params = {"path": f'/{path}/{name}', 'url': url_file, "overwrite": "true"}  
 resp = requests.post(url, headers=self.headers, params=params)  
 if resp.status_code !=202:  
 raise Exception(f"Error uploading file: {resp.json()}")  


def get_sub_breeds(breed):  
 res = requests.get(f'https://dog.ceo/api/breed/{breed}/list')  
 return res.json().get('message', [])  


def get_urls(breed, sub_breeds):  
 url_images = []  
 if sub_breeds:  
 for sub_breed in sub_breeds:  
 res = requests.get(f"https://dog.ceo/api/breed/{breed}/{sub_breed}/images/random")  
 sub_breed_urls = res.json().get('message')  
 if sub_breed_urls:  
 url_images.append(sub_breed_urls)  
 else:  
 url_image = requests.get(f"https://dog.ceo/api/breed/{breed}/images/random").json().get('message')  
 if url_image:  
 url_images.append(url_image)  
 return url_imagesdef upload_breed_images(breed):  
 sub_breeds = get_sub_breeds(breed)  
 urls = get_urls(breed, sub_breeds)  
 if not urls:  
 print(f"No images found for breed: {breed}")  
 return token = os.getenv('YANDEX_TOKEN') # use an environment variable for security yandex_client = YaUploader(token)  
 yandex_client.create_folder('test_folder')  

 for url in urls:  
 part_name = url.split('/')  
 name = '_'.join([part_name[-2], part_name[-1]])  
 yandex_client.upload_photos_to_yd("test_folder", url, name)  


@pytest.mark.parametrize('breed', ['doberman', random.choice(['bulldog', 'collie'])])  
def test_upload_dog(breed):  
 upload_breed_images(breed)  
 # Checking the folder and uploaded images url_create = 'https://cloud-api.yandex.net/v1/disk/resources'  
 token = os.getenv('YANDEX_TOKEN')  
 headers = {  
 'Content-Type': 'application/json',  
 'Accept': 'application/json',  
 'Authorization': f'OAuth {token}'  
 }  
 response = requests.get(f'{url_create}?path=/test_folder', headers=headers)  
 data = response.json()  

 assert data['type'] == "dir"  
 assert data['name'] == "test_folder"  

 items = data.get('_embedded', {}).get('items', [])  
 assert len(items) == len(get_sub_breeds(breed)) if get_sub_breeds(breed) else1 for item in items:  
 assert item['type'] == 'file'  
 assert item['name'].startswith(breed)


# Изменения и улучшения:
# Обработка ошибок: При создании папки и загрузке изображений добавлена обработка ошибок, чтобы отловить и сообщить о проблемах с API.

# Безопасность токена: Токен для доступа к API теперь загружается из переменной окружения YANDEX_TOKEN, что увеличивает безопасность.

# Проверка полученных изображений: Проверяется наличие URL перед добавлением в список.

# Проверка результата: Если нет изображений для загрузки, выводится соответствующее сообщение.

# Использование методов класса: Упрощен конструктор класса YaUploader и передача токена.

# Читаемость кода: Код структурирован более логически и читаем.

# Теперь код более надежен и безопасен, что делает загрузку изображений на Яндекс.Диск более эффективной.
