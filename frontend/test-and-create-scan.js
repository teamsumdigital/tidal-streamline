import puppeteer from 'puppeteer';

async function testLayoutAndCreateScan() {
  const browser = await puppeteer.launch({ 
    headless: false,
    defaultViewport: { width: 1400, height: 900 }
  });
  
  const page = await browser.newPage();
  
  try {
    console.log('🚀 Starting layout test...');
    
    // Navigate to the frontend
    await page.goto('http://localhost:3008', { waitUntil: 'networkidle2' });
    console.log('✅ Loaded frontend page');
    
    // Check if we're on the market scan form
    const hasForm = await page.$('form');
    if (hasForm) {
      console.log('📝 Found market scan form, creating a test scan...');
      
      // Fill out the form
      await page.type('input[name="client_name"]', 'Test User');
      await page.type('input[name="client_email"]', 'test@hiretidal.com');
      await page.type('input[name="company_domain"]', 'testcompany.com');
      await page.type('input[name="job_title"]', 'Shopify Admin');
      await page.type('textarea[name="job_description"]', 'We need a skilled Shopify administrator to manage our online store, handle inventory, process orders, and maintain product listings. Must have experience with Shopify platform, Excel, and customer service.');
      await page.type('textarea[name="hiring_challenges"]', 'Finding someone with the right balance of technical skills and attention to detail.');
      
      // Submit the form
      console.log('📤 Submitting form...');
      await page.click('button[type="submit"]');
      
      // Wait for redirect to results page
      await page.waitForNavigation({ waitUntil: 'networkidle2', timeout: 10000 });
      console.log('🔄 Redirected to results page');
      
      // Wait for analysis to complete (up to 60 seconds)
      console.log('🔍 Waiting for analysis to complete...');
      let attempts = 0;
      let analysisComplete = false;
      
      while (attempts < 20 && !analysisComplete) {
        await new Promise(resolve => setTimeout(resolve, 3000));
        
        // Check if analysis is complete by looking for salary cards
        const salaryCards = await page.$$('.grid.grid-cols-1.md\\:grid-cols-2.xl\\:grid-cols-4');
        if (salaryCards.length > 0) {
          analysisComplete = true;
          console.log('✅ Analysis completed!');
        } else {
          console.log(`⏳ Still analyzing... (attempt ${attempts + 1}/20)`);
          await page.reload({ waitUntil: 'networkidle2' });
        }
        attempts++;
      }
      
      if (!analysisComplete) {
        console.log('⚠️ Analysis did not complete in time, but checking layout anyway...');
      }
    }
    
    // Now check the layout regardless
    console.log('🎨 Checking layout...');
    
    // Check for grid layout
    const grid = await page.$('.grid.lg\\:grid-cols-3');
    if (grid) {
      console.log('✅ Found 3-column grid layout');
      
      // Check main content area
      const mainContent = await page.$('.lg\\:col-span-2');
      if (mainContent) {
        console.log('✅ Found main content area (2 columns)');
        
        // Check salary cards order
        const regionCards = await page.$$eval('.grid.grid-cols-1.md\\:grid-cols-2.xl\\:grid-cols-4 > div', 
          cards => cards.map(card => card.textContent.match(/United States|Philippines|Latin America|South Africa/)?.[0]).filter(Boolean));
        
        if (regionCards.length > 0) {
          console.log('💰 Found salary cards:', regionCards);
          if (regionCards[0] === 'United States') {
            console.log('✅ United States is correctly positioned first');
          } else {
            console.log('❌ United States is not first:', regionCards);
          }
        }
      }
      
      // Check sidebar
      const sidebar = await page.$('.lg\\:col-span-1');
      if (sidebar) {
        console.log('✅ Found sidebar (1 column)');
        
        // Check for "How Tidal Hires" content
        const tidalHires = await page.$('h3:has-text("How Tidal Hires")');
        if (tidalHires) {
          console.log('✅ Found "How Tidal Hires" section in sidebar');
          
          // Check if it's positioned correctly
          const sidebarBounds = await page.evaluate(el => {
            const rect = el.getBoundingClientRect();
            return { x: rect.x, width: rect.width };
          }, sidebar);
          
          console.log(`📏 Sidebar position: x=${sidebarBounds.x}, width=${sidebarBounds.width}`);
          
          if (sidebarBounds.x > 800) { // Should be on the right side
            console.log('✅ Sidebar is correctly positioned on the right');
          } else {
            console.log('❌ Sidebar positioning issue');
          }
        } else {
          console.log('❌ "How Tidal Hires" section not found');
        }
      } else {
        console.log('❌ Sidebar not found');
      }
    } else {
      console.log('❌ Grid layout not found');
    }
    
    // Take a screenshot for verification
    await page.screenshot({ path: 'layout-test.png', fullPage: true });
    console.log('📸 Screenshot saved as layout-test.png');
    
    console.log('🎉 Layout test completed!');
    
  } catch (error) {
    console.error('❌ Test failed:', error);
  }
  
  await browser.close();
}

testLayoutAndCreateScan();