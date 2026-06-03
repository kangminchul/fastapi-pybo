from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from domain.ai import  openapi_schema

# open api 사용
from dotenv import load_dotenv
from openai import OpenAI
from database import get_db
import base64
import logging


load_dotenv()
client = OpenAI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

image_path = "./src/boardwalk.jpg"
base64_image = encode_image(image_path)

router = APIRouter(
    prefix="/api/ai",
)


@router.post("/kakao")
async def kakao(request: Request):
    logger.info(f"+++++++++++ 데이터가 안 찍힌다고 ")
    print("데이터야 찍혀라" )
    try:
        req_data = await request.json()
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="JSON 데이터가 없습니다."
        )
    #utterance =  req_data['userRequest']['utterance']
    logger.info(f"request={req_data}")
    return {"content": "안녕"}


@router.post("/openapi", response_model=openapi_schema.OpenAPISchema)
def openapi_question( param:openapi_schema.OpenAPIParamSchema, db: Session = Depends(get_db)):
    print("param.type:" + param.type)
    if param.type == 'NQ':
        print("NQ:" + param.content)
        response = client.responses.create(
            model="gpt-4o",
            instructions="요청한 문장을 영어로 번역 해줘. 그리고 영어 문장만 답해 줘.",
            input=[
                {
                    "role": "user",
                    "content": param.content
                }
            ]
        )
        answer = response.output[0].content[0].text
        print(response.output_text)
        return {
            "openapi": answer
        }
    elif param.type == 'VQB':
        response  = client.responses.create(
            model="gpt-4o",
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": "이 이미지를 설명 해 줘."},
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    ],
                }
            ],
        )
        print(response.output_text)
        return {
            "openapi": response.output_text
        }
    else:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": "이 이미지를 설명 해 줘."
                        },
                        {
                            "type": "input_image",
                            "image_url": "https://images.unsplash.com/photo-1506744038136-46273834b3fb"
                        }
                    ]
                }
            ]
        )
        print(response.output_text)
        return {
            "openapi": response.output_text
        }





