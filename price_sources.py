"""
MULTI-SOURCE PRICE AGGREGATOR
Integração com múltiplas fontes de preços de aluguer de carros
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import asyncio
import logging

# Configuração de fontes
PRICE_SOURCES = {
    'carjet': {
        'name': 'CarJet',
        'url': 'https://www.carjet.com',
        'enabled': True,
        'priority': 1,
        'scraper': 'carjet_scraper',
        'reliability': 0.95,
        'coverage': 'global'
    },
    'discovercars': {
        'name': 'DiscoverCars',
        'url': 'https://www.discovercars.com',
        'enabled': True,
        'priority': 2,
        'scraper': 'discovercars_scraper',
        'reliability': 0.90,
        'coverage': 'global'
    },
    'kayak': {
        'name': 'Kayak',
        'url': 'https://www.kayak.com',
        'enabled': True,
        'priority': 3,
        'scraper': 'kayak_scraper',
        'reliability': 0.92,
        'coverage': 'global'
    },
    'vipcars': {
        'name': 'VIP Cars',
        'url': 'https://www.vipcars.com',
        'enabled': True,
        'priority': 4,
        'scraper': 'vipcars_scraper',
        'reliability': 0.85,
        'coverage': 'europe'
    },
    'aurumcars': {
        'name': 'Aurum Cars',
        'url': 'https://www.aurumcars.com',
        'enabled': True,
        'priority': 5,
        'scraper': 'aurumcars_scraper',
        'reliability': 0.80,
        'coverage': 'europe'
    }
}


class PriceAggregator:
    """Agregador inteligente de preços de múltiplas fontes"""
    
    def __init__(self):
        self.sources = PRICE_SOURCES
        self.results = {}
        
    async def fetch_from_all_sources(
        self,
        location: str,
        pickup_date: str,
        dropoff_date: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Busca preços de todas as fontes habilitadas em paralelo
        
        Args:
            location: Localização (ex: "Faro Aeroporto", "Albufeira")
            pickup_date: Data recolha (YYYY-MM-DD)
            dropoff_date: Data entrega (YYYY-MM-DD)
            
        Returns:
            Dict com preços agregados de todas as fontes
        """
        
        tasks = []
        enabled_sources = [k for k, v in self.sources.items() if v['enabled']]
        
        logging.info(f"🔍 Fetching from {len(enabled_sources)} sources: {', '.join(enabled_sources)}")
        
        for source_id in enabled_sources:
            task = self._fetch_from_source(source_id, location, pickup_date, dropoff_date, **kwargs)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Processar resultados
        aggregated = {
            'location': location,
            'pickup_date': pickup_date,
            'dropoff_date': dropoff_date,
            'days': (datetime.fromisoformat(dropoff_date) - datetime.fromisoformat(pickup_date)).days,
            'sources': {},
            'all_cars': [],
            'best_prices_by_group': {},
            'timestamp': datetime.utcnow().isoformat()
        }
        
        for i, source_id in enumerate(enabled_sources):
            result = results[i]
            
            if isinstance(result, Exception):
                logging.error(f"❌ {source_id} failed: {str(result)}")
                aggregated['sources'][source_id] = {
                    'status': 'error',
                    'error': str(result),
                    'cars': []
                }
            else:
                logging.info(f"✅ {source_id}: {len(result.get('cars', []))} cars")
                aggregated['sources'][source_id] = result
                
                # Adicionar carros ao pool geral
                for car in result.get('cars', []):
                    car['source'] = source_id
                    car['source_name'] = self.sources[source_id]['name']
                    aggregated['all_cars'].append(car)
        
        # Calcular melhores preços por grupo
        aggregated['best_prices_by_group'] = self._calculate_best_prices(aggregated['all_cars'])
        
        # Estatísticas
        aggregated['stats'] = {
            'total_sources': len(enabled_sources),
            'successful_sources': len([s for s in aggregated['sources'].values() if s.get('status') != 'error']),
            'total_cars': len(aggregated['all_cars']),
            'unique_groups': len(aggregated['best_prices_by_group'])
        }
        
        return aggregated
    
    async def _fetch_from_source(
        self,
        source_id: str,
        location: str,
        pickup_date: str,
        dropoff_date: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Busca preços de uma fonte específica"""
        
        source_info = self.sources[source_id]
        scraper_name = source_info['scraper']
        
        try:
            # Chamar scraper específico
            if scraper_name == 'carjet_scraper':
                return await self._scrape_carjet(location, pickup_date, dropoff_date, **kwargs)
            elif scraper_name == 'discovercars_scraper':
                return await self._scrape_discovercars(location, pickup_date, dropoff_date, **kwargs)
            elif scraper_name == 'kayak_scraper':
                return await self._scrape_kayak(location, pickup_date, dropoff_date, **kwargs)
            elif scraper_name == 'vipcars_scraper':
                return await self._scrape_vipcars(location, pickup_date, dropoff_date, **kwargs)
            elif scraper_name == 'aurumcars_scraper':
                return await self._scrape_aurumcars(location, pickup_date, dropoff_date, **kwargs)
            else:
                raise NotImplementedError(f"Scraper {scraper_name} not implemented")
                
        except Exception as e:
            logging.error(f"Error scraping {source_id}: {str(e)}")
            raise
    
    async def _scrape_carjet(self, location, pickup, dropoff, **kwargs) -> Dict[str, Any]:
        """Scraper para CarJet (já implementado no main.py)"""
        # Este será chamado do main.py existente
        return {
            'status': 'success',
            'cars': [],
            'note': 'CarJet scraper já implementado no main.py'
        }
    
    async def _scrape_discovercars(self, location, pickup, dropoff, **kwargs) -> Dict[str, Any]:
        """
        Scraper para DiscoverCars.com
        
        URL Pattern: https://www.discovercars.com/search?
            country=Portugal&
            loc=Faro+Airport&
            pickup=2024-12-01&
            dropoff=2024-12-08
        """
        # TODO: Implementar scraper DiscoverCars
        # - Playwright para navegação
        # - Parser HTML específico
        # - Normalização de dados
        
        return {
            'status': 'not_implemented',
            'cars': [],
            'note': 'DiscoverCars scraper - TO BE IMPLEMENTED'
        }
    
    async def _scrape_kayak(self, location, pickup, dropoff, **kwargs) -> Dict[str, Any]:
        """
        Scraper para Kayak.com
        
        URL Pattern: https://www.kayak.com/cars/
            Faro,Portugal-c18085/
            2024-12-01/
            2024-12-08
        """
        # TODO: Implementar scraper Kayak
        return {
            'status': 'not_implemented',
            'cars': [],
            'note': 'Kayak scraper - TO BE IMPLEMENTED'
        }
    
    async def _scrape_vipcars(self, location, pickup, dropoff, **kwargs) -> Dict[str, Any]:
        """Scraper para VIPCars.com"""
        # TODO: Implementar
        return {
            'status': 'not_implemented',
            'cars': [],
            'note': 'VIPCars scraper - TO BE IMPLEMENTED'
        }
    
    async def _scrape_aurumcars(self, location, pickup, dropoff, **kwargs) -> Dict[str, Any]:
        """Scraper para AurumCars.com"""
        # TODO: Implementar
        return {
            'status': 'not_implemented',
            'cars': [],
            'note': 'AurumCars scraper - TO BE IMPLEMENTED'
        }
    
    def _calculate_best_prices(self, cars: List[Dict]) -> Dict[str, Any]:
        """Calcula melhores preços por grupo de todas as fontes"""
        
        best_by_group = {}
        
        for car in cars:
            group = car.get('group') or car.get('car_group') or 'Unknown'
            price = car.get('price') or car.get('total_price')
            
            if not price:
                continue
            
            try:
                price_float = float(str(price).replace('€', '').replace(',', '.').strip())
            except:
                continue
            
            if group not in best_by_group or price_float < best_by_group[group]['price']:
                best_by_group[group] = {
                    'price': price_float,
                    'car': car.get('car'),
                    'supplier': car.get('supplier'),
                    'source': car.get('source'),
                    'source_name': car.get('source_name')
                }
        
        return best_by_group


# Mapeamento de localizações para cada fonte
LOCATION_MAPPINGS = {
    'carjet': {
        'Faro': 'Faro Aeroporto (FAO)',
        'Albufeira': 'Albufeira Cidade',
        'Lisboa': 'Lisboa Aeroporto (LIS)',
        'Porto': 'Porto Aeroporto (OPO)'
    },
    'discovercars': {
        'Faro': 'Faro Airport',
        'Albufeira': 'Albufeira',
        'Lisboa': 'Lisbon Airport',
        'Porto': 'Porto Airport'
    },
    'kayak': {
        'Faro': 'Faro,Portugal-c18085',
        'Albufeira': 'Albufeira,Portugal',
        'Lisboa': 'Lisbon,Portugal-c18091',
        'Porto': 'Porto,Portugal-c18104'
    },
    'vipcars': {
        'Faro': 'Faro Airport',
        'Albufeira': 'Albufeira',
        'Lisboa': 'Lisbon Airport',
        'Porto': 'Porto Airport'
    },
    'aurumcars': {
        'Faro': 'Faro Airport',
        'Albufeira': 'Albufeira',
        'Lisboa': 'Lisbon Airport',
        'Porto': 'Porto Airport'
    }
}


def normalize_location(location: str, source: str) -> str:
    """Normaliza localização para o formato específico da fonte"""
    
    # Detectar localização base
    location_lower = location.lower()
    
    if 'faro' in location_lower:
        base_location = 'Faro'
    elif 'albufeira' in location_lower:
        base_location = 'Albufeira'
    elif 'lisboa' in location_lower or 'lisbon' in location_lower:
        base_location = 'Lisboa'
    elif 'porto' in location_lower:
        base_location = 'Porto'
    else:
        base_location = location
    
    # Mapear para formato da fonte
    if source in LOCATION_MAPPINGS and base_location in LOCATION_MAPPINGS[source]:
        return LOCATION_MAPPINGS[source][base_location]
    
    return location


# Exemplo de uso
if __name__ == "__main__":
    async def test():
        aggregator = PriceAggregator()
        
        result = await aggregator.fetch_from_all_sources(
            location="Faro",
            pickup_date="2024-12-01",
            dropoff_date="2024-12-08"
        )
        
        print(f"✅ Total sources: {result['stats']['total_sources']}")
        print(f"✅ Successful: {result['stats']['successful_sources']}")
        print(f"✅ Total cars: {result['stats']['total_cars']}")
        print(f"✅ Unique groups: {result['stats']['unique_groups']}")
        
        print("\n📊 Best prices by group:")
        for group, data in result['best_prices_by_group'].items():
            print(f"  {group}: {data['price']:.2f}€ from {data['source_name']}")
    
    asyncio.run(test())
