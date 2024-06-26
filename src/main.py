import os
import uuid

from fastapi import FastAPI, UploadFile

from src.segment_model import get_point_by_image

app = FastAPI()


@app.post("/upload-file/")
async def create_upload_file(file: UploadFile):
    try:
        bytes_io = await file.read()
        filename = f"{file.filename}_{uuid.uuid4()}.{file.content_type.split('/')[1]}"
        project_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(project_dir, filename)
        with open(file_path, "wb") as f:
            f.write(bytes_io)
        points = get_point_by_image(file_path)
        os.remove(file_path)
        return {"coordinates": points}

    except Exception as e:
        return {"error": str(e)}
