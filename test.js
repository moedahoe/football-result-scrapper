'use strict';

const puppeteer = require('puppeteer');

// (async function games(){
//   const browser = await puppeteer.launch();
//   const [page] = await browser.pages();
//   page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36');
//   await page.goto('https://www.flashresultats.fr/');
// 		await page.waitForSelector('.event__match')
		
// 		const sections = await page.$$('.event__match');

//         for (const section of sections){
// 			const yo = await section.$('.event__participant--home'); 
// 			const ya = await section.$('.event__participant--away');
// 			const name = await page.evaluate(yo => yo.innerText, yo);
// 			const name1 = await page.evaluate(ya => ya.innerText, ya);
// 			console.log(name + "  -  " + name1);
// 		}

// 		browser.close();
// })();

function cutAndGenerate(string){
  var cut = "";
  if(string.length <= 12){
      cut = string.substring(4, 12);
      return("https://www.flashresultats.fr/match/"+ cut + "/#tete-a-tete;overall");
    } else { 
      cut = string.substring(84, 92)
      return("https://www.flashresultats.fr/match/"+ cut + "/#statistiques-du-match;0");
      };
}


(async function main() {
  try {
    const browser = await puppeteer.launch({headless: true});
    const page = await browser.newPage();
    // page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36');
    await page.goto('https://www.flashresultats.fr/');
    await page.waitForSelector('div.event__match');
    const style = await page.$$("div.event__match");
    const link = [];
    const matchPages = [];
    for(let i = 0; i < style.length; i++) {

        await page.waitForSelector('div.event__match');
        const styleNumbers = await page.$$("div.event__match");

        const styleNumber = styleNumbers[i];

        const id = await page.evaluate(el => el.getAttribute("id"), styleNumber);
        link.push(cutAndGenerate(id));

        await page.goto(link[i]);
        await page.waitForSelector('.highlight');
        const styles = await page.$$(".highlight");

          for(const style of styles){
            const onclick = await page.evaluate(el => el.getAttribute("onclick"), style);
            const pure = await cutAndGenerate(onclick);            
            matchPages.push(pure);

            for (const matchPage of matchPages){
              await page.goto(matchPage);
              await page.waitForSelector('#detail-submenu-bookmark');
              const rows = await page.$$('.statRow');

              const domi = await page.$('.tname-home');
              const ext = await page.$('.tname-away');
              const equipeDomi = await page.evaluate(domi => domi.innerText, domi);
              const equipeExt = await page.evaluate(ext => ext.innerText, ext);
              console.log(equipeDomi + " VS " + equipeExt);

              for(const row of rows){
                const eq1 = await row.$('.statText--homeValue');
                const title = await row.$('.statText--titleValue');
                const eq2 = await row.$('.statText--awayValue');
                const equipe = await page.evaluate(eq1 => eq1.innerText, eq1);
                const equipe1 = await page.evaluate(eq2 => eq2.innerText, eq2);
                const event = await page.evaluate(title => title.innerText, title);
                console.log(equipe + " - " + event + " - " + equipe1);
            }
            }
          }
    }


    //  await page.goto(pure, { waitUntil: 'load', timeout: 0});
    
    //         await page.waitForSelector('.statRow');
    //         const rows = await page.$$('.statRow');
    //         const domi = await page.$('.tname-home');
    //         const ext = await page.$('.tname-away');
    //         const equipeDomi = await page.evaluate(domi => domi.innerText, domi);
    //         const equipeExt = await page.evaluate(ext => ext.innerText, ext);
    
    //         console.log(equipeDomi + " VS " + equipeExt)
    
 
    
  } catch (err) {
    console.error(err);
  }
})();