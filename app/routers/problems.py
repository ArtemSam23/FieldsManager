from fastapi import APIRouter, Depends
from app.services.token import get_current_user
from app.db.crud import create_problem, update_problem_count, get_problem, update_user
from app.schemas.field_problems import Problem, ProblemCreate
from app.schemas.user import UserInDB

router = APIRouter(
    prefix="/problems",
    tags=["problems"],
)


@router.get('/')
async def get_problems(current_user: UserInDB = Depends(get_current_user)):
    problems = current_user.problems
    list_problems = []
    for problem in problems:
        problem_db = get_problem(problem)
        list_problems.append(problem_db)
    return {'problems': list_problems}


@router.post('/')
async def post_problem(problem: Problem, current_user: UserInDB = Depends(get_current_user)):
    problem = ProblemCreate(**problem.dict())
    create_problem(problem)
    current_user.problems.append(problem.id)
    update_user(current_user.id, current_user.dict())
    for field in problem.fieldsId:
        update_problem_count(field)
