#!/usr/bin/env python3
"""
Teste direto para diagnosticar porque Albufeira não funciona
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Set environment
os.environ['TEST_MODE_LOCAL'] = '0'

from datetime import datetime, timedelta
import asyncio

async def test_albufeira():
    print("=" * 60)
    print("TESTE DIRETO - ALBUFEIRA")
    print("=" * 60)
    
    # Import after env is set
    from main import track_by_params_internal
    
    # Test parameters
    location = "Albufeira"
    start_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
    days = 1
    
    print(f"\nTestando:")
    print(f"  Location: {location}")
    print(f"  Date: {start_date}")
    print(f"  Days: {days}")
    print()
    
    try:
        # Call internal function
        result = await track_by_params_internal(
            location=location,
            start_date=start_date,
            start_time="10:00",
            days=days,
            lang="pt",
            currency="EUR"
        )
        
        print(f"\n✅ RESULTADO:")
        print(f"  Items: {len(result.get('items', []))}")
        
        if result.get('items'):
            print(f"  Primeiro carro: {result['items'][0].get('car')}")
            print(f"  Primeiro preço: {result['items'][0].get('price')}")
        else:
            print("  ⚠️ NENHUM ITEM RETORNADO!")
            print(f"  Warning: {result.get('warning', 'N/A')}")
            print(f"  Error: {result.get('error', 'N/A')}")
            
    except Exception as e:
        print(f"\n❌ ERRO:")
        print(f"  {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_albufeira())
