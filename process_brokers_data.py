#!/usr/bin/env python3
"""
Processar dados do Excel Brokers Albufeira
- Coluna A: Grupos (ignorar os que têm K)
- Linha 4: Número de dias (1,2,3,4,5,6,7,8,9,14,22,28,31,60)
"""

import pandas as pd
import sys

def process_brokers_data(filepath):
    """Processa dados do Excel Brokers"""
    try:
        print(f"\n📂 A processar: {filepath}")
        print("=" * 80)
        
        # Ler Excel
        df = pd.read_excel(filepath)
        
        # Encontrar linha com "GRUPOS"
        grupos_row = None
        for idx, row in df.iterrows():
            if 'GRUPOS' in str(row.values):
                grupos_row = idx
                break
        
        if grupos_row is None:
            print("❌ Linha 'GRUPOS' não encontrada")
            return None
        
        print(f"✅ Linha 'GRUPOS' encontrada: {grupos_row}")
        
        # Extrair header com dias
        header_row = df.iloc[grupos_row]
        
        # Encontrar colunas com números (dias)
        dias_cols = []
        for col_idx, val in enumerate(header_row):
            try:
                if pd.notna(val) and float(val) > 0 and float(val) <= 60:
                    dias_cols.append((col_idx, int(float(val))))
            except:
                pass
        
        print(f"📅 Dias encontrados: {[d[1] for d in dias_cols]}")
        
        # Processar dados
        data = []
        grupos_processados = set()
        grupos_ignorados = set()
        
        # Começar a ler a partir da linha seguinte ao GRUPOS
        for idx in range(grupos_row + 1, len(df)):
            row = df.iloc[idx]
            
            # Primeira coluna tem o grupo/categoria
            grupo = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ''
            
            if not grupo or grupo == 'nan':
                continue
            
            # IGNORAR grupos com "K"
            if 'K' in grupo.upper():
                grupos_ignorados.add(grupo)
                continue
            
            grupos_processados.add(grupo)
            
            # Para cada dia, extrair os preços
            for col_idx, dias in dias_cols:
                # Preço base está na coluna do dia
                preco_base = row.iloc[col_idx] if col_idx < len(row) else None
                
                # Preço com margem está na coluna seguinte
                preco_margem = row.iloc[col_idx + 1] if (col_idx + 1) < len(row) else None
                
                if pd.notna(preco_base) and preco_base > 0:
                    # Calcular margem
                    margem_pct = 0
                    if pd.notna(preco_margem) and preco_margem > 0 and preco_base > 0:
                        margem_pct = ((preco_margem - preco_base) / preco_base) * 100
                    
                    item = {
                        'grupo': grupo,
                        'localizacao': 'Albufeira',
                        'dias': dias,
                        'preco_base': round(float(preco_base), 2),
                        'preco_final': round(float(preco_margem), 2) if pd.notna(preco_margem) else 0,
                        'margem_pct': round(margem_pct, 2)
                    }
                    
                    data.append(item)
        
        print(f"\n{'='*80}")
        print(f"✅ PROCESSAMENTO COMPLETO")
        print(f"{'='*80}")
        print(f"📊 Total de registos: {len(data)}")
        print(f"✅ Grupos processados ({len(grupos_processados)}): {sorted(grupos_processados)}")
        print(f"⏭️  Grupos ignorados ({len(grupos_ignorados)}): {sorted(grupos_ignorados)}")
        
        # Estatísticas por grupo
        print(f"\n{'='*80}")
        print(f"📊 DADOS POR GRUPO:")
        print(f"{'='*80}")
        
        for grupo in sorted(grupos_processados):
            grupo_data = [d for d in data if d['grupo'] == grupo]
            if grupo_data:
                print(f"\n🏷️  {grupo}: {len(grupo_data)} registos")
                print(f"   Dias: {sorted(set(d['dias'] for d in grupo_data))}")
                print(f"   Preço Base: {min(d['preco_base'] for d in grupo_data):.2f}€ - {max(d['preco_base'] for d in grupo_data):.2f}€")
                
                # Mostrar alguns exemplos
                exemplos = [d for d in grupo_data if d['dias'] in [1, 7, 14, 28]]
                for ex in exemplos:
                    print(f"      {ex['dias']:2d}d: Base={ex['preco_base']:6.2f}€  Final={ex['preco_final']:7.2f}€  Margem={ex['margem_pct']:5.1f}%")
        
        # Estatísticas gerais
        if data:
            print(f"\n{'='*80}")
            print(f"📊 ESTATÍSTICAS GERAIS:")
            print(f"{'='*80}")
            print(f"   Total registos: {len(data)}")
            print(f"   Grupos únicos: {len(grupos_processados)}")
            print(f"   Dias únicos: {sorted(set(d['dias'] for d in data))}")
            print(f"   Preço Base Mínimo: {min(d['preco_base'] for d in data):.2f}€")
            print(f"   Preço Base Máximo: {max(d['preco_base'] for d in data):.2f}€")
            print(f"   Preço Base Médio: {sum(d['preco_base'] for d in data)/len(data):.2f}€")
        
        return data
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    filepath = sys.argv[1] if len(sys.argv) > 1 else "Brokers Albufeira.xlsx"
    data = process_brokers_data(filepath)
    
    if data:
        print(f"\n✅ Sucesso! {len(data)} registos prontos.")
        print(f"\n💡 Próximo passo: Guardar na base de dados para automação de preços")
