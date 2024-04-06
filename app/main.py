from typing import Annotated

from fastapi import FastAPI, File, UploadFile
from io import BytesIO
import os
import uuid

app = FastAPI()

mock_result = {"coordinates":[{"x":10,"y":20},{"x":30,"y":40}]}
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    try:
        bytes_io = await file.read()
        filename = f"{file.filename}_{uuid.uuid4()}.{file.content_type.split('/')[1]}"
        project_dir = os.path.dirname(os.path.abspath(__file__))
        print(project_dir)
        with open(os.path.join(project_dir, "pics", filename), "wb") as f:
            f.write(bytes_io)

        return mock_result

    except Exception as e:
        return {"error": str(e)}

