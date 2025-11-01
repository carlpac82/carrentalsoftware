"""
CarJet Direct API - Parse completo com suppliers e categorias
"""
import urllib.request
import urllib.parse
from datetime import datetime
import uuid
import re
import time
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup


def to_carjet_format(dt: datetime) -> str:
    return dt.strftime('%d/%m/%Y %H:%M')


def extract_redirect_url(html: str) -> Optional[str]:
    pattern = r"window\.location\.replace\('([^']+)'\)"
    match = re.search(pattern, html)
    return match.group(1) if match else None


# Mapa de códigos para nomes de suppliers
SUPPLIER_MAP = {
    'AUP': 'Auto Prudente Rent a Car',
    'AUTOPRUDENTE': 'Auto Prudente Rent a Car',
    'THR': 'Thrifty',
    'ECR': 'Europcar',
    'ACE': 'Europcar',  # Ace é o mesmo que Europcar
    'HER': 'Hertz',
    'CEN': 'Centauro',
    'OKR': 'OK Mobility',
    'SUR': 'Surprice',
    'GREENMOTION': 'Greenmotion',
    'GOLDCAR': 'Goldcar',
    'SIXT': 'Sixt',
    'SIX': 'Sixt',
    'ICT': 'Interrent',
    'BGX': 'Budget',
    'YNO': 'YesNo',
    'KED': 'Keddy',
    'FIR': 'Firefly',
    'ALM': 'Alamo',
    'NAT': 'National',
    'ENT': 'Enterprise',
    'ABB1': 'Abby Car',
    'ABB': 'Abby Car',
    'GDS': 'Goldcar',
    'REC': 'Record Go',
    'FLZ': 'Flizzr',
    'ROD': 'Rhodium',
    'CAL': 'Caleche',
    'JUS': 'Justrent',
    # Suppliers adicionais do CarJet
    'AVS': 'Avis',
    'AVI': 'Avis',
    'DOL': 'Dollar',
    'ALA': 'Alamo',
    'LOC': 'Localiza',
    'MOV': 'Movida',
    'UNI': 'Unidas',
    'CAR': 'Carnect',
    'DRI': 'Drive on Holidays',
    'KEY': 'KeynGo',
    'LOY': 'Loyalty',
    'RHO': 'Rhodium',
    'WAY': 'Wayzor',
    'TEL': 'Tellescar',
    'OTO': 'Otopeni',
    'MAS': 'Master',
    'VIC': 'Victoria Cars',
    'AER': 'Aercar',
    'FLE': 'Fleet',
    'TOP': 'TopCar',
    'LIS': 'Lisbon Cars',
    'GUA': 'Guerin',
    'ADA': 'Ada',
    'IDE': 'Ideamerge',
}


# Mapeamento manual de veículos para categorias
VEHICLES = {
    # MINI 4 Lugares
    'fiat 500 4p': 'MINI 4 Lugares',
    'toyota aygo': 'MINI 4 Lugares',
    'peugeot 108': 'MINI 4 Lugares',
    
    # MINI 5 Lugares
    'fiat 500': 'MINI 5 Lugares',
    'citroen c1': 'MINI 5 Lugares',
    'volkswagen up': 'MINI 5 Lugares',
    'hyundai i10': 'MINI 5 Lugares',
    'kia picanto': 'MINI 5 Lugares',
    'fiat panda': 'MINI 5 Lugares',
    
    # MINI Auto
    'fiat 500 auto': 'MINI Auto',
    'citroen c1 auto': 'MINI Auto',
    'toyota aygo auto': 'MINI Auto',
    'peugeot 108 auto': 'MINI Auto',
    'kia picanto auto': 'MINI Auto',
    'mitsubishi spacestar auto': 'MINI Auto',
    
    # ECONOMY
    'renault clio': 'ECONOMY',
    'peugeot 208': 'ECONOMY',
    'ford fiesta': 'ECONOMY',
    'seat ibiza': 'ECONOMY',
    'hyundai i20': 'ECONOMY',
    'opel corsa': 'ECONOMY',
    'volkswagen polo': 'ECONOMY',
    'nissan micra': 'ECONOMY',
    'kia ceed': 'ECONOMY',
    'dacia sandero': 'ECONOMY',
    'skoda fabia': 'ECONOMY',
    'renault twingo': 'MINI 4 Lugares',
    'citroen c3': 'ECONOMY',
    'opel adam': 'MINI 4 Lugares',
    
    # ECONOMY Auto
    'renault clio auto': 'ECONOMY Auto',
    'peugeot 208 auto': 'ECONOMY Auto',
    'ford fiesta auto': 'ECONOMY Auto',
    'seat ibiza auto': 'ECONOMY Auto',
    'hyundai i20 auto': 'ECONOMY Auto',
    'opel corsa auto': 'ECONOMY Auto',
    'peugeot 308 auto': 'ECONOMY Auto',
    'toyota corolla auto': 'ECONOMY Auto',
    'nissan micra auto': 'ECONOMY Auto',
    'ford focus auto': 'ECONOMY Auto',
    'citroen c3 auto': 'ECONOMY Auto',
    
    # SUV
    'nissan juke': 'SUV',
    'peugeot 2008': 'SUV',
    'renault captur': 'SUV',
    'kia stonic': 'SUV',
    'hyundai kauai': 'SUV',
    'hyundai kona': 'SUV',
    'ford kuga': 'SUV',
    'peugeot 3008': 'SUV',
    'nissan qashqai': 'SUV',
    'kia sportage': 'SUV',
    'seat ateca': 'SUV',
    'renault austral': 'SUV',
    'skoda kamiq': 'SUV',
    'hyundai tucson': 'SUV',
    
    # SUV Auto
    'peugeot 3008 auto': 'SUV Auto',
    'toyota chr auto': 'SUV Auto',
    'toyota c-hr auto': 'SUV Auto',
    'ford ecosport auto': 'SUV Auto',
    'opel crossland x auto': 'SUV Auto',
    'volkswagen tiguan auto': 'SUV Auto',
    'skoda karoq auto': 'SUV Auto',
    'citroen c3 aircross auto': 'SUV Auto',
    'volkswagen t-cross auto': 'SUV Auto',
    'vw t-cross auto': 'SUV Auto',
    'fiat 500x auto': 'SUV Auto',
    'opel grandland x auto': 'SUV Auto',
    'citroen c4 auto electric': 'SUV Auto',
    'opel mokka auto electric': 'SUV Auto',
    'citroen c4 auto': 'SUV Auto',
    'renault arkana auto': 'SUV Auto',
    'citroen c4 x auto electric': 'SUV Auto',
    
    # Crossover
    'fiat 500x': 'Crossover',
    'volkswagen t-cross': 'Crossover',
    'vw t-cross': 'Crossover',
    'volkswagen taigo': 'Crossover',
    'vw taigo': 'Crossover',
    'jeep avenger': 'Crossover',
    'citroen c3 aircross': 'Crossover',
    'seat arona': 'SUV',
    'ford puma': 'Crossover',
    'fiat 500l': 'Crossover',
    'citroen c4 cactus': 'Crossover',
    'mazda cx-3': 'Crossover',
    'mitsubishi asx': 'Crossover',
    
    # Luxury (X)
    'mini cooper': 'Luxury',
    'mini countryman': 'Luxury',
    'mini countryman auto': 'Luxury',
    'audi a1': 'Luxury',
    'cupra formentor': 'Luxury',
    'ds 4': 'Luxury',
    'bmw 1 series auto': 'Luxury',
    'mercedes a class auto': 'Luxury',
    'audi a3 auto': 'Luxury',
    'bmw 2 series gran coupe auto': 'Luxury',
    'mercedes c class auto': 'Luxury',
    'mercedes a class automático': 'Luxury',
    'mercedes gla auto': 'Luxury',
    'bmw x1 auto': 'Luxury',
    
    # Station Wagon
    'renault clio sw': 'Station Wagon',
    'opel astra sw': 'Station Wagon',
    'skoda fabia sw': 'Station Wagon',
    'seat leon sw': 'Station Wagon',
    'ford focus sw': 'Station Wagon',
    'peugeot 308 sw': 'Station Wagon',
    'volkswagen golf sw': 'Station Wagon',
    'vw golf sw': 'Station Wagon',
    'skoda octavia': 'Station Wagon',
    'skoda octavia sw': 'Station Wagon',
    'volkswagen passat': 'Station Wagon',
    'vw passat': 'Station Wagon',
    'fiat tipo sw': 'Station Wagon',
    
    # Station Wagon Auto
    'peugeot 308 sw auto': 'Station Wagon Auto',
    'toyota corolla sw auto': 'Station Wagon Auto',
    'cupra leon sw auto': 'Station Wagon Auto',
    'renault megane sedan auto': 'Station Wagon Auto',
    
    # 7 Lugares
    'peugeot 5008': '7 Lugares',
    'peugeot rifter': '7 Lugares',
    'dacia lodgy': '7 Lugares',
    'opel zafira': '7 Lugares',
    'renault grand scenic': '7 Lugares',
    'citroen grand picasso': '7 Lugares',
    'citroen c4 grand picasso': '7 Lugares',
    'citroen c4 picasso': '7 Lugares',
    'dacia jogger': '7 Lugares',
    
    # 7 Lugares Auto
    'volkswagen caddy auto': '7 Lugares Auto',
    'vw caddy auto': '7 Lugares Auto',
    'volkswagen multivan auto': '7 Lugares Auto',
    'vw multivan auto': '7 Lugares Auto',
    'citroen c4 grand spacetourer auto': '7 Lugares Auto',
    'citroen c4 picasso auto': '7 Lugares Auto',
    'renault grand scenic auto': '7 Lugares Auto',
    'mercedes glb auto': '7 Lugares Auto',
    
    # 9 Lugares
    'ford tourneo': '9 Lugares',
    'volkswagen sharan': '9 Lugares',
    'vw sharan': '9 Lugares',
    'ford galaxy': '9 Lugares',
    'ford transit': '9 Lugares',
    'opel vivaro': '9 Lugares',
    'toyota proace': '9 Lugares',
    'fiat talento': '9 Lugares',
    'citroen spacetourer': '9 Lugares',
    'renault trafic': '9 Lugares',
    'peugeot traveller': '9 Lugares',
    'volkswagen transporter': '9 Lugares',
    'vw transporter': '9 Lugares',
    'mercedes vito': '9 Lugares',
    'volkswagen caravelle': '9 Lugares',
    'vw caravelle': '9 Lugares',
    'mercedes v class': '9 Lugares',
    'fiat 500 cabrio': 'Cabrio',
    'ford focus': 'ECONOMY',
    'ford focus sw auto': 'Station Wagon Auto',
    'ford puma auto': 'SUV Auto',
    'kia ceed sw': 'Station Wagon',
    'mazda mx5 cabrio auto': 'Cabrio',
    'mercedes v class auto': '9 Lugares',
    'mercedes vito auto': '9 Lugares',
    'vw polo auto': 'ECONOMY Auto',
    'vw taigo auto': 'SUV Auto',
    'volvo xc40 auto': 'SUV Auto',
    'volvo xc60 auto': 'SUV Auto',
    'volvo v60 4x4 auto, hybrid': 'Station Wagon Auto',
    'volkswagen t-roc': 'SUV',
    'volkswagen t-roc cabrio': 'SUV',
    'seat leon': 'ECONOMY',
    'seat arona auto': 'SUV Auto',
    'renault megane': 'ECONOMY',
    'renault megane auto': 'ECONOMY Auto',
    'renault megane sw': 'Station Wagon',
    'renault megane sw auto': 'Station Wagon Auto',
    'renault megane sw auto, hybrid': 'Station Wagon Auto',
    'peugeot 108 cabrio': 'Cabrio',
    'peugeot 2008 auto': 'SUV Auto',
    'peugeot 2008 auto, electric': 'SUV Auto',
    'peugeot 308': 'ECONOMY',
    'nissan qashqai auto': 'SUV',
    'cupra formentor auto': 'SUV Auto',
    'mercedes c class sw auto': 'Station Wagon Auto',
    'mercedes cle coupe auto': 'Luxury',
    'mercedes e class auto': 'Luxury',
    'mercedes e class sw auto': 'Station Wagon Auto',
    'mercedes s class auto': 'Luxury',
    'citroen c4': 'Crossover',
    'fiat 500': 'MINI 4 Portas',
    'fiat 500 auto': 'MINI Auto',
    'renault megane sw auto': 'Station Wagon Auto',
}


def normalize_supplier(name: str) -> str:
    """Converte código/nome de supplier para nome completo"""
    if not name:
        return 'CarJet'
    
    name_upper = name.upper().strip()
    
    # Tentar extrair código de logo primeiro (ex: logo_AUP.png → AUP)
    logo_match = re.search(r'logo[_-]([A-Z0-9]+)', name_upper)
    if logo_match:
        code = logo_match.group(1)
        if code in SUPPLIER_MAP:
            return SUPPLIER_MAP[code]
    
    # Tentar match direto
    if name_upper in SUPPLIER_MAP:
        return SUPPLIER_MAP[name_upper]
    
    # Normalizar nomes comuns
    for code, full_name in SUPPLIER_MAP.items():
        if code in name_upper or full_name.upper() in name_upper:
            return full_name
    
    # Se ainda não encontrou e tem logo_, retornar o código
    if logo_match:
        return logo_match.group(1).title()
    
    return name.strip()


def detect_category_from_car(car_name: str, transmission: str = '') -> str:
    """
    Detecta categoria baseado no nome do carro
    Consulta primeiro o dicionário VEHICLES para mapeamento exato
    Retorna nome descritivo da categoria para exibição na UI
    """
    car = car_name.lower().strip()
    trans = transmission.lower()
    auto = 'auto' in car or 'auto' in trans or 'automatic' in trans
    
    # 1. PRIORIDADE: Consultar dicionário VEHICLES para match exato
    # Normalizar nome do carro para busca
    car_normalized = car
    car_normalized = re.sub(r'\s+', ' ', car_normalized)  # Normalizar espaços
    
    # Tentar match direto
    if car_normalized in VEHICLES:
        return VEHICLES[car_normalized]
    
    # Tentar variações comuns
    variations = [
        car_normalized,
        car_normalized.replace('volkswagen', 'vw'),
        car_normalized.replace('vw', 'volkswagen'),
        car_normalized.replace('citroën', 'citroen'),
        car_normalized.replace('citroen', 'citroën'),
    ]
    
    for variant in variations:
        if variant in VEHICLES:
            return VEHICLES[variant]
    
    # Tentar busca parcial (substring match) - do mais específico ao menos específico
    for key in sorted(VEHICLES.keys(), key=len, reverse=True):
        if key in car_normalized:
            return VEHICLES[key]
    
    # 2. FALLBACK: Regras genéricas caso não encontre no VEHICLES
    # Casos específicos primeiro
    if 'peugeot' in car and '308' in car and auto:
        return 'ECONOMY Auto'
    if 'fiat' in car and '500l' in car:
        return 'Crossover'
    if 'kia' in car and 'ceed' in car:
        return 'ECONOMY'
    if 'mini' in car and 'countryman' in car:
        return 'Luxury'
    if 'caddy' in car and auto:
        return '7 Lugares Auto'
    if 'peugeot' in car and 'rifter' in car:
        return '7 Lugares'
    if 'citroen' in car and 'c1' in car and auto:
        return 'MINI Auto'
    if 'citroen' in car and 'c3' in car and 'aircross' in car:
        return 'SUV Auto' if auto else 'Crossover'
    if 'peugeot' in car and '5008' in car:
        return '7 Lugares'
    if 'fiat' in car and '500x' in car:
        return 'SUV Auto' if auto else 'Crossover'
    if 'cross' in car and ('vw' in car or 'volkswagen' in car):
        return 'SUV Auto' if auto else 'Crossover'
    if 'peugeot' in car and '308' in car and 'sw' in car and auto:
        return 'Station Wagon Auto'
    
    # Categorias por tipo de veículo
    if any(x in car for x in ['fiat 500', 'citroen c1', 'toyota aygo', 'volkswagen up', 'peugeot 108', 'hyundai i10']):
        if '4' in car and 'door' in car:
            return 'MINI 4 Portas'
        return 'MINI Auto' if auto else 'MINI 5 Portas'
    
    if any(x in car for x in ['renault clio', 'peugeot 208', 'ford fiesta', 'seat ibiza', 'hyundai i20', 'opel corsa']):
        return 'ECONOMY Auto' if auto else 'ECONOMY'
    
    if any(x in car for x in ['juke', '2008', 'captur', 'stonic', 'kauai', 'kona']):
        return 'SUV'
    
    if 'mini' in car and 'cooper' in car:
        return 'Luxury'
    
    if any(x in car for x in ['crossover', 'aircross', '500x', 't-cross', 'taigo', 'arona']):
        return 'SUV Auto' if auto else 'Crossover'
    
    # Station Wagon - IMPORTANTE: NÃO confundir com sedan!
    # Só é SW se tiver explicitamente: sw, estate, wagon, touring, combi
    # E NÃO pode ter "sedan" no nome
    if 'sedan' not in car and 'saloon' not in car:
        if (' sw' in car or 'estate' in car or 'wagon' in car or 'touring' in car or 'combi' in car) and '7' not in car:
            return 'Station Wagon Auto' if auto else 'Station Wagon'
    
    if any(x in car for x in ['3008', 'qashqai', 'c-hr', 'tiguan', 'karoq', 'tucson']):
        return 'SUV Auto' if auto else 'SUV'
    
    if any(x in car for x in ['lodgy', 'scenic', 'rifter', '7 seater']) or '7' in car:
        return '7 Lugares Auto' if auto else '7 Lugares'
    
    if '9' in car or 'tourneo' in car or 'vito' in car or 'transporter' in car:
        return '9 Lugares'
    
    # Fallback baseado em tamanho
    if auto:
        return 'ECONOMY Auto'
    return 'ECONOMY'


def scrape_carjet_direct(location: str, start_dt: datetime, end_dt: datetime, quick: int = 0) -> List[Dict[str, Any]]:
    try:
        print(f"[DIRECT] Location: {location}, Start: {start_dt}, End: {end_dt}")
        
        location_codes = {
            'faro': 'FAO02',
            'aeroporto de faro': 'FAO02',
            'albufeira': 'ABF01',
            'lisboa': 'LIS01',
            'porto': 'OPO01',
            'funchal': 'FNC01',
            'ponta delgada': 'PDL01',
        }
        
        loc_lower = location.lower()
        pickup_code = 'FAO02'
        for key, code in location_codes.items():
            if key in loc_lower:
                pickup_code = code
                break
        
        print(f"[DIRECT] Código: {pickup_code}")
        
        pickup_date = to_carjet_format(start_dt)
        return_date = to_carjet_format(end_dt)
        session_id = str(uuid.uuid4())
        
        form_data = {
            'frmDestino': pickup_code,
            'frmDestinoFinal': '',
            'frmFechaRecogida': pickup_date,
            'frmFechaDevolucion': return_date,
            'frmHasAge': 'False',
            'frmEdad': '35',
            'frmPrvNo': '',
            'frmMoneda': 'EUR',
            'frmMonedaForzada': '',
            'frmJsonFilterInfo': '',
            'frmTipoVeh': 'CAR',
            'idioma': 'PT',
            'frmSession': session_id,
            'frmDetailCode': ''
        }
        
        encoded_data = urllib.parse.urlencode(form_data).encode('utf-8')
        url = 'https://www.carjet.com/do/list/pt'
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html',
            'Accept-Language': 'pt-PT,pt;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Referer': 'https://www.carjet.com/',
            'Origin': 'https://www.carjet.com'
        }
        
        print(f"[DIRECT] POST → {url}")
        req = urllib.request.Request(url, data=encoded_data, headers=headers, method='POST')
        
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode('utf-8')
        
        print(f"[DIRECT] HTML: {len(html)} bytes")
        
        # Seguir redirect se necessário
        if 'Waiting Prices' in html or 'window.location.replace' in html:
            redirect_url = extract_redirect_url(html)
            if redirect_url:
                wait_time = 2 if quick else 4
                print(f"[DIRECT] Aguardando {wait_time}s...")
                time.sleep(wait_time)
                
                full_url = f'https://www.carjet.com{redirect_url}'
                print(f"[DIRECT] Redirect → {full_url[:80]}...")
                req2 = urllib.request.Request(full_url, headers=headers, method='GET')
                
                with urllib.request.urlopen(req2, timeout=30) as response2:
                    html = response2.read().decode('utf-8')
                
                print(f"[DIRECT] HTML final: {len(html)} bytes")
        
        items = parse_carjet_html_complete(html)
        print(f"[DIRECT API] ✅ {len(items)} carros extraídos")
        return items
        
    except Exception as e:
        print(f"[DIRECT API] ❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return []


def parse_carjet_html_complete(html: str) -> List[Dict[str, Any]]:
    """Parse completo com BeautifulSoup - extrai supplier, category, photos"""
    items = []
    
    try:
        soup = BeautifulSoup(html, 'lxml')
        
        # Procurar blocos de carros
        car_blocks = (
            soup.find_all('article') or
            soup.find_all('div', class_=lambda x: x and ('car' in x or 'auto' in x or 'result' in x) if x else False)
        )
        
        print(f"[PARSE] {len(car_blocks)} blocos encontrados")
        
        for idx, block in enumerate(car_blocks):
            try:
                # Nome do carro
                car_name = ''
                for tag in block.find_all(['h3', 'h4', 'span', 'div']):
                    text = tag.get_text(strip=True)
                    # Verificar se parece nome de carro (tem marca conhecida)
                    if any(brand in text.lower() for brand in ['fiat', 'renault', 'peugeot', 'citroen', 'toyota', 'ford', 'vw', 'volkswagen', 'opel', 'seat', 'hyundai', 'kia', 'nissan', 'mercedes', 'bmw', 'audi', 'mini', 'jeep', 'dacia', 'skoda', 'mazda', 'mitsubishi', 'honda', 'suzuki']):
                        car_name = text
                        
                        # LIMPEZA COMPLETA do nome do carro
                        # 1. Remover "ou similar" / "or similar" e tudo depois
                        car_name = re.sub(r'\s+(ou\s*similar|or\s*similar).*$', '', car_name, flags=re.IGNORECASE)
                        
                        # 2. Remover categorias após pipe | (Pequeno, Médio, Grande, etc)
                        car_name = re.sub(r'\s*\|\s*.*$', '', car_name)
                        
                        # 3. Remover categorias de tamanho em qualquer lugar
                        car_name = re.sub(r'\s+(pequeno|médio|medio|grande|compacto|economico|econômico|familiar|luxo|premium|standard)\s*$', '', car_name, flags=re.IGNORECASE)
                        
                        # 4. Manter apenas Auto/Automatic e SW/Station Wagon
                        # Preservar "Auto" ou "Automatic" no final
                        has_auto = re.search(r'\b(auto|automatic)\b', car_name, re.IGNORECASE)
                        # Preservar "SW" ou "Station Wagon"
                        has_sw = re.search(r'\b(sw|station\s*wagon)\b', car_name, re.IGNORECASE)
                        
                        # Normalizar espaços
                        car_name = re.sub(r'\s+', ' ', car_name).strip()
                        break
                
                if not car_name:
                    continue
                
                # Supplier - PRIORIDADE 1: atributo data-prv (mais confiável)
                supplier = 'CarJet'
                
                # Tentar extrair data-prv do article
                data_prv = block.get('data-prv', '').strip()
                if data_prv:
                    supplier = normalize_supplier(data_prv)
                    print(f"[PARSE] Supplier de data-prv: {data_prv} → {supplier}")
                
                # PRIORIDADE 2: procurar por logo ou texto (fallback)
                # Sempre buscar img_tags para uso posterior (fotos)
                img_tags = block.find_all('img')
                
                # Se não encontrou supplier via data-prv, tentar pelos logos
                if supplier == 'CarJet':
                    for img in img_tags:
                        src = img.get('src', '')
                        alt = img.get('alt', '')
                        title = img.get('title', '')

                        # Logos normalmente têm /logo no path
                        if '/logo' in src.lower() or 'logo_' in src.lower():
                            supplier = normalize_supplier(src)
                            if supplier != 'CarJet':
                                break

                        # Verificar alt text
                        if alt and len(alt) <= 50 and alt.lower() not in ['car', 'vehicle', 'auto']:
                            normalized = normalize_supplier(alt)
                            if normalized != 'CarJet' and normalized != alt:
                                supplier = normalized
                                break

                        # Verificar title
                        if title and len(title) <= 50:
                            normalized = normalize_supplier(title)
                            if normalized != 'CarJet' and normalized != title:
                                supplier = normalized
                                break

                # Preço - PRIORIZAR .price.pr-euros (preço total, NÃO por dia)
                price = '€0.00'
                
                # 1ª PRIORIDADE: Buscar .price.pr-euros MAS excluir .price-day-euros e .old-price
                # Procurar por LISTA de classes para verificar todas
                for span_tag in block.find_all('span'):
                    classes = span_tag.get('class', [])
                    if not classes:
                        continue
                    
                    # Verificar se tem 'price' E 'pr-euros' MAS NÃO tem 'day' nem 'old-price'
                    has_price = 'price' in classes
                    has_pr_euros = 'pr-euros' in classes
                    has_day = any('day' in c for c in classes)
                    has_old = any('old' in c for c in classes)
                    
                    if has_price and has_pr_euros and not has_day and not has_old:
                        text = span_tag.get_text(strip=True)
                        # Formato esperado: "1.010,29 €" ou "68,18 €" ou "68.18€"
                        # Aceitar separador de milhares (. ou ,) e decimais
                        match = re.search(r'([\d.,]+)\s*€', text)
                        if match:
                            try:
                                price_str = match.group(1)
                                # Normalizar: remover pontos (milhares) e trocar vírgula por ponto
                                # Exemplo: "1.010,29" → "1010.29"
                                if ',' in price_str and '.' in price_str:
                                    # Formato europeu: 1.010,29
                                    price_str = price_str.replace('.', '').replace(',', '.')
                                elif ',' in price_str:
                                    # Formato europeu sem milhares: 68,18
                                    price_str = price_str.replace(',', '.')
                                # else: já está em formato correto (1010.29)
                                
                                price_val = float(price_str)
                                if 10 < price_val < 10000:
                                    price = f'{price_val:.2f} €'
                                    break  # Encontrou o correto!
                            except:
                                pass
                
                # 2ª PRIORIDADE: Se não encontrou .pr-euros, buscar .price genérico (mas pode ser libras!)
                if price == '€0.00':
                    for tag in block.find_all(['span', 'div'], class_=lambda x: x and 'price' in x if x else False):
                        text = tag.get_text(strip=True)
                        # Ignorar preços em libras (£) e preços por dia
                        if '£' in text or 'libras' in tag.get('class', []):
                            continue
                        if 'day' in tag.get('class', []) or 'dia' in tag.get('class', []):
                            continue
                        
                        match = re.search(r'([\d.,]+)\s*€', text)
                        if match:
                            try:
                                price_str = match.group(1)
                                # Normalizar formato europeu
                                if ',' in price_str and '.' in price_str:
                                    price_str = price_str.replace('.', '').replace(',', '.')
                                elif ',' in price_str:
                                    price_str = price_str.replace(',', '.')
                                
                                price_val = float(price_str)
                                if 10 < price_val < 10000:
                                    price = f'{price_val:.2f} €'
                                    break
                            except:
                                pass
                
                if price == '€0.00':
                    continue
                
                # Foto
                photo = ''
                for img in img_tags:
                    src = img.get('src', '')
                    # Fotos de carros normalmente têm /cars/ ou /vehicles/ no path
                    if '/car' in src.lower() or '/vehicle' in src.lower() or '/img' in src:
                        photo = src if src.startswith('http') else f'https://www.carjet.com{src}'
                        break
                
                # Transmissão
                transmission = ''
                for tag in block.find_all(['span', 'div']):
                    text = tag.get_text(strip=True).lower()
                    if 'automatic' in text or 'manual' in text:
                        transmission = 'Automatic' if 'automatic' in text else 'Manual'
                        break
                
                # Detectar categoria
                category = detect_category_from_car(car_name, transmission)
                
                items.append({
                    'id': idx,
                    'car': car_name,
                    'supplier': supplier,
                    'price': price,
                    'category': category,
                    'transmission': transmission,
                    'photo': photo,
                    'currency': 'EUR',
                    'link': '',
                })
                
            except Exception as e:
                print(f"[PARSE] Erro bloco {idx}: {e}")
                continue
        
        print(f"[PARSE] {len(items)} items válidos")
        
    except Exception as e:
        print(f"[PARSE ERROR] {e}")
        import traceback
        traceback.print_exc()
    
    return items
