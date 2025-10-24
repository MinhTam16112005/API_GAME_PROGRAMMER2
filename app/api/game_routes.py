from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.game import GameCreateRequest, GameResponse
from app.services.game_service import GameService

router = APIRouter()

@router.post("/create", response_model=GameResponse)
async def create_game(
    game_data: GameCreateRequest,
    db: Session = Depends(get_db)
):
    """
    Create a new game with generated distractor texts
    """
    try:
        game_service = GameService()
        game = game_service.create_game_with_distractors(
            db=db,
            title=game_data.title,
            original_text=game_data.original_text,
            host=game_data.host,
            category=game_data.category,
            grade_level=game_data.grade_level
        )
        return game
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create game: {str(e)}")

@router.get("/{game_id}", response_model=GameResponse)
async def get_game(
    game_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific game by ID
    """
    game_service = GameService()
    game = game_service.get_game_by_id(db, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

@router.get("/", response_model=List[GameResponse])
async def get_all_games(
    db: Session = Depends(get_db)
):
    """
    Get all games
    """
    game_service = GameService()
    games = game_service.get_all_games(db)
    return games
