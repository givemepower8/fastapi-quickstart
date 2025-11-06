"""FastAPI web application.

This module provides a FastAPI application with routes for serving
HTML pages, handling form submissions, and serving static files.
"""
from fastapi import FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Serve the index page.
    
    Args:
        request: The FastAPI request object.
        
    Returns:
        HTMLResponse: The rendered index.html template.
    """
    print('Request for index page received')
    return templates.TemplateResponse('index.html', {"request": request})

@app.get('/favicon.ico')
async def favicon():
    """Serve the favicon.ico file.
    
    Returns:
        FileResponse: The favicon.ico file from the static directory.
    """
    file_name = 'favicon.ico'
    file_path = './static/' + file_name
    return FileResponse(path=file_path, headers={'mimetype': 'image/vnd.microsoft.icon'})

@app.post('/hello', response_class=HTMLResponse)
async def hello(request: Request, name: str = Form(...)):
    """Handle form submission and display hello page.
    
    Args:
        request: The FastAPI request object.
        name: The name submitted via form (required).
        
    Returns:
        HTMLResponse: The rendered hello.html template with the name.
        RedirectResponse: Redirects to index page if name is empty or blank.
    """
    if name:
        print(f'Request for hello page received with name={name}')
        return templates.TemplateResponse('hello.html', {"request": request, 'name': name})
    print('Request for hello page received with no name or blank name -- redirecting')
    return RedirectResponse(request.url_for("index"), status_code=status.HTTP_302_FOUND)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)
    