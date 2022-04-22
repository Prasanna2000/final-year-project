from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time

PATH = "chromedriver.exe"

# wd stands for web driver
wd = webdriver.Chrome(PATH)


def get_images_from_google(wd, delay, max_images):

    count = 0

    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

    url = "https://www.google.com/search?q=forest+fire+drone+view&tbm=isch&ved=2ahUKEwjTvP6L-Kf3AhWik9gFHYTZAfQQ2-cCegQIABAA&oq=forest+fire+drone+&gs_lcp=CgNpbWcQARgBMgcIIxDvAxAnMgUIABCABDIECAAQHjIGCAAQCBAeMgQIABAYUM0GWM0GYOYOaABwAHgAgAF-iAH8AZIBAzAuMpgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=XMNiYtOeNKKn4t4PhLOHoA8&bih=714&biw=1536&rlz=1C1CHZN_enIN961IN961"
    wd.get(url)

    image_urls = set()

    while len(image_urls) < max_images:
        scroll_down(wd)

        thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

        for img in thumbnails[len(image_urls): max_images]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue

            images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
            for img in images:
                if img.get_attribute("src") and "http" in img.get_attribute("src"):
                    image_urls.add(img.get_attribute("src"))
                    print(f"Found image! count:{count+1}")
                    count += 1
    return image_urls


def download_image(download_path, url, file_name):
    count = 0
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, 'wb') as f:
            image.save(f, "JPEG")
        print(f"Download Success {count}")
        count += 1

    except Exception as e:
        print("Failed to download ", e)


# download it step by step (if lot of images are downloaded at the same time google will block ip)
img_urls = get_images_from_google(wd, 2, 10)
for i, url in enumerate(img_urls):
    download_image("images/fire/", url, f"fire_{i}.jpg")

wd.quit()
