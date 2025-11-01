#!/bin/bash
# Test login and homepage
echo "=== Testing Login ==="
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin" \
  -c cookies.txt -b cookies.txt -L -s -o /dev/null -w "Status: %{http_code}\n"

echo ""
echo "=== Testing Homepage after login ==="
curl http://localhost:8000/ -b cookies.txt -s | grep -o "<title>[^<]*</title>"

echo ""
echo "=== Testing API with auth ==="
curl -X POST http://localhost:8000/api/track-by-params \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"location":"Aeroporto de Faro","start_date":"2025-02-01","start_time":"15:00","days":7,"lang":"pt","currency":"EUR"}' \
  -s | python3 -c "import sys, json; d=json.load(sys.stdin); print('OK:', d.get('ok'), '| Error:', d.get('error', 'None'))"
