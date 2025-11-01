# Frontend Vehicle Name Mapping

## Problema
A frontend UI mostra nomes originais do scraping (ex: "Fiat Panda ou similar Pequeno") em vez dos clean names definidos no sistema (ex: "Fiat Panda").

## Solução
Usar o endpoint `/api/vehicles/name-mapping` para obter o mapeamento e aplicar nos resultados.

## API Endpoint

### GET /api/vehicles/name-mapping

Retorna mapeamento de nomes originais → clean names

**Resposta:**
```json
{
  "ok": true,
  "mapping": {
    "fiat 500": "fiat 500",
    "fiat panda": "fiat panda",
    "renault clio": "renault clio",
    ...
  },
  "total": 500
}
```

## Como Usar na Frontend

### 1. Buscar Mapeamento ao Carregar

```javascript
let vehicleNameMapping = {};

async function loadVehicleMapping() {
    try {
        const response = await fetch('/api/vehicles/name-mapping');
        const data = await response.json();
        if (data.ok) {
            vehicleNameMapping = data.mapping;
        }
    } catch (error) {
        console.error('Error loading vehicle mapping:', error);
    }
}

// Carregar ao iniciar
loadVehicleMapping();
```

### 2. Função para Limpar Nome do Veículo

```javascript
function getCleanVehicleName(originalName) {
    // Remove sufixos comuns
    const cleaned = originalName
        .replace(/\s+ou\s+similar(es)?/gi, '')
        .replace(/\s+ou\s+semelhante(s)?/gi, '')
        .replace(/\s+or\s+similar/gi, '')
        .replace(/\s+(pequeno|médio|grande|small|medium|large)/gi, '')
        .trim()
        .toLowerCase();
    
    // Buscar no mapeamento
    if (vehicleNameMapping[cleaned]) {
        // Retornar capitalizado
        return vehicleNameMapping[cleaned]
            .split(' ')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }
    
    // Se não encontrar, retornar cleaned capitalizado
    return cleaned
        .split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
}
```

### 3. Aplicar nos Resultados

```javascript
// Ao receber resultados do scraping
function processResults(results) {
    return results.map(result => {
        // Limpar o nome do carro
        const cleanName = getCleanVehicleName(result.car);
        
        return {
            ...result,
            car: cleanName,           // Nome limpo
            originalCar: result.car   // Nome original (manter para referência)
        };
    });
}
```

### 4. Exemplo Completo

```javascript
// Buscar resultados
async function searchVehicles(location, dates) {
    // 1. Buscar resultados do CarJet
    const response = await fetch(`/api/search?location=${location}&...`);
    const data = await response.json();
    
    // 2. Processar e limpar nomes
    const cleanedResults = data.results.map(result => ({
        ...result,
        car: getCleanVehicleName(result.car),
        displayName: getCleanVehicleName(result.car)
    }));
    
    // 3. Renderizar com nomes limpos
    renderResults(cleanedResults);
}

function renderResults(results) {
    results.forEach(result => {
        // Agora result.car é "Fiat Panda" em vez de "Fiat Panda ou similar Pequeno"
        const card = createCard(result);
        container.appendChild(card);
    });
}
```

## Exemplos de Transformação

| Original (Scraping)              | Clean Name (Resultado)  |
|----------------------------------|-------------------------|
| Fiat Panda ou similar Pequeno    | Fiat Panda             |
| RENAULT Clio ou semelhante       | Renault Clio           |
| Peugeot 3008 or similar          | Peugeot 3008           |
| VW up pequeno                    | Volkswagen Up          |

## Refresh do Mapeamento

Se criar novas categorias/veículos, refresh o mapeamento:

```javascript
// Após criar novo veículo
await saveVehicle(newVehicle);
await loadVehicleMapping(); // Refresh mapping
```

## Cache

Considere fazer cache do mapeamento:

```javascript
const CACHE_KEY = 'vehicleNameMapping';
const CACHE_DURATION = 3600000; // 1 hora

async function loadVehicleMapping() {
    // Tentar cache
    const cached = localStorage.getItem(CACHE_KEY);
    if (cached) {
        const {data, timestamp} = JSON.parse(cached);
        if (Date.now() - timestamp < CACHE_DURATION) {
            vehicleNameMapping = data;
            return;
        }
    }
    
    // Buscar do servidor
    const response = await fetch('/api/vehicles/name-mapping');
    const data = await response.json();
    if (data.ok) {
        vehicleNameMapping = data.mapping;
        // Guardar em cache
        localStorage.setItem(CACHE_KEY, JSON.stringify({
            data: data.mapping,
            timestamp: Date.now()
        }));
    }
}
```

## Notas

- O endpoint não requer autenticação (público)
- Atualizar o mapeamento sempre que adicionar novos veículos
- O clean name sempre retorna capitalizado (Fiat Panda)
- Manter originalCar para debugging se necessário
