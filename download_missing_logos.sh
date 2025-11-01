#!/bin/bash

# Script para descarregar logos em falta do CarJet
# Logos encontrados no site: https://www.carjet.com/cdn/img/prv/flat/mid/

cd "$(dirname "$0")/static/logos"

# Base URL do CarJet
BASE_URL="https://www.carjet.com/cdn/img/prv/flat/mid"

# Lista de logos que faltam (comparando com os 51 encontrados vs 20 que temos)
MISSING_LOGOS=(
  "logo_ABB1.png"
  "logo_AIR.png"
  "logo_AMI1.png"
  "logo_ATR.png"
  "logo_AUU.png"
  "logo_AVX.png"
  "logo_BSD.png"
  "logo_CAE.png"
  "logo_DOY.png"
  "logo_DTG.png"
  "logo_DTG1.png"
  "logo_DVM.png"
  "logo_ENT.png"
  "logo_EPI.png"
  "logo_EU2.png"
  "logo_EUK.png"
  "logo_FFX.png"
  "logo_GMO.png"
  "logo_GMO1.png"
  "logo_GUE.png"
  "logo_KLA.png"
  "logo_LOC.png"
  "logo_MVY.png"
  "logo_NAT.png"
  "logo_OKR1.png"
  "logo_PAR.png"
  "logo_REC.png"
  "logo_RNA.png"
  "logo_SAD.png"
  "logo_SVN.png"
  "logo_SXT.png"
  "logo_YES.png"
)

echo "🔽 Descarregando ${#MISSING_LOGOS[@]} logos em falta..."
echo ""

SUCCESS=0
FAILED=0

for logo in "${MISSING_LOGOS[@]}"; do
  echo -n "Descarregando $logo... "
  
  # Tentar descarregar
  if curl -s -f -o "$logo" "${BASE_URL}/${logo}"; then
    echo "✅"
    ((SUCCESS++))
  else
    echo "❌ (não encontrado)"
    ((FAILED++))
    rm -f "$logo" 2>/dev/null
  fi
done

echo ""
echo "📊 Resumo:"
echo "   ✅ Sucesso: $SUCCESS"
echo "   ❌ Falhou: $FAILED"
echo ""
echo "📁 Total de logos agora: $(ls -1 logo_*.* 2>/dev/null | wc -l)"
