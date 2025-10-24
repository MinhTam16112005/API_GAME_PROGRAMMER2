from sqlalchemy.orm import Session
from typing import List
from app.models.game import Game
from app.models.distractor import Distractor
from app.services.llm_service import LLMService

class GameService:
    def __init__(self):
        self.llm_service = LLMService()
    
    def create_game_with_distractors(
        self, 
        db: Session, 
        title: str, 
        original_text: str, 
        host: str = None, 
        category: str = None, 
        grade_level: int = None
    ) -> Game:
        """
        Create a new game with generated distractors
        """
        # Create the game
        game = Game(
            title=title,
            original_text=original_text,
            host=host,
            category=category,
            grade_level=grade_level
        )
        
        db.add(game)
        db.commit()
        db.refresh(game)
        
        # Generate distractors
        try:
            distractor_texts = self.llm_service.generate_distractors(original_text, 3)
        except Exception as e:
            print(f"LLM service failed: {e}")
            # Use fallback generation
            distractor_texts = self.llm_service._generate_fallback_distractors(original_text, 3)
        
        # Create distractor records
        for distractor_text in distractor_texts:
            distractor = Distractor(
                game_id=game.id,
                distractor_text=distractor_text
            )
            db.add(distractor)
        
        db.commit()
        
        # Refresh to get the distractors
        db.refresh(game)
        return game
    
    def get_game_by_id(self, db: Session, game_id: int) -> Game:
        """
        Get a game by ID with its distractors
        """
        return db.query(Game).filter(Game.id == game_id).first()
    
    def get_all_games(self, db: Session) -> List[Game]:
        """
        Get all games with their distractors
        """
        return db.query(Game).all()
