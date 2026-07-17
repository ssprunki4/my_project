from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from models import GuideORM, CategoryORM
from database import get_db
from schemas.guides import GuideCreate, GuideUpdate
from schemas.guides import GuideResponse
router = APIRouter(
    prefix="/guides",
    tags=["guides"],
)

@router.get('/all', include_in_schema=False, response_model=list[GuideResponse])
async def get_guides(db:AsyncSession = Depends(get_db)):
    guica = select(GuideORM).options(joinedload(GuideORM.category))
    result = await db.execute(guica)
    guides = result.scalars().all()
    return guides


@router.get('/by-category/{category_id}', response_model = list[GuideResponse])
async def get_guides_by_category(category_id: str, db:AsyncSession = Depends(get_db)):
    op1 = select(GuideORM).options(joinedload(GuideORM.category)).where(GuideORM.category_id == category_id)
    result = await db.execute(op1)
    guides_by_category = result.scalars().all()
    return guides_by_category


@router.post('', response_model = GuideCreate, status_code=201)
async def create_guide(create_guide: GuideCreate, db:AsyncSession = Depends(get_db)):
    result = await db.execute(select(CategoryORM).where(CategoryORM.id == create_guide.category_id))
    category_info = result.scalar_one_or_none()
    if not category_info:
        raise HTTPException(status_code=404, detail='Выбранной категории не существует')
    db_guide = GuideORM(
        name=create_guide.name,
        url=create_guide.url,
        category_id=create_guide.category_id,
    )
    db.add(db_guide)
    await db.commit()
    await db.refresh(db_guide)
    return db_guide

@router.patch('/{guide_id}', response_model=GuideResponse)
async def update_guide(guide_id: str, update_guide: GuideUpdate, db:AsyncSession = Depends(get_db)):
    result = await db.execute(select(GuideORM).where(GuideORM.id == guide_id))
    guide = result.scalar_one_or_none()
    if not guide:
        raise HTTPException(status_code=404, detail='Гайд не найден')
    if update_guide.name is not None:
        guide.name = update_guide.name
    if update_guide.url is not None:
        guide.url = update_guide.url
    if update_guide.category_id is not None:
        result = await db.execute(select(CategoryORM).where(CategoryORM.id == update_guide.category_id))
        category_exists = result.scalar_one_or_none()
        if not category_exists:
            raise HTTPException(status_code=404, detail='Категория не обнаружена')
        guide.category_id = update_guide.category_id
    await db.commit()
    await db.refresh(guide)
    return guide

@router.delete('/{guide_id}')
async def delete_guide(guide_id: str, db:AsyncSession = Depends(get_db)):
    result = await db.execute(select(GuideORM).where(GuideORM.id == guide_id))
    guide = result.scalar_one_or_none()
    if not guide:
        raise HTTPException(status_code=404, detail='Не найдено')
    guide.name = guide.name
    await db.delete(guide)
    await db.commit()
    return {'detail': f' "{guide.name}" был удален'}