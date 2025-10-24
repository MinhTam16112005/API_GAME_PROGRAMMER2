import openai
import google.generativeai as genai
from typing import List
from app.config import OPENAI_API_KEY, GEMINI_API_KEY, LLM_PROVIDER

class LLMService:
    def __init__(self):
        self.provider = LLM_PROVIDER.lower()
        self.has_openai_key = bool(OPENAI_API_KEY)
        self.has_gemini_key = bool(GEMINI_API_KEY)
        
        if self.provider == "openai" and self.has_openai_key:
            openai.api_key = OPENAI_API_KEY
        elif self.provider == "gemini" and self.has_gemini_key:
            genai.configure(api_key=GEMINI_API_KEY)
        else:
            # Try to use any available provider
            if self.has_gemini_key:
                self.provider = "gemini"
                genai.configure(api_key=GEMINI_API_KEY)
            elif self.has_openai_key:
                self.provider = "openai"
                openai.api_key = OPENAI_API_KEY
    
    def generate_distractors(self, original_text: str, num_distractors: int = 3) -> List[str]:
        """
        Generate distractor texts that resemble the original but include inaccuracies
        """
        # If no API keys available, use fallback immediately
        if not (self.has_openai_key or self.has_gemini_key):
            return self._generate_fallback_distractors(original_text, num_distractors)
        
        # Try the configured provider first
        if self.provider == "gemini" and self.has_gemini_key:
            return self._generate_with_gemini(original_text, num_distractors)
        elif self.provider == "openai" and self.has_openai_key:
            return self._generate_with_openai(original_text, num_distractors)
        
        # Fallback to any available provider
        if self.has_gemini_key:
            return self._generate_with_gemini(original_text, num_distractors)
        elif self.has_openai_key:
            return self._generate_with_openai(original_text, num_distractors)
        else:
            return self._generate_fallback_distractors(original_text, num_distractors)
    
    def _generate_with_openai(self, original_text: str, num_distractors: int) -> List[str]:
        """Generate distractors using OpenAI"""
        prompt = f"""
        You are an expert at creating educational distractor texts. 
        Given the original text, create {num_distractors} distractor texts that:
        1. Resemble the original text in style and structure
        2. Include small inaccuracies, misleading details, or missing information
        3. Are plausible enough to be confusing but clearly wrong
        4. Each distractor should have different types of errors (factual, logical, missing info)
        
        Original text: "{original_text}"
        
        Generate exactly {num_distractors} distractor texts. Return them as a JSON array of strings.
        Example format: ["distractor 1", "distractor 2", "distractor 3"]
        """
        
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert educational content creator."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=500
            )
            
            return self._parse_response(response.choices[0].message.content.strip(), num_distractors)
                
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return self._generate_fallback_distractors(original_text, num_distractors)
    
    def _generate_with_gemini(self, original_text: str, num_distractors: int) -> List[str]:
        """Generate distractors using Gemini"""
        prompt = f"""
        You are an expert at creating educational distractor texts. 
        Given the original text, create {num_distractors} distractor texts that:
        1. Resemble the original text in style and structure
        2. Include small inaccuracies, misleading details, or missing information
        3. Are plausible enough to be confusing but clearly wrong
        4. Each distractor should have different types of errors (factual, logical, missing info)
        
        Original text: "{original_text}"
        
        Generate exactly {num_distractors} distractor texts. Return them as a JSON array of strings.
        Example format: ["distractor 1", "distractor 2", "distractor 3"]
        """
        
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            return self._parse_response(response.text.strip(), num_distractors)
                
        except Exception as e:
            print(f"Gemini API error: {e}")
            return self._generate_fallback_distractors(original_text, num_distractors)
    
    def _parse_response(self, response_text: str, num_distractors: int) -> List[str]:
        """Parse LLM response and extract distractors"""
        import json
        
        try:
            # Try to parse as JSON array
            distractors = json.loads(response_text)
            if isinstance(distractors, list) and len(distractors) >= num_distractors:
                return distractors[:num_distractors]
        except json.JSONDecodeError:
            pass
        
        # Fallback: split by lines and take first N
        lines = [line.strip() for line in response_text.split('\n') if line.strip()]
        if len(lines) >= num_distractors:
            return lines[:num_distractors]
        
        # If still not enough, use fallback generation
        return self._generate_fallback_distractors("", num_distractors)
    
    def _generate_fallback_distractors(self, original_text: str, num_distractors: int) -> List[str]:
        """
        Fallback method to generate distractors without LLM
        """
        # Simple rule-based distractor generation
        distractors = []
        
        # Distractor 1: Change a key word
        if "sunlight" in original_text.lower():
            distractor1 = original_text.replace("sunlight", "moonlight")
            distractors.append(distractor1)
        
        # Distractor 2: Change the process
        if "convert" in original_text.lower():
            distractor2 = original_text.replace("convert", "absorb")
            distractors.append(distractor2)
        
        # Distractor 3: Change the outcome
        if "glucose" in original_text.lower():
            distractor3 = original_text.replace("glucose", "carbon dioxide")
            distractors.append(distractor3)
        
        # Fill remaining with variations
        while len(distractors) < num_distractors:
            base_text = original_text
            if len(distractors) == 0:
                base_text = base_text.replace("water", "air")
            elif len(distractors) == 1:
                base_text = base_text.replace("oxygen", "nitrogen")
            else:
                base_text = base_text.replace("plants", "animals")
            distractors.append(base_text)
        
        return distractors[:num_distractors]
