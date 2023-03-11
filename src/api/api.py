import json

from typing import List, Optional
from src import cruds

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from src import cruds
from src.database import get_db
from src.schemas.schemas import *

from src.ngrok.settings import setup_ngrok


from time import sleep
from selenium import webdriver
# seleniumが最新版なら必要
#from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import requests
import json
import os
from dotenv import load_dotenv


settings = setup_ngrok()

router = APIRouter()

@router.get('/{post_url}')
def result(post_url):
    driver_path = "/Users/hamusuta/dev/HACKATHON/chromedriver_mac_arm64/chromedriver"

    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service)

    driver.get(post_url)

    sleep(12)

    try:
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

        # imgをリスト化
        for j in img:
            srcset = j.get_attribute('srcset')
            img_url = srcset[:srcset.find(" 640w,https://")]
            images.append(img_url)

    except Exception:
        raise HTTPException(status_code=404, detail='faild')

    load_dotenv() #.envファイルの内容を読み込む

    #サブスクリプションキー
    #subscription_key = ""
    subscription_key = os.environ['Azure_COGNITIVECOGNITO2_SUBSC_KEY']
    #エンドポイント
    endpoint = "https://cognitive-cognito2.cognitiveservices.azure.com/"
    #リクエストURL
    request_describe_url = endpoint + "/vision/v3.2/describe?language=ja&model-version=latest"
    #リクエストURL
    request_tag_url = endpoint + "/vision/v3.2/tag?language=ja&model-version=latest"
    #リクエストヘッダー(画像URLの場合)
    headers = {"Ocp-Apim-Subscription-Key": subscription_key,"Content-Type": "application/json"}

    for img in images:
        #リクエストボディ
        body = {"url": img}

        #実行
        response = requests.post(request_describe_url, headers=headers, json=body)
        del response[0]
        response.append(requests.post(request_tag_url, headers=headers, json=body))

        #json化
        result = response.json()

        return result


# 以下テンプレ

# @router.get('/bootup')
# def index():
#     json_data = cruds.bootup.index()
#     if not json_data:
#         raise HTTPException(status_code=405, detail='Todo not found')
#     return json_data

# @router.post('/login')
# def login(login: Login, db: Session = Depends(get_db)):
#     json_data = cruds.login.login(db, login=login)
#     if not json_data:
#         raise HTTPException(status_code=404, detail='Account not found')
#     return {"message": "successed"}

# @router.post('/signup')
# def signup(signup: Signup, db: Session = Depends(get_db)):
#     json_data = cruds.signup.signup(db, signup=signup)
#     if not json_data:
#         raise HTTPException(status_code=404, detail='Todo not found')
#     return json_data

# @router.get('/todo', response_model=List[TodoModel])
# def index(limit: Optional[int] = 100, db: Session = Depends(get_db)):
#     json_data = cruds.todo.index(db, limit=limit)
#     if not json_data:
#         raise HTTPException(status_code=404, detail='Todo not found')
#     return json_data

# @router.post('/todo')
# def create(todo: TodoCreate, db: Session = Depends(get_db)):
#     json_data = cruds.todo.create(db, todo=todo)
#     if not json_data:
#         raise HTTPException(status_code=404, detail='Todo not found')
#     return {"message": "successed"}

# @router.patch('/todo/{target_id}')
# def update(target_id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
#     json_data = cruds.todo.update(db, todo=todo)
#     if not json_data:
#         raise HTTPException(status_code=404, detail='Todo not found')
#     return {"message": "successed", "id": target_id}

# @router.delete('/todo/{target_id}')
# def delete(target_id: int, db: Session = Depends(get_db)):
#     json_data = cruds.todo.delete(db, target_id=target_id)
#     if not json_data:
#         raise HTTPException(status_code=404, detail='Todo not found')
#     return {"message": "successed"}

# @router.get('/user/{email}', response_model=UserModel)
# def show(email: str, db: Session = Depends(get_db)):
#     json_data = cruds.user.show(db, email=email)
#     if not json_data:
#         raise HTTPException(status_code=404, detail='Todo not found')
#     return {"email":email, "todos": json_data}

# @router.post('/ml', response_model=MlResponse)
# def ml(data: MlData):
#     json_data = cruds.ml.ml(data=data)
#     if not json_data:
#         raise HTTPException(status_code=405, detail='Todo not found')
#     return json_data

# @router.post('/ml_fundamental', response_model=MlFundamentalResponse)
# def ml(data: MlFundamentalModel):
#     json_data = cruds.ml_fundamental.ml(data=data)
#     if not json_data:
#         raise HTTPException(status_code=405, detail='Appropriate Data is Not Provided')
#     return json_data
