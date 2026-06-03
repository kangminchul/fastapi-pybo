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


def generate_response_from_openai(query: str) -> str:
    response = client.responses.create(
        model="gpt-4o",
        input=[
            {
                "role": "user",
                "content": query
            }
        ]
    )
    return response.output_text


@router.post("/kakao")
async def kakao(request: Request):
    print("req_data:" )
    try:
        req_data = await request.json()
        query = req_data['userRequest']['utterance']
        if not query:
            raise HTTPException(status_code=400, detail="Query is missing")
        content = generate_response_from_openai(query)
        return {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": content
                        }
                    }
                ]
            }
        }
#        logger.info("req_data:" + req_data)
#        print("req_data:" + req_data )
    except Exception as e:
        logger.info(f"kakao error ={str(e)}")
        return {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": f"Error: {str(e)}"
                        }
                    }
                ]
            }
        }


#    return {"content": "안녕"}


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





