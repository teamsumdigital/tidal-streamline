import puppeteer from 'puppeteer';

async function debugLayout() {
  const browser = await puppeteer.launch({ 
    headless: false,
    defaultViewport: { width: 1600, height: 1000 }
  });
  
  const page = await browser.newPage();
  
  try {
    console.log('🔍 Debugging layout in detail...');
    
    const scanId = '6b18da2a-f25f-43a7-b51c-b9f95e78b6d3';
    await page.goto(`http://localhost:3008/scan/${scanId}`, { waitUntil: 'networkidle2' });
    
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Get detailed layout information
    const layoutInfo = await page.evaluate(() => {
      const grid = document.querySelector('.flex.flex-row');
      const mainContent = document.querySelector('.flex-\\[2\\]');
      const sidebar = document.querySelector('.max-w-sm');
      
      const getElementInfo = (el, name) => {
        if (!el) return { name, exists: false };
        
        const rect = el.getBoundingClientRect();
        const computedStyle = window.getComputedStyle(el);
        
        return {
          name,
          exists: true,
          rect: {
            x: Math.round(rect.x),
            y: Math.round(rect.y),
            width: Math.round(rect.width),
            height: Math.round(rect.height)
          },
          styles: {
            display: computedStyle.display,
            gridTemplateColumns: computedStyle.gridTemplateColumns,
            gridColumn: computedStyle.gridColumn,
            position: computedStyle.position
          },
          classes: Array.from(el.classList)
        };
      };
      
      return {
        viewport: { width: window.innerWidth, height: window.innerHeight },
        grid: getElementInfo(grid, 'grid'),
        mainContent: getElementInfo(mainContent, 'mainContent'),
        sidebar: getElementInfo(sidebar, 'sidebar')
      };
    });
    
    console.log('📊 Detailed Layout Information:');
    console.log('Viewport:', layoutInfo.viewport);
    console.log('Grid:', layoutInfo.grid);
    console.log('Main Content:', layoutInfo.mainContent);
    console.log('Sidebar:', layoutInfo.sidebar);
    
    // Check if we're at the right viewport size for md breakpoint
    if (layoutInfo.viewport.width >= 768) {
      console.log('✅ Viewport is wide enough for md breakpoint (768px+)');
    } else {
      console.log('❌ Viewport too narrow for md breakpoint');
    }
    
    // Check if grid is actually using 3 columns
    if (layoutInfo.grid.exists && layoutInfo.grid.styles.gridTemplateColumns) {
      const columnCount = layoutInfo.grid.styles.gridTemplateColumns.split(' ').length;
      console.log(`📐 Grid has ${columnCount} columns`);
      
      if (columnCount === 3) {
        console.log('✅ Grid correctly has 3 columns');
      } else {
        console.log('❌ Grid does not have 3 columns');
      }
    }
    
    // Visual test - add temporary border to debug
    await page.addStyleTag({
      content: `
        .flex.flex-row { border: 3px solid red !important; }
        .flex-\\[2\\] { border: 3px solid blue !important; }
        .max-w-sm { border: 3px solid green !important; }
      `
    });
    
    console.log('🎨 Added debug borders (red=grid, blue=main, green=sidebar)');
    
    await page.screenshot({ path: 'debug-layout.png', fullPage: true });
    console.log('📸 Debug screenshot saved as debug-layout.png');
    
  } catch (error) {
    console.error('❌ Debug failed:', error);
  }
  
  // Keep browser open for manual inspection
  console.log('🔍 Browser staying open for manual inspection...');
  await new Promise(resolve => setTimeout(resolve, 15000));
  
  await browser.close();
}

debugLayout();