"""
AI PRICING ASSISTANT
Integração com Claude Sonnet 3.5 / GPT-4 para sugestões inteligentes de pricing
"""

import os
import json
from typing import Dict, List, Any, Optional
import logging

# Tentar importar bibliotecas de AI
try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


class AIPricingAssistant:
    """
    Assistente de pricing usando AI externa (Claude/GPT)
    Analisa dados de mercado e fornece sugestões inteligentes
    """
    
    def __init__(self, provider: str = "claude"):
        """
        Args:
            provider: "claude" ou "openai"
        """
        self.provider = provider
        self.anthropic_client = None
        self.openai_client = None
        
        # Configurar cliente baseado no provider
        if provider == "claude" and HAS_ANTHROPIC:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if api_key:
                self.anthropic_client = anthropic.Anthropic(api_key=api_key)
                logging.info("✅ Claude AI initialized")
            else:
                logging.warning("⚠️ ANTHROPIC_API_KEY not found in environment")
        
        elif provider == "openai" and HAS_OPENAI:
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                openai.api_key = api_key
                self.openai_client = openai
                logging.info("✅ OpenAI initialized")
            else:
                logging.warning("⚠️ OPENAI_API_KEY not found in environment")
        
        else:
            logging.warning(f"⚠️ AI provider '{provider}' not available or libraries not installed")
    
    def analyze_market_positioning(
        self,
        group: str,
        days: int,
        location: str,
        current_price: float,
        competitors: List[Dict[str, Any]],
        historical_data: Optional[List[Dict]] = None,
        min_price_day: Optional[float] = None,
        min_price_month: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Analisa posicionamento de mercado usando AI externa
        
        Args:
            group: Grupo de veículo (B1, B2, D, etc)
            days: Número de dias de aluguer
            location: Localização (Albufeira, Faro, etc)
            current_price: Preço atual AutoPrudente
            competitors: Lista de preços dos competidores
            historical_data: Dados históricos opcionais
            min_price_day: Preço mínimo por dia (NUNCA pode ser menor)
            min_price_month: Preço mínimo para reservas ≥30 dias
            
        Returns:
            Dict com análise e sugestões da AI
        """
        
        if not self.is_available():
            return self._fallback_analysis(
                group, days, location, current_price, competitors,
                min_price_day, min_price_month
            )
        
        # Preparar contexto para AI
        context = self._prepare_market_context(
            group, days, location, current_price, competitors, historical_data,
            min_price_day, min_price_month
        )
        
        # Fazer request para AI
        if self.provider == "claude" and self.anthropic_client:
            analysis = self._analyze_with_claude(context)
        elif self.provider == "openai" and self.openai_client:
            analysis = self._analyze_with_openai(context)
        else:
            return self._fallback_analysis(
                group, days, location, current_price, competitors,
                min_price_day, min_price_month
            )
        
        # VALIDAÇÃO CRÍTICA: Aplicar preço mínimo
        analysis = self._enforce_minimum_price(analysis, days, min_price_day, min_price_month)
        
        return analysis
    
    def _prepare_market_context(
        self,
        group: str,
        days: int,
        location: str,
        current_price: float,
        competitors: List[Dict],
        historical_data: Optional[List[Dict]],
        min_price_day: Optional[float] = None,
        min_price_month: Optional[float] = None
    ) -> Dict[str, Any]:
        """Prepara contexto formatado para enviar à AI"""
        
        # Calcular estatísticas de mercado
        competitor_prices = [c.get('price', 0) for c in competitors if c.get('price')]
        
        if competitor_prices:
            lowest = min(competitor_prices)
            highest = max(competitor_prices)
            average = sum(competitor_prices) / len(competitor_prices)
            median = sorted(competitor_prices)[len(competitor_prices) // 2]
            
            # Posição no mercado
            below_count = sum(1 for p in competitor_prices if p < current_price)
            position = below_count + 1
            percentile = (position / (len(competitor_prices) + 1)) * 100
        else:
            lowest = highest = average = median = current_price
            percentile = 50
        
        context = {
            "vehicle": {
                "group": group,
                "rental_days": days,
                "location": location,
                "booking_type": self._classify_booking_type(days)
            },
            "current_pricing": {
                "autoprudente_price": current_price,
                "market_position": f"{percentile:.0f}th percentile",
                "position_rank": f"#{below_count + 1} of {len(competitor_prices) + 1}"
            },
            "market_data": {
                "competitors_count": len(competitors),
                "lowest_price": lowest,
                "highest_price": highest,
                "average_price": average,
                "median_price": median,
                "price_range": highest - lowest,
                "competitors": [
                    {
                        "supplier": c.get('supplier', 'Unknown'),
                        "price": c.get('price'),
                        "car": c.get('car')
                    }
                    for c in competitors[:10]  # Top 10 competitors
                ]
            },
            "historical_patterns": historical_data if historical_data else [],
            "pricing_constraints": {
                "min_price_day": min_price_day,
                "min_price_month": min_price_month,
                "applicable_minimum": min_price_month if days >= 30 and min_price_month else min_price_day,
                "note": "CRITICAL: Recommended price MUST NEVER be below the applicable minimum"
            }
        }
        
        return context
    
    def _classify_booking_type(self, days: int) -> str:
        """Classifica tipo de booking baseado na duração"""
        if days <= 3:
            return "short_term_weekend"
        elif days <= 7:
            return "week_rental"
        elif days <= 14:
            return "extended_rental"
        else:
            return "long_term_advance_booking"
    
    def _analyze_with_claude(self, context: Dict) -> Dict[str, Any]:
        """Análise usando Claude Sonnet 3.5"""
        
        prompt = self._build_pricing_prompt(context)
        
        try:
            message = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",  # Latest Sonnet 3.5
                max_tokens=2000,
                temperature=0.3,  # Mais determinístico para decisões de negócio
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Parse resposta
            response_text = message.content[0].text
            
            # Tentar extrair JSON da resposta
            analysis = self._parse_ai_response(response_text)
            analysis['ai_provider'] = 'claude-sonnet-3.5'
            analysis['ai_raw_response'] = response_text
            
            return analysis
            
        except Exception as e:
            logging.error(f"Claude AI error: {str(e)}")
            return self._fallback_analysis(
                context['vehicle']['group'],
                context['vehicle']['rental_days'],
                context['vehicle']['location'],
                context['current_pricing']['autoprudente_price'],
                context['market_data']['competitors']
            )
    
    def _analyze_with_openai(self, context: Dict) -> Dict[str, Any]:
        """Análise usando GPT-4"""
        
        prompt = self._build_pricing_prompt(context)
        
        try:
            response = self.openai_client.ChatCompletion.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert car rental pricing analyst specializing in dynamic pricing and competitive positioning."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            response_text = response.choices[0].message.content
            
            analysis = self._parse_ai_response(response_text)
            analysis['ai_provider'] = 'gpt-4'
            analysis['ai_raw_response'] = response_text
            
            return analysis
            
        except Exception as e:
            logging.error(f"OpenAI error: {str(e)}")
            return self._fallback_analysis(
                context['vehicle']['group'],
                context['vehicle']['rental_days'],
                context['vehicle']['location'],
                context['current_pricing']['autoprudente_price'],
                context['market_data']['competitors']
            )
    
    def _build_pricing_prompt(self, context: Dict) -> str:
        """Constrói prompt para AI"""
        
        return f"""You are a car rental pricing expert. Analyze this market data and provide pricing recommendations.

CONTEXT:
- Vehicle Group: {context['vehicle']['group']}
- Rental Duration: {context['vehicle']['rental_days']} days
- Booking Type: {context['vehicle']['booking_type']}
- Location: {context['vehicle']['location']}

CURRENT PRICING:
- AutoPrudente (Our Price): €{context['current_pricing']['autoprudente_price']:.2f}
- Market Position: {context['current_pricing']['market_position']}
- Rank: {context['current_pricing']['position_rank']}

MARKET DATA:
- Competitors Analyzed: {context['market_data']['competitors_count']}
- Lowest Competitor: €{context['market_data']['lowest_price']:.2f}
- Average Market: €{context['market_data']['average_price']:.2f}
- Highest Competitor: €{context['market_data']['highest_price']:.2f}
- Price Range: €{context['market_data']['price_range']:.2f}

TOP COMPETITORS:
{json.dumps(context['market_data']['competitors'], indent=2)}

⚠️ PRICING CONSTRAINTS (CRITICAL):
- Minimum Price/Day: €{context['pricing_constraints']['min_price_day']:.2f if context['pricing_constraints']['min_price_day'] else 'Not set'}
- Minimum Price/Month (≥30d): €{context['pricing_constraints']['min_price_month']:.2f if context['pricing_constraints']['min_price_month'] else 'Not set'}
- APPLICABLE MINIMUM: €{context['pricing_constraints']['applicable_minimum']:.2f if context['pricing_constraints']['applicable_minimum'] else 'Not set'}

⛔ ABSOLUTE RULE: Your recommended price MUST NEVER be below the applicable minimum!
   If market analysis suggests a lower price, recommend the minimum instead.

ANALYSIS REQUIRED:
1. Evaluate current pricing position (too cheap, too expensive, optimal)
2. Consider booking type and customer psychology:
   - Short-term (1-3d): Weekend/last-minute bookings - competitive market
   - Week rental (4-7d): Standard bookings - balanced approach
   - Extended (8-14d): Vacation rentals - value positioning
   - Long-term (15+d): Advance bookings - reliability over price
3. Analyze competitive landscape
4. Consider seasonality and demand patterns
5. Recommend optimal price and strategy

RESPONSE FORMAT (JSON):
{{
  "analysis": "Brief analysis of current position and market dynamics",
  "current_position": "too_cheap|optimal|too_expensive",
  "recommended_price": 25.50,
  "price_change": 2.00,
  "price_change_percentage": 8.5,
  "confidence": 85,
  "strategy": "INCREASE_TO_VALUE|DECREASE_TO_COMPETITIVE|MAINTAIN",
  "reasoning": "Detailed explanation of recommendation considering booking type and market position",
  "risk_factors": ["Factor 1", "Factor 2"],
  "opportunities": ["Opportunity 1", "Opportunity 2"],
  "target_percentile": 65
}}

Provide your analysis and recommendation now:"""
    
    def _parse_ai_response(self, response_text: str) -> Dict[str, Any]:
        """Parse resposta da AI para extrair dados estruturados"""
        
        # Tentar extrair JSON da resposta
        try:
            # Procurar por bloco JSON
            import re
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                json_str = json_match.group(0)
                data = json.loads(json_str)
                return data
        except Exception as e:
            logging.warning(f"Failed to parse JSON from AI response: {e}")
        
        # Fallback: parse manual
        return {
            "analysis": response_text,
            "recommended_price": None,
            "confidence": 50,
            "strategy": "REVIEW_MANUALLY",
            "reasoning": response_text
        }
    
    def _fallback_analysis(
        self,
        group: str,
        days: int,
        location: str,
        current_price: float,
        competitors: List[Dict],
        min_price_day: Optional[float] = None,
        min_price_month: Optional[float] = None
    ) -> Dict[str, Any]:
        """Análise fallback quando AI não está disponível"""
        
        competitor_prices = [c.get('price', 0) for c in competitors if c.get('price')]
        
        if not competitor_prices:
            return {
                "analysis": "No competitor data available",
                "recommended_price": current_price,
                "confidence": 0,
                "strategy": "MAINTAIN",
                "reasoning": "Insufficient data for analysis",
                "ai_provider": "fallback"
            }
        
        lowest = min(competitor_prices)
        average = sum(competitor_prices) / len(competitor_prices)
        
        # Lógica simples baseada em percentil
        below_count = sum(1 for p in competitor_prices if p < current_price)
        percentile = (below_count / len(competitor_prices)) * 100
        
        if percentile < 30:
            strategy = "INCREASE_MARGIN"
            recommended = lowest * 1.10
            reasoning = f"Currently too cheap ({percentile:.0f}th percentile). Increase to capture margin."
        elif percentile > 70:
            strategy = "DECREASE_TO_COMPETITIVE"
            recommended = average * 0.95
            reasoning = f"Currently too expensive ({percentile:.0f}th percentile). Reduce to improve conversion."
        else:
            strategy = "MAINTAIN"
            recommended = current_price
            reasoning = f"Well positioned at {percentile:.0f}th percentile."
        
        analysis = {
            "analysis": f"Fallback analysis: {len(competitors)} competitors analyzed",
            "current_position": "optimal" if 30 <= percentile <= 70 else ("too_cheap" if percentile < 30 else "too_expensive"),
            "recommended_price": recommended,
            "price_change": recommended - current_price,
            "price_change_percentage": ((recommended - current_price) / current_price) * 100 if current_price > 0 else 0,
            "confidence": 60,
            "strategy": strategy,
            "reasoning": reasoning,
            "ai_provider": "fallback"
        }
        
        # Aplicar preço mínimo
        return self._enforce_minimum_price(analysis, days, min_price_day, min_price_month)
    
    def _enforce_minimum_price(
        self,
        analysis: Dict[str, Any],
        days: int,
        min_price_day: Optional[float],
        min_price_month: Optional[float]
    ) -> Dict[str, Any]:
        """
        VALIDAÇÃO CRÍTICA: Garante que recommended_price NUNCA é menor que o mínimo
        """
        if 'recommended_price' not in analysis or analysis['recommended_price'] is None:
            return analysis
        
        recommended = analysis['recommended_price']
        
        # Determinar preço mínimo aplicável
        applicable_minimum = None
        if days >= 30 and min_price_month:
            applicable_minimum = min_price_month
            min_type = "monthly"
        elif min_price_day:
            applicable_minimum = min_price_day
            min_type = "daily"
        
        # Aplicar mínimo se necessário
        if applicable_minimum and recommended < applicable_minimum:
            original_price = recommended
            analysis['recommended_price'] = applicable_minimum
            analysis['price_change'] = applicable_minimum - analysis.get('current_price', recommended)
            analysis['price_change_percentage'] = (
                ((applicable_minimum - analysis.get('current_price', recommended)) / 
                 analysis.get('current_price', recommended)) * 100
                if analysis.get('current_price', recommended) > 0 else 0
            )
            
            # Atualizar reasoning para explicar ajuste
            original_reasoning = analysis.get('reasoning', '')
            analysis['reasoning'] = (
                f"{original_reasoning}\n\n"
                f"⚠️ PRICE FLOOR APPLIED: AI suggested €{original_price:.2f}, but this is below "
                f"the configured {min_type} minimum of €{applicable_minimum:.2f}. "
                f"Price automatically adjusted to respect minimum pricing rules."
            )
            
            analysis['minimum_price_applied'] = True
            analysis['original_ai_suggestion'] = original_price
            analysis['applied_minimum'] = applicable_minimum
            analysis['minimum_type'] = min_type
            
            logging.info(
                f"⚠️ Minimum price enforced: {original_price:.2f}€ → {applicable_minimum:.2f}€ "
                f"({min_type} minimum for {days}d rental)"
            )
        else:
            analysis['minimum_price_applied'] = False
        
        return analysis
    
    def is_available(self) -> bool:
        """Verifica se AI está disponível"""
        if self.provider == "claude":
            return self.anthropic_client is not None
        elif self.provider == "openai":
            return self.openai_client is not None
        return False
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status da integração AI"""
        return {
            "provider": self.provider,
            "available": self.is_available(),
            "has_anthropic": HAS_ANTHROPIC,
            "has_openai": HAS_OPENAI,
            "client_initialized": self.anthropic_client is not None or self.openai_client is not None
        }


# Singleton instance
_ai_assistant = None

def get_ai_assistant(provider: str = "claude") -> AIPricingAssistant:
    """Get or create AI assistant instance"""
    global _ai_assistant
    if _ai_assistant is None:
        _ai_assistant = AIPricingAssistant(provider=provider)
    return _ai_assistant
