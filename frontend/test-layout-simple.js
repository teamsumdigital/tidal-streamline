import puppeteer from 'puppeteer';

async function testLayoutSimple() {
  const browser = await puppeteer.launch({ 
    headless: false,
    defaultViewport: { width: 1600, height: 1000 }
  });
  
  const page = await browser.newPage();
  
  try {
    console.log('🚀 Testing layout with completed scan...');
    
    // Navigate directly to a completed scan
    const scanId = '6b18da2a-f25f-43a7-b51c-b9f95e78b6d3'; // From the API response
    await page.goto(`http://localhost:3008/scan/${scanId}`, { waitUntil: 'networkidle2' });
    console.log('✅ Loaded results page');
    
    // Wait a moment for any dynamic content to load
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Check for flex layout
    const grid = await page.$('.flex.flex-row');
    if (grid) {
      console.log('✅ Found flex row layout');
      
      // Check main content area
      const mainContent = await page.$('.flex-\\[2\\]');
      if (mainContent) {
        console.log('✅ Found main content area (spans 2 columns)');
        
        // Check salary cards
        const salaryCardsContainer = await page.$('.grid.grid-cols-1.md\\:grid-cols-2.xl\\:grid-cols-4');
        if (salaryCardsContainer) {
          console.log('✅ Found salary cards container');
          
          // Get all region cards and their order
          const regionTexts = await page.$$eval('.grid.grid-cols-1.md\\:grid-cols-2.xl\\:grid-cols-4 > div', 
            cards => cards.map(card => {
              const regionElement = card.querySelector('h3');
              return regionElement ? regionElement.textContent.trim() : null;
            }).filter(Boolean)
          );
          
          console.log('💰 Region cards found:', regionTexts);
          
          if (regionTexts.includes('United States') && regionTexts[0] === 'United States') {
            console.log('✅ United States is correctly positioned first');
          } else if (regionTexts.includes('United States')) {
            console.log('⚠️ United States found but not first. Order:', regionTexts);
          } else {
            console.log('❌ United States not found in regions');
          }
          
          // Check card dimensions
          const cardInfo = await page.$$eval('.grid.grid-cols-1.md\\:grid-cols-2.xl\\:grid-cols-4 > div', 
            cards => cards.map(card => {
              const rect = card.getBoundingClientRect();
              return { 
                width: Math.round(rect.width), 
                height: Math.round(rect.height),
                hasMinHeight: card.classList.contains('min-h-[200px]') || window.getComputedStyle(card).minHeight !== 'auto'
              };
            })
          );
          
          console.log('📏 Card dimensions:', cardInfo);
          
          if (cardInfo.length > 0 && cardInfo[0].width > 250) {
            console.log('✅ Cards have good width (>250px)');
          } else {
            console.log('⚠️ Cards might be too narrow');
          }
        } else {
          console.log('❌ Salary cards container not found');
        }
      } else {
        console.log('❌ Main content area not found');
      }
      
      // Check sidebar
      const sidebar = await page.$('.max-w-sm');
      if (sidebar) {
        console.log('✅ Found sidebar (spans 1 column)');
        
        // Check for "How Tidal Hires" content
        const tidalHiresHeading = await page.$('h3');
        const tidalHiresFound = await page.evaluate(() => {
          const headings = Array.from(document.querySelectorAll('h3'));
          return headings.some(h => h.textContent.includes('How Tidal Hires'));
        });
        
        if (tidalHiresFound) {
          console.log('✅ Found "How Tidal Hires" section');
          
          // Check if it's in the sidebar
          const sidebarBounds = await page.evaluate(el => {
            const rect = el.getBoundingClientRect();
            return { x: rect.x, width: rect.width, left: rect.left };
          }, sidebar);
          
          console.log(`📏 Sidebar bounds: x=${sidebarBounds.x}, width=${sidebarBounds.width}`);
          
          // Check positioning - sidebar should be on the right side of a 1600px viewport
          if (sidebarBounds.x > 1000) {
            console.log('✅ Sidebar is correctly positioned on the right side');
          } else {
            console.log('⚠️ Sidebar positioning might be off. Expected x > 1000, got:', sidebarBounds.x);
          }
          
          // Check for the three sections
          const robustEval = await page.evaluate(() => {
            return Array.from(document.querySelectorAll('h4')).some(h => h.textContent.includes('Robust Evaluation Process'));
          });
          
          const intangibles = await page.evaluate(() => {
            return Array.from(document.querySelectorAll('h4')).some(h => h.textContent.includes('Intangibles We Look For'));
          });
          
          const guarantee = await page.evaluate(() => {
            return Array.from(document.querySelectorAll('h4')).some(h => h.textContent.includes('6 Month Guarantee'));
          });
          
          console.log('📝 Sidebar sections found:');
          console.log(`   - Robust Evaluation Process: ${robustEval ? '✅' : '❌'}`);
          console.log(`   - Intangibles We Look For: ${intangibles ? '✅' : '❌'}`);
          console.log(`   - 6 Month Guarantee: ${guarantee ? '✅' : '❌'}`);
          
        } else {
          console.log('❌ "How Tidal Hires" section not found');
        }
      } else {
        console.log('❌ Sidebar not found');
      }
    } else {
      console.log('❌ Grid layout not found');
      
      // Check what's actually on the page
      const bodyContent = await page.$eval('body', el => el.textContent.substring(0, 500));
      console.log('🔍 Page content preview:', bodyContent);
    }
    
    // Take a screenshot for verification
    await page.screenshot({ path: 'layout-verification.png', fullPage: true });
    console.log('📸 Screenshot saved as layout-verification.png');
    
    console.log('🎉 Layout test completed!');
    
  } catch (error) {
    console.error('❌ Test failed:', error);
  }
  
  // Keep browser open for 10 seconds for manual inspection
  console.log('🔍 Browser will stay open for 10 seconds for manual inspection...');
  await new Promise(resolve => setTimeout(resolve, 10000));
  
  await browser.close();
}

testLayoutSimple();