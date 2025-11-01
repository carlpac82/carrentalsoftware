/**
 * DATABASE SYNC - Sincronização Automática localStorage ↔ Database
 * 
 * Garante que NADA é perdido quando Render entra em sleep mode
 * Sincroniza automaticamente:
 * - AI Learning Data (priceAIData)
 * - Custom Days (customDias)
 * - Automated Price Rules (automatedPriceRules)
 * - Price Automation Settings (priceAutomationSettings)
 * 
 * USO: Incluir em todas as páginas que usam localStorage
 * <script src="/static/js/db-sync.js"></script>
 */

(function() {
    'use strict';
    
    const DB_SYNC_VERSION = '1.0.0';
    const SYNC_INTERVAL = 30000; // 30 segundos
    const KEYS_TO_SYNC = ['customDias', 'priceAIData'];
    
    console.log(`[DB-SYNC ${DB_SYNC_VERSION}] Inicializando sincronização automática...`);
    
    // ==========================================
    // LOAD FROM DATABASE
    // ==========================================
    
    async function loadFromDatabase() {
        try {
            console.log('[DB-SYNC] Carregando dados da database...');
            
            // Carregar User Settings (customDias, etc)
            const settingsResp = await fetch('/api/user-settings/load?user_key=default');
            if (settingsResp.ok) {
                const data = await settingsResp.json();
                if (data.ok && data.settings) {
                    // Aplicar ao localStorage
                    Object.entries(data.settings).forEach(([key, value]) => {
                        if (KEYS_TO_SYNC.includes(key)) {
                            const valueStr = typeof value === 'string' ? value : JSON.stringify(value);
                            localStorage.setItem(key, valueStr);
                            console.log(`[DB-SYNC] ✓ Loaded ${key} from database`);
                        }
                    });
                }
            }
            
            // Carregar AI Learning Data
            const aiResp = await fetch('/api/ai/learning/load');
            if (aiResp.ok) {
                const data = await aiResp.json();
                if (data.ok && data.adjustments) {
                    const aiData = {
                        adjustments: data.adjustments,
                        patterns: {},
                        suggestions: []
                    };
                    localStorage.setItem('priceAIData', JSON.stringify(aiData));
                    console.log(`[DB-SYNC] ✓ Loaded ${data.adjustments.length} AI adjustments from database`);
                }
            }
            
            // Carregar Automated Price Rules (já existe endpoint)
            try {
                const rulesResp = await fetch('/api/price-automation/rules/load');
                if (rulesResp.ok) {
                    const data = await rulesResp.json();
                    if (data.ok && data.rules) {
                        localStorage.setItem('automatedPriceRules', JSON.stringify(data.rules));
                        console.log(`[DB-SYNC] ✓ Loaded automated price rules from database`);
                    }
                }
            } catch (e) {
                console.warn('[DB-SYNC] Rules endpoint not available yet');
            }
            
            // Carregar Price Automation Settings (já existe endpoint)
            try {
                const settResp = await fetch('/api/price-automation/settings/load');
                if (settResp.ok) {
                    const data = await settResp.json();
                    if (data.ok && data.settings) {
                        localStorage.setItem('priceAutomationSettings', JSON.stringify(data.settings));
                        console.log(`[DB-SYNC] ✓ Loaded price automation settings from database`);
                    }
                }
            } catch (e) {
                console.warn('[DB-SYNC] Settings endpoint not available yet');
            }
            
            console.log('[DB-SYNC] ✅ Dados carregados da database com sucesso!');
            
        } catch (error) {
            console.error('[DB-SYNC] ❌ Erro ao carregar da database:', error);
        }
    }
    
    // ==========================================
    // SAVE TO DATABASE
    // ==========================================
    
    async function saveToDatabase() {
        try {
            console.log('[DB-SYNC] Salvando dados na database...');
            
            // Salvar User Settings
            const settings = {};
            KEYS_TO_SYNC.forEach(key => {
                const value = localStorage.getItem(key);
                if (value) {
                    try {
                        settings[key] = JSON.parse(value);
                    } catch {
                        settings[key] = value;
                    }
                }
            });
            
            if (Object.keys(settings).length > 0) {
                await fetch('/api/user-settings/save', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ user_key: 'default', settings })
                });
                console.log(`[DB-SYNC] ✓ Saved ${Object.keys(settings).length} settings to database`);
            }
            
            // Salvar Automated Price Rules (se modificados)
            const rulesStr = localStorage.getItem('automatedPriceRules');
            if (rulesStr) {
                try {
                    const rules = JSON.parse(rulesStr);
                    await fetch('/api/price-automation/rules/save', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ rules })
                    });
                    console.log(`[DB-SYNC] ✓ Saved automated price rules to database`);
                } catch (e) {
                    console.warn('[DB-SYNC] Rules save failed:', e.message);
                }
            }
            
            // Salvar Price Automation Settings (se modificados)
            const settingsStr = localStorage.getItem('priceAutomationSettings');
            if (settingsStr) {
                try {
                    const autoSettings = JSON.parse(settingsStr);
                    await fetch('/api/price-automation/settings/save', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ settings: autoSettings })
                    });
                    console.log(`[DB-SYNC] ✓ Saved price automation settings to database`);
                } catch (e) {
                    console.warn('[DB-SYNC] Settings save failed:', e.message);
                }
            }
            
            console.log('[DB-SYNC] ✅ Dados salvos na database com sucesso!');
            
        } catch (error) {
            console.error('[DB-SYNC] ❌ Erro ao salvar na database:', error);
        }
    }
    
    // ==========================================
    // AI LEARNING SYNC
    // ==========================================
    
    async function saveAIAdjustment(adjustment) {
        try {
            await fetch('/api/ai/learning/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ adjustment })
            });
            console.log(`[DB-SYNC] ✓ AI adjustment saved: ${adjustment.group}/${adjustment.days}d`);
        } catch (error) {
            console.error('[DB-SYNC] ❌ Erro ao salvar AI adjustment:', error);
        }
    }
    
    // Exportar para uso global
    window.dbSync = {
        load: loadFromDatabase,
        save: saveToDatabase,
        saveAIAdjustment: saveAIAdjustment,
        version: DB_SYNC_VERSION
    };
    
    // ==========================================
    // AUTO-SYNC LIFECYCLE
    // ==========================================
    
    // Carregar ao iniciar página
    document.addEventListener('DOMContentLoaded', async () => {
        console.log('[DB-SYNC] 🔄 Auto-loading from database...');
        await loadFromDatabase();
    });
    
    // Salvar periodicamente
    setInterval(async () => {
        console.log('[DB-SYNC] 🔄 Auto-saving to database...');
        await saveToDatabase();
    }, SYNC_INTERVAL);
    
    // Salvar antes de sair da página
    window.addEventListener('beforeunload', () => {
        console.log('[DB-SYNC] 💾 Saving before page unload...');
        // Usar sendBeacon para garantir que envia mesmo ao sair
        navigator.sendBeacon('/api/user-settings/save', JSON.stringify({
            user_key: 'default',
            settings: KEYS_TO_SYNC.reduce((acc, key) => {
                const value = localStorage.getItem(key);
                if (value) {
                    try {
                        acc[key] = JSON.parse(value);
                    } catch {
                        acc[key] = value;
                    }
                }
                return acc;
            }, {})
        }));
    });
    
    console.log('[DB-SYNC] ✅ Sincronização automática configurada!');
    console.log(`[DB-SYNC] Salvamento automático a cada ${SYNC_INTERVAL/1000}s`);
    
})();
