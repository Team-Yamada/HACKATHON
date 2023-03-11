from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from urllib import request
from PIL import Image

driver_path = "/Users/hamusuta/dev/HACKATHON/chromedriver_mac_arm64/chromedriver"

service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service)

# post = 1
# driver.get("https://instagram.com/p/Cpm53N4ybXQ/")

# post = 2
# driver.get("https://www.instagram.com/p/CgwwHqUvGz2/?igshid=YmMyMTA2M2Y=")

# post = 3
# driver.get("https://www.instagram.com/p/Cpm4Wy8voaC/?igshid=YmMyMTA2M2Y=")

# post = 4
# driver.get("https://www.instagram.com/p/CpZ96mNvM6Q/?igshid=YmMyMTA2M2Y=")

# post = 5
driver.get("https://www.instagram.com/p/CpfUL6BhCAW/?igshid=YmMyMTA2M2Y%3Dmedia%2F%3Fsize%3Dl")

# post >= 6
# driver.get("https://www.instagram.com/p/CpmkP2nJloQ/?igshid=YmMyMTA2M2Y=")

sleep(12)

try:
    # print('go')
    # # next = driver.find_element(by=By.CSS_SELECTOR, value='button')['aria-label="次へ"']
    # sleep(5)
    # next.click()
    post_size = len(driver.find_elements_by_css_selector("div._acnb"))
    
    click_count = 2 if post_size >= 3 else 1
    images = []

# 画像が複数あれば指定回数クリック
    if post_size > 1:
        next = driver.find_element_by_css_selector("button[aria-label='次へ']")
        for i in range(click_count):
            next.click()
    
    # imgのurlを取得
    img = driver.find_elements_by_css_selector("img[decoding='auto']")
    
    for j in img:
        srcset = j.get_attribute('srcset')
        img_url = srcset[:srcset.find(" 640w,https://")]
        images.append(img_url)
    
    print(images)
    print('success')
except Exception:
    print('error')



import requests
import json
import os
from dotenv import load_dotenv #キーを別ファイルで管理するため

load_dotenv() #.envファイルの内容を読み込む


#サブスクリプションキー
#subscription_key = ""
subscription_key = os.environ['Azure_COGNITIVECOGNITO2_SUBSC_KEY']
#エンドポイント
endpoint = "https://cognitive-cognito2.cognitiveservices.azure.com/"
#リクエストURL
request_url = endpoint + "/vision/v3.2/describe?language=ja&model-version=latest"
#画像のURL
img ="https://www.instagram.com/p/CpfUL6BhCAW/media/?size=l"


#リクエストヘッダー(画像URLの場合)
headers = {"Ocp-Apim-Subscription-Key": subscription_key,"Content-Type": "application/json"}
#リクエストヘッダー(画像のバイナリデータを直接送る場合)
#headers = {
#   'Content-Type': 'application/json',
#   'Ocp-Apim-SUbscription-Key': subscription_key,
#}


#リクエストボディ
body = {"url": img}


#実行
response = requests.post(request_url, headers=headers, json=body)
#response.raise_for_status()
#print(response.json())


#json化
result = response.json()
#print(json.dumps(result, indent=4,ensure_ascii=False))


description = result['description']
#tagsのみ抽出
for i in range(len(description['tags'])):
    print(description['tags'][i])

#captionのみ抽出
print('caption:' + description['captions'][0]['text'])






import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

#サブスクリプションキー
#subscription_key = ""
subscription_key = os.environ['Azure_COGNITIVECOGNITO2_SUBSC_KEY']

#エンドポイント
endpoint = "https://cognitive-cognito2.cognitiveservices.azure.com/"
#リクエストURL
request_url = endpoint + "/vision/v3.2/tag?language=ja&model-version=latest"
#画像のURL
img ="https://www.instagram.com/p/CpfUL6BhCAW/media/?size=l"


#リクエストヘッダー(画像URLの場合)
headers = {"Ocp-Apim-Subscription-Key": subscription_key,"Content-Type": "application/json"}
#リクエストヘッダー(画像のバイナリデータを直接送る場合)
#headers = {
#   'Content-Type': 'application/json',
#   'Ocp-Apim-SUbscription-Key': subscription_key,
#}

#リクエストボディ
body = {"url": img}


#実行
response = requests.post(request_url, headers=headers, json=body)
#response.raise_for_status()
#確認
#print(response.json())


#json化
result = response.json()
#print(json.dumps(result, indent=4,ensure_ascii=False))

#nameのみ抽出
tags = result['tags']
for i in tags:
    print(i['name'])
