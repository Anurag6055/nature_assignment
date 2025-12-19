from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from . import database, schemas, config, helpers

app = FastAPI(title="URL Shortner")

def get_db():
    db = database.Session_local()
    try:
        yield db
    finally:
        db.close()
    return


@app.post("/shorten", status_code=status.HTTP_201_CREATED)
def shorten_url(payload: schemas.URLCreate, db: Session = Depends(get_db)):
    url_item, error = helpers.create_short_url(
        db = db,
        long_url = str(payload.url),
        alias = payload.custom_alias,
        expiry = payload.expires_in_seconds
    )

    if error:
        raise HTTPException(status_code=400, detail=error)
    
    return {"Code": url_item.short_code}

@app.get("/code")
def redirect_to_long_url(code: str, db: Session = Depends(get_db)):
    record = db.query(database.URLItem).filter_by(short_code=code).first()

    if not record:
        raise HTTPException(status_code = 404, detail = "No URL found for the code provided.")
    
    if record.expires_at and record.expires_at < record.created_at.utcnow():
        raise HTTPException(status_code=410, detail = "Code has been expired")
    
    record.access_count += 1
    record.last_accessed = record.created_at.utcnow()

    db.commit()

    return RedirectResponse(url=record.long_url, status_code=status.HTTP_302_FOUND)