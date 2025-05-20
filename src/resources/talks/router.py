from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from typing_extensions import Annotated

from src.resources.events.repository import EventRepository, get_event_repository
from src.resources.shared.schemas import PaginationParams
from src.resources.talks.repository import TalkRepository, get_talk_repository
from src.resources.talks.schema import TalkCreate, TalkDB, TalksPaginatedResponse, TalkUpdate

router = APIRouter(
    prefix='/talks',
    tags=['talks'],
    responses={
        404: {'description': 'Talk não encontrado'},
        400: {'description': 'Dados inválidos'},
        500: {'description': 'Erro interno do servidor'},
    },
)


TalkRepositoryDep = Annotated[TalkRepository, Depends(get_talk_repository)]
EventRepositoryDep = Annotated[EventRepository, Depends(get_event_repository)]


@router.post(
    '',
    response_model=TalkDB,
    status_code=HTTPStatus.CREATED,
    summary='Criar nova palestra',
    description="""
    Cria uma nova palestra no sistema.

    - **title**: Título da palestra
    - **description**: Descrição da palestra
    - **speaker_id**: ID do palestrante da palestra
    - **start_time**: Data e hora de início da palestra
    - **end_time**: Data e hora de término da palestra
    - **event_id**: ID do evento da palestra

    Retorna os dados da palestra criada.
    """,
)
async def create_talk(
    talk_data: TalkCreate,
    talk_repository: TalkRepositoryDep,
    event_repository: EventRepositoryDep,
):
    """Cria uma nova palestra no sistema."""

    existing_event = await event_repository.get_by_id(talk_data.event_id)

    if not existing_event:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Event does not exist',
        )

    if talk_data.title in [talk.title for talk in existing_event.talks]:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Talk with this title already exists',
        )

    created_talk = await talk_repository.create(talk_data)

    return created_talk


@router.get(
    '/{talk_id}',
    response_model=TalkDB,
    summary='Buscar palestra por ID',
    description="""
    Retorna os dados de uma palestra específica pelo seu ID.

    - **talk_id**: ID único da palestra (ULID)

    Retorna os dados da palestra.
    """,
)
async def get_talk(
    talk_id: str,
    talk_repository: TalkRepositoryDep,
):
    """Retorna os dados de uma palestra pelo seu ID."""

    talk = await talk_repository.get_by_id(talk_id)

    if not talk:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Talk not found',
        )

    return talk


@router.patch(
    '/{talk_id}',
    response_model=TalkDB,
    summary='Atualizar palestra',
    description="""
    Atualiza os dados de uma palestra existente.

    - **talk_id**: ID único da palestra (ULID)

    Campos que podem ser atualizados:
    - **title**: Título da palestra
    - **description**: Descrição da palestra
    - **speaker_id**: ID do palestrante da palestra
    - **start_time**: Data e hora de início da palestra
    - **end_time**: Data e hora de término da palestra
    - **event_id**: ID do evento da palestra

    Retorna os dados atualizados da palestra.
    """,
)
async def update_talk(
    talk_id: str,
    talk_data: TalkUpdate,
    talk_repository: TalkRepositoryDep,
):
    """Atualiza os dados de uma palestra existente."""
    talk = await talk_repository.get_by_id(talk_id)

    if not talk:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Talk not found',
        )

    updated_talk = await talk_repository.update(talk_id, talk_data)

    if not updated_talk:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail='Failed to update talk',
        )

    return updated_talk


@router.delete(
    '/{talk_id}',
    status_code=HTTPStatus.NO_CONTENT,
    summary='Deletar palestra',
    description="""
    Deleta uma palestra existente.

    - **talk_id**: ID único da palestra (ULID)

    Retorna 204 No Content em caso de sucesso.
    """,
)
async def delete_talk(
    talk_id: str,
    talk_repository: TalkRepositoryDep,
):
    """Deleta uma palestra existente."""
    talk = await talk_repository.get_by_id(talk_id)

    if not talk:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Talk not found',
        )

    await talk_repository.delete(talk_id)


@router.get(
    '',
    response_model=TalksPaginatedResponse,
    summary='Listar palestras',
    description="""
    Retorna uma lista paginada de palestras.

    Parâmetros de paginação:
    - **page**: Número da página (padrão: 1)
    - **per_page**: Itens por página (padrão: 10, máximo: 100)

    Retorna:
    - Lista de palestras
    """,
)
async def list_talks(
    params: Annotated[PaginationParams, Depends()],
    talk_repository: TalkRepositoryDep,
):
    """Retorna uma lista paginada de palestras."""
    talks = await talk_repository.list_talks(params)
    return talks
