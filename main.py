from fastapi import FastAPI, Request, UploadFile, HTTPException, status
from fastapi.responses import HTMLResponse
import aiofiles
from pdftools import *
from classobjects import PDF 
pdf=PDF()

app = FastAPI()

# Use a template engine like Jinja2 for more complex HTML forms
# (This approach avoids escaping HTML in Python string literals)

# @app.get('/')
# async def render_template(request: Request):
#     return TemplateResponse('index.html', {'request': request})

# Alternatively, serve the raw HTML

# @app.get('/')
# async def main():
#     return HTMLResponse(open('index.html', 'r').read())  # Read HTML from file

# @app.post('/upload')
# async def upload(file: UploadFile):
#     try:
#         contents = await file.read()
#         async with aiofiles.open(file.filename, 'wb') as f:
#             await f.write(contents)
#     except Exception:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail='There was an error uploading the file',
#         )
#     finally:
#         await file.close()
        

#     return {'message': f'Successfully uploaded {file.filename}'}

app = FastAPI()


MAX_FILE_SIZE = 1024 * 1024 * 12  # 12MB 
@app.post('/extract-text')
async def extract_texts(file: UploadFile ):
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File is too large")
    pdf_bytes = await file.read()

    # Optionally save the PDF temporarily
    with open('temp_pdf.pdf', 'wb') as f:
        f.write(pdf_bytes)

    pdf.textdata = clean_text(read_pdf('temp_pdf.pdf'))  # Replace with your program's function
    # pdf_title = pdftitle.get_title_from_file('temp_pdf.pdf')
    # author = pdfplumber.open('temp_pdf.pdf').metadata['Author']
    # presentation.author = author
    # presentation.title = pdf_title
    # return {'title':presentation.title,'textdata':pdf.textdata}
    return {'textdata':pdf.textdata}




# Run the FastAPI application
if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='127.0.0.1', port=8000)