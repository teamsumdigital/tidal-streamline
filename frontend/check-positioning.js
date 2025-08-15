import puppeteer from 'puppeteer';

async function checkPositioning() {
  const browser = await puppeteer.launch({ 
    headless: false,
    defaultViewport: { width: 1600, height: 1000 }
  });
  
  const page = await browser.newPage();
  
  try {
    const scanId = '6b18da2a-f25f-43a7-b51c-b9f95e78b6d3';
    await page.goto(`http://localhost:3008/scan/${scanId}`, { waitUntil: 'networkidle2' });
    
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Add debug styles to see the layout clearly
    await page.addStyleTag({
      content: `
        .grid.grid-cols-4 { 
          border: 4px solid red !important; 
          background: rgba(255,0,0,0.1) !important;
        }
        .col-span-3 { 
          border: 4px solid blue !important; 
          background: rgba(0,0,255,0.1) !important;
        }
        .col-span-1 { 
          border: 4px solid green !important; 
          background: rgba(0,255,0,0.1) !important;
        }
        h3:contains("How Tidal Hires") {
          background: yellow !important;
        }
      `
    });
    
    // Check the exact positioning
    const positions = await page.evaluate(() => {
      const container = document.querySelector('[style*="display: grid"]');
      const main = document.querySelector('[style*="display: grid"] > div:first-child');
      const sidebar = document.querySelector('[style*="width: 320px"]');
      const tidalHires = document.querySelector('h3');
      
      const getInfo = (el, name) => {
        if (!el) return { name, found: false };
        const rect = el.getBoundingClientRect();
        const styles = window.getComputedStyle(el);
        return {
          name,
          found: true,
          x: Math.round(rect.x),
          y: Math.round(rect.y),
          width: Math.round(rect.width),
          height: Math.round(rect.height),
          display: styles.display,
          flexDirection: styles.flexDirection,
          position: styles.position
        };
      };
      
      return {
        container: getInfo(container, 'container'),
        main: getInfo(main, 'main'),
        sidebar: getInfo(sidebar, 'sidebar'),
        tidalHires: getInfo(tidalHires, 'tidalHires'),
        viewport: {
          width: window.innerWidth,
          height: window.innerHeight
        }
      };
    });
    
    console.log('🔍 CURRENT POSITIONING ANALYSIS:');
    console.log('================================');
    console.log('Viewport:', positions.viewport);
    console.log('Container:', positions.container);
    console.log('Main Content:', positions.main);
    console.log('Sidebar:', positions.sidebar);
    console.log('Tidal Hires:', positions.tidalHires);
    
    // Check if sidebar is actually to the right
    if (positions.sidebar.found && positions.main.found) {
      const sidebarIsRight = positions.sidebar.x > positions.main.x;
      const sidebarSameRow = Math.abs(positions.sidebar.y - positions.main.y) < 100;
      
      console.log('\n📐 POSITIONING ANALYSIS:');
      console.log(`Sidebar X (${positions.sidebar.x}) > Main X (${positions.main.x}): ${sidebarIsRight}`);
      console.log(`Sidebar Y (${positions.sidebar.y}) ≈ Main Y (${positions.main.y}): ${sidebarSameRow}`);
      
      if (sidebarIsRight && sidebarSameRow) {
        console.log('✅ Sidebar is correctly positioned to the right!');
      } else {
        console.log('❌ Sidebar is not positioned correctly');
        
        if (!sidebarIsRight) {
          console.log('   → Sidebar needs to move right');
        }
        if (!sidebarSameRow) {
          console.log('   → Sidebar needs to move up to same row as main content');
        }
      }
    }
    
    await page.screenshot({ path: 'positioning-debug.png', fullPage: true });
    console.log('\n📸 Debug screenshot saved as positioning-debug.png');
    
  } catch (error) {
    console.error('❌ Error:', error);
  }
  
  // Keep open for inspection
  console.log('\n⏳ Keeping browser open for 15 seconds...');
  await new Promise(resolve => setTimeout(resolve, 15000));
  
  await browser.close();
}

checkPositioning();