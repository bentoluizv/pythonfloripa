from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.resources.shared.schemas import PaginationParams
from src.resources.speakers.repository import SpeakerRepository, get_speaker_repository
from src.resources.speakers.schema import SpeakerCreate, SpeakerDB, SpeakersPaginatedResponse, SpeakerUpdate

router = APIRouter(
    prefix='/speakers',
    tags=['speakers'],
    responses={
        404: {'description': 'Speaker não encontrado'},
        400: {'description': 'Dados inválidos'},
        500: {'description': 'Erro interno do servidor'},
    },
)


SpeakerRepositoryDep = Annotated[SpeakerRepository, Depends(get_speaker_repository)]


@router.post(
    '',
    response_model=SpeakerDB,
    status_code=HTTPStatus.CREATED,
    summary='Criar novo palestrante',
    description="""
    Cria um novo palestrante no sistema.

    - **name**: Nome do palestrante
    - **email**: Email do palestrante
    - **linkedin_url**: URL do LinkedIn do palestrante
    - **github_url**: URL do GitHub do palestrante
    - **twitter_url**: URL do Twitter do palestrante
    - **website_url**: URL do site do palestrante
    - **bio**: Biografia do palestrante
    - **image_url**: URL da imagem do palestrante

    Retorna os dados do palestrante criado.
    """,
)
async def create_speaker(
    speaker_data: SpeakerCreate,
    speaker_repository: SpeakerRepositoryDep,
):
    """Cria um novo palestrante no sistema."""

    existing_speaker = await speaker_repository.get_by_email(speaker_data.email)

    if existing_speaker:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Speaker with this email already exists',
        )

    created_speaker = await speaker_repository.create(speaker_data)

    return created_speaker


@router.get(
    '/{speaker_id}',
    response_model=SpeakerDB,
    summary='Buscar palestrante por ID',
    description="""
    Retorna os dados de um palestrante específico pelo seu ID.

    - **speaker_id**: ID único do palestrante (ULID)

    Retorna os dados do palestrante.
    """,
)
async def get_speaker(
    speaker_id: str,
    speaker_repository: SpeakerRepositoryDep,
):
    """Retorna os dados de um palestrante pelo seu ID."""

    speaker = await speaker_repository.get_by_id(speaker_id)

    if not speaker:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Speaker not found',
        )

    return speaker


@router.patch(
    '/{speaker_id}',
    response_model=SpeakerDB,
    summary='Atualizar palestrante',
    description="""
    Atualiza os dados de um palestrante existente.

    - **speaker_id**: ID único do palestrante (ULID)

    Campos que podem ser atualizados:
    - **name**: Nome do palestrante
    - **email**: Email do palestrante
    - **linkedin_url**: URL do LinkedIn do palestrante
    - **github_url**: URL do GitHub do palestrante
    - **twitter_url**: URL do Twitter do palestrante
    - **website_url**: URL do site do palestrante
    - **bio**: Biografia do palestrante
    - **image_url**: URL da imagem do palestrante

    Retorna os dados atualizados do palestrante.
    """,
)
async def update_speaker(
    speaker_id: str,
    speaker_data: SpeakerUpdate,
    speaker_repository: SpeakerRepositoryDep,
):
    """Atualiza os dados de um palestrante existente."""

    updated_speaker = await speaker_repository.update(speaker_id, speaker_data)

    if not updated_speaker:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Speaker not found',
        )

    return updated_speaker


@router.delete(
    '/{speaker_id}',
    status_code=HTTPStatus.NO_CONTENT,
    summary='Deletar palestrante',
    description="""
    Deleta um palestrante existente.

    - **speaker_id**: ID único do palestrante (ULID)

    Retorna 204 No Content em caso de sucesso.
    """,
)
async def delete_speaker(
    speaker_id: str,
    speaker_repository: SpeakerRepositoryDep,
):
    """Deleta um palestrante existente."""

    speaker = await speaker_repository.get_by_id(speaker_id)

    if not speaker:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Speaker not found',
        )

    await speaker_repository.delete(speaker_id)


@router.get(
    '',
    response_model=SpeakersPaginatedResponse,
    summary='Listar palestrantes',
    description="""
    Retorna uma lista paginada de palestrantes.

    Parâmetros de paginação:
    - **page**: Número da página (padrão: 1)
    - **per_page**: Itens por página (padrão: 10, máximo: 100)


    Retorna:
    - Lista de palestrantes
    """,
)
async def list_speakers(
    params: Annotated[PaginationParams, Depends()],
    speaker_repository: SpeakerRepositoryDep,
):
    """Retorna uma lista paginada de palestrantes."""
    speakers = await speaker_repository.list_speakers(params)
    return speakers
