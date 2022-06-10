from typing import Optional

from fastapi import File, UploadFile, APIRouter, HTTPException, Depends, Form

from app.db.crud import update_user
from app.s3.actions import upload_file_to_bucket, create_url
from app.schemas.documents import DocType, Document
from app.schemas.user import UserInDB
from app.services.token import get_current_user

router = APIRouter(
    prefix="/docs",
    tags=["docs"],
)


@router.post("/", status_code=201)
async def create_upload_file(current_user: UserInDB = Depends(get_current_user), doc_type: DocType = Form(...),
                             upload_file: UploadFile = File(...), comment: Optional[str] = Form(None)):
    id_user = current_user.id
    bucket = 'backend.documents'
    result = upload_file_to_bucket(upload_file, bucket, doc_type.value, id_user)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to upload in S3")
    else:
        new_doc_model = Document(file_name=result, type=doc_type, comment=comment)
        current_user.docs.append(new_doc_model)
        update_user(current_user.id, current_user.dict())


@router.get('/')
def download_file(doc_type: DocType, current_user: UserInDB = Depends(get_current_user)):
    file_type = doc_type.value
    current_user = current_user.dict()
    docs = current_user['docs']
    for i in range(len(docs) - 1, -1, -1):
        doc = docs[i]
        if doc['type'] == file_type:
            file_name = doc['file_name']
            url = create_url(file_name, 3600)
            return {'docUrl': url}
    return {}


@router.get('/status')
def get_status(doc_type: DocType, current_user: UserInDB = Depends(get_current_user)):
    file_type = doc_type.value
    current_user = current_user.dict()
    docs = current_user['docs']
    result = {}
    for i in range(len(docs) - 1, -1, -1):
        doc = docs[i]
        if doc['type'] == file_type:
            result['status'] = doc['status']
            result['dateEnd'] = doc['dateEnd']
            result['dateStart'] = doc['dateStart']
            return result
    return result


@router.get('/templates')
def download_templates():
    nda_url = create_url('/templates/nda.txt', 3600)
    instruction_url = create_url('/templates/instruction.txt', 3600)
    template_url = create_url('/templates/template.txt', 3600)
    return {'nda_url': nda_url,
            'instruction_url': instruction_url,
            'template_url': template_url
            }
