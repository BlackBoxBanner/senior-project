from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/603010")
async def upload_image(file: UploadFile = File(...)):
    contents = await file.read()
    # You can save the file or process it here
    return JSONResponse(
        content={"filename": file.filename, "content_type": file.content_type}
    )
