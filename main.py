import logging


from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import  FileResponse
from starlette.staticfiles import StaticFiles

from domain.answer import  answer_router
from domain.question import question_router
from domain.user import user_router
from domain.ai import  openapi_router
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

app = FastAPI()

origins = ["http://127.0.0.1:5173",
           # 또는 "http://localhost:5173"
]

app.add_middleware(CORSMiddleware,
                #    allow_origins=origins,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )

# @app.get("/hello")
# def hello():
#     return {"message": "안녕하세요 파이보"}

logging.basicConfig(level=logging.DEBUG)

app.include_router(question_router.router)
app.include_router(answer_router.router)
app.include_router(user_router.router)
app.include_router(openapi_router.router)


@app.get("/items/{item_id}")
async def read_item(item_id : int):
    return {"item_id": item_id}

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
@app.get("/items_get/")
async def read_item_get(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

app.mount("/assets", StaticFiles(directory="frontend/dist/assets") )
#app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")
@app.get("/")
def index():
    return FileResponse("frontend/dist/index.html")

