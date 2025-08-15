const puppeteer = require('puppeteer');

async function testLayout() {
  const browser = await puppeteer.launch({ 
    headless: false,
    defaultViewport: { width: 1400, height: 900 }
  });
  
  const page = await browser.newPage();
  
  try {
    // Navigate to the frontend
    await page.goto('http://localhost:3008', { waitUntil: 'networkidle0' });
    
    // Check if we can find a completed scan or need to create one
    const hasResults = await page.$('.grid.lg\\:grid-cols-3');
    
    if (!hasResults) {
      console.log('No completed scan found, need to navigate to a scan result...');
      // For now, let's check the main page structure
      const title = await page.title();
      console.log('Page title:', title);
      
      const content = await page.content();
      console.log('Page has market scan form:', content.includes('Market Scan'));
    } else {
      console.log('Found results grid!');
      
      // Check sidebar positioning
      const sidebar = await page.$('.lg\\:col-span-1');
      const sidebarRect = await page.evaluate(el => {
        const rect = el.getBoundingClientRect();
        return { width: rect.width, height: rect.height, x: rect.x, y: rect.y };
      }, sidebar);
      
      console.log('Sidebar dimensions:', sidebarRect);
    }
    
  } catch (error) {
    console.error('Test failed:', error);
  }
  
  await browser.close();
}

testLay