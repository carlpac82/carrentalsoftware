/**
 * SCRIPT: Criar Strategies Automáticas para Todos os Grupos
 * 
 * COMO USAR:
 * 1. Abrir /admin/price-automation-settings
 * 2. F12 → Console
 * 3. Copiar e colar este código completo
 * 4. Pressionar Enter
 * 5. Refresh a página (F5)
 */

(function createDefaultStrategies() {
    console.log('🚀 Creating default strategies for all groups...');
    
    const locations = ['Albufeira', 'Aeroporto de Faro'];
    const grupos = ['B1', 'B2', 'D', 'E1', 'E2', 'F', 'G', 'J1', 'J2', 'L1', 'L2', 'M1', 'M2', 'N'];
    const months = [11, 12]; // Novembro, Dezembro
    const days = [1, 2, 3, 4, 5, 6, 7, 14, 21, 30, 60, 90]; // Dias comuns
    
    // Load existing rules or create new
    let rules = JSON.parse(localStorage.getItem('automatedPriceRules') || '{}');
    
    // Default strategy: Follow Lowest Price + 0.50€
    const defaultStrategy = {
        type: 'follow_lowest',
        diffType: 'euros',
        diffValue: 0.50,
        minPriceDay: null,
        minPriceMonth: null
    };
    
    let created = 0;
    
    locations.forEach(location => {
        console.log(`📍 Processing ${location}...`);
        
        if (!rules[location]) rules[location] = {};
        
        grupos.forEach(grupo => {
            if (!rules[location][grupo]) rules[location][grupo] = { months: {} };
            if (!rules[location][grupo].months) rules[location][grupo].months = {};
            
            months.forEach(month => {
                if (!rules[location][grupo].months[month]) {
                    rules[location][grupo].months[month] = { days: {} };
                }
                
                days.forEach(day => {
                    // Only create if doesn't exist
                    if (!rules[location][grupo].months[month].days[day]) {
                        rules[location][grupo].months[month].days[day] = {
                            strategies: [{ ...defaultStrategy }]
                        };
                        created++;
                    }
                });
            });
            
            console.log(`  ✅ ${grupo}: ${months.length * days.length} configurations`);
        });
    });
    
    // Save to localStorage
    localStorage.setItem('automatedPriceRules', JSON.stringify(rules));
    
    console.log('');
    console.log('═══════════════════════════════════════════');
    console.log('✅ DEFAULT STRATEGIES CREATED SUCCESSFULLY!');
    console.log('═══════════════════════════════════════════');
    console.log(`📊 Total configurations created: ${created}`);
    console.log(`📍 Locations: ${locations.join(', ')}`);
    console.log(`🚗 Groups: ${grupos.join(', ')}`);
    console.log(`📅 Months: ${months.join(', ')}`);
    console.log(`⏱️ Days: ${days.join(', ')}`);
    console.log('');
    console.log('🔧 Default Strategy:');
    console.log('   Type: Follow Lowest Price');
    console.log('   Difference: +0.50€');
    console.log('');
    console.log('🔄 Please REFRESH the page (F5) to see changes!');
    console.log('═══════════════════════════════════════════');
    
    return {
        success: true,
        created: created,
        locations: locations.length,
        groups: grupos.length,
        months: months.length,
        days: days.length
    };
})();
