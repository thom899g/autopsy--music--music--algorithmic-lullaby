#!/usr/bin/env python3
"""
Algorithmic Lullaby Generator
A robust system for generating AI-composed lullabies with comprehensive error handling.

Architecture:
1. AI Service Wrapper with fallback mechanisms
2. Musical composition logic with parameter validation
3. File generation with existence checks
4. Comprehensive logging and monitoring
"""

import os
import sys
import time
import logging
import json
import random
from typing import Optional, Dict, Any, Tuple, List
from datetime import datetime
from pathlib import Path
import requests
from dataclasses import dataclass, asdict
import hashlib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('lullaby_generator.log')
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class LullabyConfig:
    """Configuration for lullaby generation"""
    theme: str = "gentle night"
    tempo_bpm: int = 60
    duration_seconds: int = 120
    target_age_months: int = 12
    complexity_level: int = 2  # 1-5 scale
    use_ai: bool = True
    fallback_to_procedural: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LullabyConfig':
        return cls(**data)

@dataclass
class LullabyResult:
    """Result container for lullaby generation"""
    success: bool
    lullaby_text: Optional[str] = None
    melody_notes: Optional[List[str]] = None
    file_path: Optional[str] = None
    generation_method: str = "unknown"
    error_message: Optional[str] = None
    config_hash: Optional[str] = None
    timestamp: str = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class LullabyGenerator:
    """Main orchestrator for lullaby generation"""
    
    # Fallback lullaby templates for when AI fails
    FALLBACK_LULLABIES = [
        "Sleep little one, the moon is high,\nStars are twinkling in the sky.\nDream of lands where fairies play,\nUntil the coming of the day.",
        "Hush now baby, don't you cry,\nGentle lullaby.\nClose your eyes and drift away,\nInto dreams where you can play.",
        "Twinkle, twinkle, little star,\nHow I wonder what you are.\nUp above the world so high,\nLike a diamond in the sky."
    ]
    
    # Simple melody patterns (fallback)
    MELODY_PATTERNS = [
        ["C4", "E4", "G4", "E4", "C4"],
        ["G4", "E4", "C4", "E4", "G4"],
        ["A4", "C5", "E5", "C5", "A4"]
    ]
    
    def __init__(self, config: Optional[LullabyConfig] = None):
        """Initialize the generator with configuration"""
        self.config = config or LullabyConfig()
        self.config_hash = self._generate_config_hash()
        self.ai_service = AIServiceWrapper()
        self.results_dir = Path("lullaby_results")
        self.results_dir.mkdir(exist_ok=True)
        
        logger.info(f"Initialized Lull