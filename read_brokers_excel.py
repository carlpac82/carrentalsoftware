#!/usr/bin/env python3
"""
Script para ler ficheiro Excel de Brokers com estrutura específica
"""

import pandas as pd
import sys

def read_brokers_excel(filepath):
    """Lê ficheiro Excel de Brokers Albufeira"""
    try:
        print(f"\n📂 A ler ficheiro: {filepath}")
        print("=" * 80)
        
        # Ler Excel
        df = pd.read_excel(filepath)
        
        print(f"\n✅ Ficheiro carregado!")
        print(f"📊 Dimensões: {df.shape[0]} linhas x {df.shape[1]} colunas")
        
        # Encontrar linha com "GRUPOS" que indica o header
        grupos_row = None
        for idx, row in df.iterrows():
            if 'GRUPOS' in str(row.values):
                grupos_row = idx
                break
        
        if grupos_row is None:
            print("❌ Não encontrei a linha 'GRUPOS'")
            return None
        
        print(f"\n📍 Linha 'GRUPOS' encontrada: {grupos_row}")
        
        # Extrair dados a partir da linha GRUPOS
        # A linha GRUPOS tem os números de dias
        header_row = df.iloc[grupos_row]
        
        # Encontrar colunas com números (dias)
        dias_cols = []
        for col_idx, val in enumerate(header_row):
            try:
                if pd.notna(val) and float(val) > 0 and float(val) <= 60:
                    dias_cols.append((col_idx, int(float(val))))
            except:
                pass
        
        print(f"\n📅 Dias encontrados: {[d[1] for d in dias_cols]}")
        
        # Processar dados
        data = []
        
        # Começar a ler a partir da linha seguinte ao GRUPOS
        for idx in range(grupos_row + 1, len(df)):
            row = df.iloc[idx]
            
            # Primeira coluna deve ter o grupo/categoria
            grupo = str(row.iloc[0]) if pd.notna(row.iloc[0]) else ''
            
            if not grupo or grupo == 'nan':
                continue
            
            print(f"\n{'='*80}")
            print(f"🏷️  GRUPO: {grupo}")
            print(f"{'='*80}")
            
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
                        'dias': dias,
                        'preco_base': round(float(preco_base), 2),
                        'preco_final': round(float(preco_margem), 2) if pd.notna(preco_margem) else 0,
                        'margem_pct': round(margem_pct, 2)
                    }
                    
                    data.append(item)
                    
                    print(f"  {dias:2d} dias: Base={item['preco_base']:7.2f}€  "
                          f"Final={item['preco_final']:7.2f}€  "
                          f"Margem={item['margem_pct']:5.2f}%")
        
        print(f"\n{'='*80}")
        print(f"✅ TOTAL: {len(data)} registos processados")
        print(f"{'='*80}")
        
        # Estatísticas
        if data:
            print(f"\n📊 ESTATÍSTICAS:")
            print(f"   Grupos únicos: {len(set(d['grupo'] for d in data))}")
            print(f"   Dias únicos: {sorted(set(d['dias'] for d in data))}")
            print(f"   Preço mínimo: {min(d['preco_base'] for d in data):.2f}€")
            print(f"   Preço máximo: {max(d['preco_base'] for d in data):.2f}€")
            print(f"   Preço médio: {sum(d['preco_base'] for d in data)/len(data):.2f}€")
            print(f"   Margem média: {sum(d['margem_pct'] for d in data)/len(data):.2f}%")
        
        return data
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    filepath = sys.argv[1] if len(sys.argv) > 1 else "Brokers Albufeira.xlsx"
    data = read_brokers_excel(filepath)
    
    if data:
        print(f"\n✅ Sucesso! {len(data)} registos prontos para usar.")
