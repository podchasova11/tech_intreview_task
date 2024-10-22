Конечно! Я внесу дополнительные правки, чтобы улучшить обработку ошибок, структуру и безопасность токена. Вот обновленный код:

```pythonimport randomimport pytestimport requestsimport osclass YaUploader:
 def __init__(self, token):
 self.token = token self.headers = {
 'Content-Type': 'application/json',
 'Accept': 'application/json',
 'Authorization': f'OAuth {self.token}'
 }

 def create_folder(self, path):
 url_create = 'https://cloud-api.yandex.net/v1/disk/resources'
 response = requests.put(f'{url_create}?path={path}', headers=self.headers)
 if response.status_code not in [201,409]: #201 - создано,409 - уже существует raise Exception(f"Error creating folder: {response.json()}")

 def upload_photos_to_yd(self, path, url_file, name):
 url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
 params = {"path": f'/{path}/{name}', 'url': url_file, "overwrite": "true"}
 resp = requests.post(url, headers=self.headers, params=params)
 if resp.status_code !=202:
 raise Exception(f"Error uploading file: {resp.json()}")


def get_sub_breeds(breed):
 res = requests.get(f'https://dog.ceo/api/breed/{breed}/list')
 if res.status_code !=200:
 raise Exception(f"Error fetching sub-breeds: {res.json()}")
 return res.json().get('message', [])


def get_urls(breed, sub_breeds):
 url_images = []
 if sub_breeds:
 for sub_breed in sub_breeds:
 res = requests.get(f"https://dog.ceo/api/breed/{breed}/{sub_breed}/images/random")
 if res.status_code ==200:
 url_images.append(res.json().get('message'))
 else:
 print(f"Error fetching image for {sub_breed}: {res.json()}")
 else:
 res = requests.get(f"https://dog.ceo/api/breed/{breed}/images/random")
 if res.status_code ==200:
 url_images.append(res.json().get('message'))
 else:
 raise Exception(f"Error fetching image for {breed}: {res.json()}")
 return url_imagesdef upload_breed_images(breed):
 sub_breeds = get_sub_breeds(breed)
 urls = get_urls(breed, sub_breeds)

 if not urls:
 print(f"No images found for breed: {breed}")
 return token = os.getenv('YANDEX_TOKEN') # Чтение токена из переменной окружения yandex_client = YaUploader(token)
 yandex_client.create_folder('test_folder')

 for url in urls:
 if url: # Проверка, что URL не пустой part_name = url.split('/')
 name = '_'.join([part_name[-2], part_name[-1]])
 yandex_client.upload_photos_to_yd("test_folder", url, name)


@pytest.mark.parametrize('breed', ['doberman', random.choice(['bulldog', 'collie'])])
def test_upload_dog(breed):
 try:
 upload_breed_images(breed)
 # Проверка существования директории и загруженных изображений url_create = 'https://cloud-api.yandex.net/v1/disk/resources'
 token = os.getenv('YANDEX_TOKEN')
 headers = {
 'Content-Type': 'application/json',
 'Accept': 'application/json',
 'Authorization': f'OAuth {token}'
 }

 response = requests.get(f'{url_create}?path=/test_folder', headers=headers)
 response.raise_for_status() # Проверка на ошибки HTTP data = response.json()

 assert data['type'] == "dir"
 assert data['name'] == "test_folder"

 items = data.get('_embedded', {}).get('items', [])
 assert len(items) == len(get_sub_breeds(breed)) if get_sub_breeds(breed) else1 for item in items:
 assert item['type'] == 'file'
 assert item['name'].startswith(breed)
 except Exception as e:
 pytest.fail(f"Test failed due to errors: {e}")

```

### Основные изменения:

# 1. **Обработка ошибок при запросах**: Добавлены проверки статуса ответа на запросы, чтобы обработать возможные ошибки при получении данных о подпородах и изображениях.

# 2. **Проверка на пустые URL**: Перед попыткой загрузки изображений проверяется, что URL не пустой.

# 3. **Безопасность токена**: Токен загружается из переменной окружения `YANDEX_TOKEN`, что обеспечивает безопасность.

# 4. **Обработка исключений в тестах**: Весь блок логики тестирования обернут в блок `try...except`, чтобы все возможные ошибки были ловлены и выводились в виде сообщения об ошибке теста.

# 5. **Сообщения об ошибках**: Добавлено больше информации об ошибках для лучшей диагностики.

# Эти доработки улучшат структуру кода, сделают его более надежным и безопасным, особенно в контексте работы с внешними API.
