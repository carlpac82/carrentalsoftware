#!/usr/bin/env python3
"""
Script para ler e processar ficheiro Excel de automação de preços
"""

import pandas as pd
import sys
import os

def read_excel_file(filepath):
    """Lê e processa ficheiro Excel"""
    try:
        print(f"\n📂 A ler ficheiro: {filepath}")
        print("=" * 60)
        
        # Ler Excel
        df = pd.read_excel(filepath)
        
        print(f"\n✅ Ficheiro carregado com sucesso!")
        print(f"📊 Total de linhas: {len(df)}")
        print(f"📋 Colunas encontradas: {list(df.columns)}")
        
        print("\n" + "=" * 60)
        print("PREVIEW DOS DADOS (primeiras 10 linhas):")
        print("=" * 60)
        print(df.head(10).to_string())
        
        print("\n" + "=" * 60)
        print("ESTATÍSTICAS:")
        print("=" * 60)
        
        # Verificar colunas esperadas
        expected_cols = ['Categoria', 'Localização', 'Dias', 'Preço Base', 'Margem (%)', 'Preço Final']
        missing_cols = [col for col in expected_cols if col not in df.columns]
        
        if missing_cols:
            print(f"\n⚠️  Colunas em falta: {missing_cols}")
        else:
            print(f"\n✅ Todas as colunas esperadas estão presentes!")
        
        # Estatísticas por categoria
        if 'Categoria' in df.columns:
            print(f"\n📊 Distribuição por Categoria:")
            print(df['Categoria'].value_counts().to_string())
        
        # Estatísticas por localização
        if 'Localização' in df.columns or 'Localizacao' in df.columns:
            loc_col = 'Localização' if 'Localização' in df.columns else 'Localizacao'
            print(f"\n📍 Distribuição por Localização:")
            print(df[loc_col].value_counts().to_string())
        
        # Estatísticas por dias
        if 'Dias' in df.columns:
            print(f"\n📅 Distribuição por Dias:")
            print(df['Dias'].value_counts().sort_index().to_string())
        
        # Estatísticas de preços
        if 'Preço Base' in df.columns or 'Preco Base' in df.columns:
            price_col = 'Preço Base' if 'Preço Base' in df.columns else 'Preco Base'
            print(f"\n💰 Estatísticas de Preço Base:")
            print(f"   Mínimo: {df[price_col].min():.2f}€")
            print(f"   Máximo: {df[price_col].max():.2f}€")
            print(f"   Média: {df[price_col].mean():.2f}€")
            print(f"   Mediana: {df[price_col].median():.2f}€")
        
        print("\n" + "=" * 60)
        print("DADOS COMPLETOS (JSON):")
        print("=" * 60)
        
        # Converter para lista de dicionários
        data = []
        for idx, row in df.iterrows():
            item = {
                'linha': idx + 2,  # +2 porque Excel começa em 1 e tem header
                'categoria': str(row.get('Categoria', '')),
                'localizacao': str(row.get('Localização', row.get('Localizacao', ''))),
                'dias': int(row.get('Dias', 0)) if pd.notna(row.get('Dias')) else 0,
                'preco_base': float(row.get('Preço Base', row.get('Preco Base', 0))) if pd.notna(row.get('Preço Base', row.get('Preco Base'))) else 0,
                'margem': float(row.get('Margem (%)', row.get('Margem', 0))) if pd.notna(row.get('Margem (%)', row.get('Margem'))) else 0,
                'preco_final': float(row.get('Preço Final', row.get('Preco Final', 0))) if pd.notna(row.get('Preço Final', row.get('Preco Final'))) else 0
            }
            data.append(item)
            print(f"\nLinha {item['linha']}: {item}")
        
        print("\n" + "=" * 60)
        print(f"✅ PROCESSAMENTO COMPLETO: {len(data)} registos")
        print("=" * 60)
        
        return data
        
    except FileNotFoundError:
        print(f"❌ Erro: Ficheiro não encontrado: {filepath}")
        print(f"\n💡 Certifique-se que o ficheiro está no caminho correto.")
        return None
    except Exception as e:
        print(f"❌ Erro ao processar ficheiro: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Uso: python read_excel.py <caminho_para_ficheiro.xlsx>")
        print("\n💡 Exemplo:")
        print("   python read_excel.py 'Brokers Albufeira.xlsx'")
        print("   python read_excel.py ~/Downloads/Brokers\\ Albufeira.xlsx")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    # Se o ficheiro não existe, tentar procurar em localizações comuns
    if not os.path.exists(filepath):
        common_paths = [
            os.path.expanduser(f"~/Downloads/{filepath}"),
            os.path.expanduser(f"~/Desktop/{filepath}"),
            os.path.join(os.getcwd(), filepath)
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                filepath = path
                break
    
    data = read_excel_file(filepath)
    
    if data:
        print(f"\n✅ Ficheiro processado com sucesso!")
        print(f"📊 Total de registos: {len(data)}")
