#!/usr/bin/env python3
"""
Processar dados completos do Excel Brokers Albufeira
- Incluir 60 dias (coluna AL/40)
- Ler comissão da célula AP3 (13.66%)
- Calcular Preço NET = Preço Final / (1 + comissão)
"""

import pandas as pd
import sys
import sqlite3

def process_brokers_complete(filepath):
    """Processa dados completos do Excel Brokers"""
    try:
        print(f"\n📂 A processar: {filepath}")
        print("=" * 80)
        
        # Ler Excel
        df = pd.read_excel(filepath)
        
        # Ler comissão da linha 1, coluna 41 (AP3)
        comissao = df.iloc[1, 41] if len(df.columns) > 41 else 0.1366
        comissao_pct = comissao * 100
        
        print(f"💰 Comissão encontrada: {comissao_pct:.2f}% (célula AP3)")
        
        # Encontrar linha com "GRUPOS"
        grupos_row = None
        for idx, row in df.iterrows():
            if 'GRUPOS' in str(row.values):
                grupos_row = idx
                break
        
        if grupos_row is None:
            print("❌ Linha 'GRUPOS' não encontrada")
            return None, None
        
        print(f"✅ Linha 'GRUPOS' encontrada: {grupos_row}")
        
        # Extrair header com dias (incluindo 60)
        header_row = df.iloc[grupos_row]
        
        # Encontrar colunas com números (dias) - INCLUINDO 60
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
                preco_final_cliente = row.iloc[col_idx + 1] if (col_idx + 1) < len(row) else None
                
                # Se 60 dias não tem valor, pular
                if dias == 60 and (not pd.notna(preco_final_cliente) or preco_final_cliente == 0):
                    continue
                
                if pd.notna(preco_base) and preco_base > 0:
                    # Calcular Preço NET (remover comissão do preço final)
                    preco_net = 0
                    if pd.notna(preco_final_cliente) and preco_final_cliente > 0:
                        preco_net = preco_final_cliente / (1 + comissao)
                    
                    # Calcular margem sobre o NET
                    margem_pct = 0
                    if preco_net > 0 and preco_base > 0:
                        margem_pct = ((preco_net - preco_base) / preco_base) * 100
                    
                    item = {
                        'grupo': grupo,
                        'localizacao': 'Albufeira',
                        'dias': dias,
                        'preco_base': round(float(preco_base), 2),
                        'preco_net': round(float(preco_net), 2),
                        'preco_final_cliente': round(float(preco_final_cliente), 2) if pd.notna(preco_final_cliente) else 0,
                        'comissao_pct': round(comissao_pct, 2),
                        'margem_pct': round(margem_pct, 2)
                    }
                    
                    data.append(item)
        
        print(f"\n{'='*80}")
        print(f"✅ PROCESSAMENTO COMPLETO")
        print(f"{'='*80}")
        print(f"📊 Total de registos: {len(data)}")
        print(f"✅ Grupos processados ({len(grupos_processados)}): {sorted(grupos_processados)}")
        print(f"⏭️  Grupos ignorados ({len(grupos_ignorados)}): {sorted(grupos_ignorados)}")
        
        # Mostrar exemplos com cálculos
        print(f"\n{'='*80}")
        print(f"💰 EXEMPLO DE CÁLCULOS (Grupo B1):")
        print(f"{'='*80}")
        print(f"Comissão: {comissao_pct:.2f}%")
        print(f"\n{'Dias':<5} {'Base':<8} {'Final':<8} {'NET':<8} {'Margem':<8}")
        print(f"{'-'*5} {'-'*8} {'-'*8} {'-'*8} {'-'*8}")
        
        b1_data = [d for d in data if d['grupo'] == 'B1'][:5]
        for item in b1_data:
            print(f"{item['dias']:<5d} {item['preco_base']:>7.2f}€ {item['preco_final_cliente']:>7.2f}€ {item['preco_net']:>7.2f}€ {item['margem_pct']:>6.1f}%")
        
        # Estatísticas gerais
        if data:
            print(f"\n{'='*80}")
            print(f"📊 ESTATÍSTICAS GERAIS:")
            print(f"{'='*80}")
            print(f"   Total registos: {len(data)}")
            print(f"   Grupos únicos: {len(grupos_processados)}")
            print(f"   Dias únicos: {sorted(set(d['dias'] for d in data))}")
            print(f"   Preço NET Mínimo: {min(d['preco_net'] for d in data if d['preco_net'] > 0):.2f}€")
            print(f"   Preço NET Máximo: {max(d['preco_net'] for d in data):.2f}€")
            print(f"   Preço NET Médio: {sum(d['preco_net'] for d in data)/len(data):.2f}€")
        
        return data, comissao_pct
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return None, None

def save_to_database(data, comissao_pct, db_path="carrental.db"):
    """Guarda dados na base de dados"""
    try:
        print(f"\n{'='*80}")
        print(f"💾 A guardar na base de dados: {db_path}")
        print(f"{'='*80}")
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Criar tabela de preços dos brokers
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS broker_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                grupo TEXT NOT NULL,
                localizacao TEXT NOT NULL,
                dias INTEGER NOT NULL,
                preco_base REAL NOT NULL,
                preco_net REAL NOT NULL,
                preco_final_cliente REAL NOT NULL,
                comissao_pct REAL NOT NULL,
                margem_pct REAL NOT NULL,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(grupo, localizacao, dias)
            )
        """)
        
        # Criar tabela de configurações
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS automation_settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Guardar comissão nas configurações
        cursor.execute("""
            INSERT OR REPLACE INTO automation_settings (key, value)
            VALUES ('comissao_broker_pct', ?)
        """, (str(comissao_pct),))
        
        # Limpar dados antigos
        cursor.execute("DELETE FROM broker_prices WHERE localizacao = 'Albufeira'")
        
        # Inserir novos dados
        for item in data:
            cursor.execute("""
                INSERT INTO broker_prices 
                (grupo, localizacao, dias, preco_base, preco_net, preco_final_cliente, comissao_pct, margem_pct)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item['grupo'],
                item['localizacao'],
                item['dias'],
                item['preco_base'],
                item['preco_net'],
                item['preco_final_cliente'],
                item['comissao_pct'],
                item['margem_pct']
            ))
        
        conn.commit()
        conn.close()
        
        print(f"✅ {len(data)} registos guardados com sucesso!")
        print(f"✅ Comissão {comissao_pct:.2f}% guardada nas configurações")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao guardar: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    filepath = sys.argv[1] if len(sys.argv) > 1 else "Brokers Albufeira.xlsx"
    data, comissao = process_brokers_complete(filepath)
    
    if data and comissao:
        print(f"\n✅ Sucesso! {len(data)} registos processados.")
        
        # Perguntar se quer guardar
        save = input("\n💾 Guardar na base de dados? (s/n): ").lower().strip()
        if save == 's':
            save_to_database(data, comissao)
