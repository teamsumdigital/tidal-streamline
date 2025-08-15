import puppeteer from 'puppeteer';

async function finalTest() {
  const browser = await puppeteer.launch({ 
    headless: false,
    defaultViewport: { width: 1600, height: 1000 }
  });
  
  const page = await browser.newPage();
  
  try {
    console.log('🎯 FINAL COMPREHENSIVE TEST');
    console.log('================================');
    
    const scanId = '6b18da2a-f25f-43a7-b51c-b9f95e78b6d3';
    await page.goto(`http://localhost:3008/scan/${scanId}`, { waitUntil: 'networkidle2' });
    
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    // Test 1: Check United States positioning
    const regionOrder = await page.$$eval('.grid.grid-cols-1.sm\\:grid-cols-2.lg\\:grid-cols-3 > div', 
      cards => cards.map(card => {
        const regionElement = card.querySelector('h3');
        return regionElement ? regionElement.textContent.trim() : null;
      }).filter(Boolean)
    );
    
    console.log('💰 SALARY CARDS:');
    console.log(`   Order: ${regionOrder.join(' → ')}`);
    if (regionOrder[0] === 'United States') {
      console.log('   ✅ United States is first');
    } else {
      console.log('   ❌ United States is not first');
    }
    
    // Test 2: Check card widths
    const cardWidths = await page.$$eval('.grid.grid-cols-1.sm\\:grid-cols-2.lg\\:grid-cols-3 > div', 
      cards => cards.map(card => Math.round(card.getBoundingClientRect().width))
    );
    
    console.log(`   Card widths: ${cardWidths.join('px, ')}px`);
    if (cardWidths[0] > 250) {
      console.log('   ✅ Cards are wide enough (>250px)');
    } else {
      console.log('   ❌ Cards too narrow (<250px)');
    }
    
    // Test 3: Check sidebar positioning
    const layoutInfo = await page.evaluate(() => {
      const container = document.querySelector('[style*="display: grid"]');
      const mainContent = document.querySelector('[style*="display: grid"] > div:first-child');
      const sidebar = document.querySelector('[style*="width: 320px"]');
      
      const getPos = (el) => {
        if (!el) return null;
        const rect = el.getBoundingClientRect();
        return {
          x: Math.round(rect.x),
          y: Math.round(rect.y),
          width: Math.round(rect.width),
          height: Math.round(rect.height)
        };
      };
      
      return {
        container: getPos(container),
        mainContent: getPos(mainContent),
        sidebar: getPos(sidebar)
      };
    });
    
    console.log('🏗️ LAYOUT POSITIONING:');
    console.log(`   Container: x=${layoutInfo.container?.x}, width=${layoutInfo.container?.width}`);
    console.log(`   Main: x=${layoutInfo.mainContent?.x}, width=${layoutInfo.mainContent?.width}`);
    console.log(`   Sidebar: x=${layoutInfo.sidebar?.x}, width=${layoutInfo.sidebar?.width}`);
    
    // Calculate expected sidebar position
    const expectedSidebarX = (layoutInfo.container?.x || 0) + (layoutInfo.mainContent?.width || 0) + 32; // gap-8 = 32px
    console.log(`   Expected sidebar x: ${expectedSidebarX}`);
    
    if (layoutInfo.sidebar && layoutInfo.sidebar.x > layoutInfo.mainContent?.x + 200) {
      console.log('   ✅ Sidebar is positioned to the right of main content');
    } else {
      console.log('   ❌ Sidebar is not positioned correctly');
    }
    
    // Test 4: Check "How Tidal Hires" content
    const tidalSections = await page.evaluate(() => {
      const sections = [
        'Robust Evaluation Process',
        'Intangibles We Look For', 
        '6 Month Guarantee'
      ];
      
      return sections.map(section => {
        const found = Array.from(document.querySelectorAll('h4')).some(h => 
          h.textContent.includes(section)
        );
        return { section, found };
      });
    });
    
    console.log('📋 "HOW TIDAL HIRES" SECTIONS:');
    tidalSections.forEach(({ section, found }) => {
      console.log(`   ${found ? '✅' : '❌'} ${section}`);
    });
    
    // Final scoring
    const scores = {
      unitedStatesFirst: regionOrder[0] === 'United States',
      cardWidthOk: cardWidths[0] > 250,
      sidebarPositioned: layoutInfo.sidebar && layoutInfo.sidebar.x > layoutInfo.mainContent?.x + 200,
      allSectionsPresent: tidalSections.every(s => s.found)
    };
    
    const totalScore = Object.values(scores).filter(Boolean).length;
    const maxScore = Object.keys(scores).length;
    
    console.log('🏆 FINAL SCORE:');
    console.log(`   ${totalScore}/${maxScore} tests passed`);
    
    if (totalScore === maxScore) {
      console.log('   🎉 ALL TESTS PASSED! Layout is fixed!');
    } else {
      console.log('   ⚠️  Some issues remain to be fixed');
    }
    
    await page.screenshot({ path: 'final-layout-test.png', fullPage: true });
    console.log('📸 Final screenshot saved as final-layout-test.png');
    
  } catch (error) {
    console.error('❌ Test failed:', error);
  }
  
  // Keep browser open longer for final inspection
  console.log('🔍 Browser staying open for 20 seconds for final inspection...');
  await new Promise(resolve => setTimeout(resolve, 20000));
  
  await browser.close();
}

finalTest();