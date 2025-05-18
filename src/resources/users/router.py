from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.resources.shared.schemas import PaginationParams
from src.resources.users.repository import UserRepository, get_user_repository
from src.resources.users.schema import UserCreate, UserPublic, UsersPaginatedResponse, UserUpdate

router = APIRouter(
    prefix='/users',
    tags=['users'],
    responses={
        404: {'description': 'Usuário não encontrado'},
        400: {'description': 'Dados inválidos'},
        500: {'description': 'Erro interno do servidor'},
    },
)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


@router.post(
    '',
    response_model=UserPublic,
    status_code=HTTPStatus.CREATED,
    summary='Criar novo usuário',
    description="""
    Cria um novo usuário no sistema.

    - **email**: Email único do usuário
    - **username**: Nome de usuário (3-50 caracteres, apenas letras, números, _ e -)
    - **password**: Senha (mínimo 8 caracteres, deve conter letras e números)
    - **profile**: Dados do perfil (opcional)
        - **full_name**: Nome completo (máximo 100 caracteres)
        - **linkedin_url**: URL do LinkedIn (formato: https://linkedin.com/in/username)
        - **github_url**: URL do GitHub (formato: https://github.com/username)
        - **phone_number**: Número de telefone (formato: +5511999999999)
        - **bio**: Biografia (máximo 500 caracteres)

    Retorna os dados do usuário criado, excluindo a senha.
    """,
)
async def create_user(
    user_data: UserCreate,
    repository: UserRepositoryDep,
):
    """Cria um novo usuário no sistema."""
    # Check for existing email

    existing_user = await repository.get_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with this email already exists',
        )

    # Check for existing username
    existing_username = await repository.get_by_username(user_data.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with this username already exists',
        )
    created_user = await repository.create(user_data)
    return created_user


@router.get(
    '/{user_id}',
    response_model=UserPublic,
    summary='Buscar usuário por ID',
    description="""
    Retorna os dados de um usuário específico pelo seu ID.

    - **user_id**: ID único do usuário (ULID)

    Retorna os dados do usuário, excluindo a senha.
    """,
)
async def get_user(
    user_id: str,
    repository: UserRepositoryDep,
):
    """Retorna os dados de um usuário pelo seu ID."""
    user = await repository.get_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        )

    return user


@router.patch(
    '/{user_id}',
    response_model=UserPublic,
    summary='Atualizar usuário',
    description="""
    Atualiza os dados de um usuário existente.

    - **user_id**: ID único do usuário (ULID)

    Campos que podem ser atualizados:
    - **email**: Novo email (opcional)
    - **username**: Novo nome de usuário (opcional)
    - **password**: Nova senha (opcional)
    - **is_active**: Status de ativação (opcional)
    - **profile**: Dados do perfil (opcional)

    Retorna os dados atualizados do usuário.
    """,
)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    repository: UserRepositoryDep,
):
    """Atualiza os dados de um usuário existente."""
    # Check if user exists
    user = await repository.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        )

    # Check for email uniqueness if email is being updated
    if user_data.email and user_data.email != user.email:
        existing_user = await repository.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User with this email already exists',
            )

    # Check for username uniqueness if username is being updated
    if user_data.username and user_data.username != user.username:
        existing_username = await repository.get_by_username(user_data.username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User with this username already exists',
            )

    updated_user = await repository.update(user_id, user_data)

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to update user',
        )
    return updated_user


@router.delete(
    '/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Deletar usuário',
    description="""
    Deleta um usuário existente.

    - **user_id**: ID único do usuário (ULID)

    Retorna 204 No Content em caso de sucesso.
    """,
)
async def delete_user(
    user_id: str,
    repository: UserRepositoryDep,
):
    """Deleta um usuário existente."""
    user = await repository.delete(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        )


@router.get(
    '',
    response_model=UsersPaginatedResponse,
    summary='Listar usuários',
    description="""
    Retorna uma lista paginada de usuários.

    Parâmetros de paginação:
    - **page**: Número da página (padrão: 1)
    - **per_page**: Itens por página (padrão: 10, máximo: 100)

    Retorna:
    - Lista de usuários
    - Total de usuários
    - Total de páginas
    - Página atual
    - Itens por página
    """,
)
async def list_users(
    params: Annotated[PaginationParams, Depends()],
    repository: UserRepositoryDep,
) -> UsersPaginatedResponse:
    """Retorna uma lista paginada de usuários."""
    return await repository.list_users(params)
