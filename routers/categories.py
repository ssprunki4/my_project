from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas.categories import CategoryCreate, CategoryResponse, CategoryUpdate
from sqlalchemy import select, delete
from models import CategoryORM

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)

@router.get('', response_model = list[CategoryResponse])
async def get_categories(db:AsyncSession = Depends(get_db)):
    result = await db.execute(select(CategoryORM))
    categories = result.scalars().all()
    return categories

@router.post('', response_model = CategoryResponse)
async def create_category(category: CategoryCreate, db:AsyncSession = Depends(get_db)):
    db_obj = CategoryORM(name = category.name)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj
@router.patch('', status_code=201)
async def update_category(category_id: str, category_data: CategoryUpdate, db:AsyncSession = Depends(get_db)):
    result = await db.execute(select(CategoryORM).where(CategoryORM.id == category_id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail='Выбранная категория не найдена')
    if category_data.name is not None:
        category.name = category_data.name
    await db.commit()
    await db.refresh(category)
    return category


@router.delete('/{category_id}')
async def delete_category(category_id: str, db:AsyncSession = Depends(get_db)):
    result = await db.execute(select(CategoryORM).where(CategoryORM.id == category_id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    await db.execute(delete(CategoryORM).where(CategoryORM.id == category_id))
    await db.commit()
    return {'detail': f'Категория {category.name} и все гайды внутри удалены'}
