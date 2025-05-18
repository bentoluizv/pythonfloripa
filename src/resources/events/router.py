from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.resources.events.repository import EventRepository, get_event_repository
from src.resources.events.schema import EventCreate, EventDB, EventsPaginatedResponse, EventUpdate
from src.resources.shared.schemas import PaginationParams

router = APIRouter(
    prefix='/events',
    tags=['events'],
    responses={
        404: {'description': 'Evento não encontrado'},
        400: {'description': 'Dados inválidos'},
        500: {'description': 'Erro interno do servidor'},
    },
)


EventRepositoryDep = Annotated[EventRepository, Depends(get_event_repository)]


@router.post(
    '',
    response_model=EventDB,
    status_code=HTTPStatus.CREATED,
    summary='Criar novo evento',
    description="""
    Cria um novo evento no sistema.

    - **edition**: Edição do evento
    - **title**: Título do evento
    - **description**: Descrição do evento
    - **start_date**: Data de início do evento
    - **end_date**: Data de término do evento
    - **location**: Localização do evento
    - **image_url**: URL da imagem do evento
    """,
)
async def create_event(
    event_data: EventCreate,
    repository: EventRepositoryDep,
):
    """Cria um novo evento no sistema."""

    existing_event = await repository.get_by_edition(event_data.edition)

    if existing_event:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Event with this edition already exists',
        )

    created_event = await repository.create(event_data)

    return created_event


@router.get(
    '/{event_id}',
    response_model=EventDB,
    summary='Buscar evento por ID',
    description="""
    Retorna os dados de um evento específico pelo seu ID.

    - **event_id**: ID único do evento (ULID)

    Retorna os dados do evento.
    """,
)
async def get_event(
    event_id: str,
    repository: EventRepositoryDep,
):
    """Retorna os dados de um evento pelo seu ID."""
    event = await repository.get_by_id(event_id)

    if not event:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Event not found',
        )

    return event


@router.patch(
    '/{event_id}',
    response_model=EventDB,
    summary='Atualizar evento',
    description="""
    Atualiza os dados de um evento existente.

    - **event_id**: ID único do evento (ULID)

    Campos que podem ser atualizados:
    - **title**: Título do evento
    - **description**: Descrição do evento
    - **start_date**: Data de início do evento
    - **end_date**: Data de término do evento
    - **location**: Localização do evento
    - **image_url**: URL da imagem do evento
    - **is_active**: Status de ativação do evento
    - **is_published**: Status de publicação do evento

    Retorna os dados atualizados do evento.
    """,
)
async def update_event(
    event_id: str,
    event_data: EventUpdate,
    repository: EventRepositoryDep,
):
    """Atualiza os dados de um evento existente."""
    event = await repository.get_by_id(event_id)

    if not event:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Event not found',
        )

    updated_event = await repository.update(event_id, event_data)

    if not updated_event:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail='Failed to update event',
        )

    return updated_event


@router.delete(
    '/{event_id}',
    status_code=HTTPStatus.NO_CONTENT,
    summary='Deletar evento',
    description="""
    Deleta um evento existente.

    - **event_id**: ID único do evento (ULID)

    Retorna 204 No Content em caso de sucesso.
    """,
)
async def delete_event(
    event_id: str,
    repository: EventRepositoryDep,
):
    """Deleta um evento existente."""
    event = await repository.get_by_id(event_id)

    if not event:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Event not found',
        )

    await repository.delete(event_id)


@router.get(
    '',
    response_model=EventsPaginatedResponse,
    summary='Listar eventos',
    description="""
    Retorna uma lista paginada de eventos.

    Parâmetros de paginação:
    - **page**: Número da página (padrão: 1)
    - **per_page**: Itens por página (padrão: 10, máximo: 100)

    Retorna:
    - Lista de eventos
    - Total de eventos
    - Total de páginas
    - Página atual
    - Itens por página
    """,
)
async def list_events(
    params: Annotated[PaginationParams, Depends()],
    repository: EventRepositoryDep,
):
    """Retorna uma lista paginada de eventos."""
    events = await repository.list_events(params)
    return events
