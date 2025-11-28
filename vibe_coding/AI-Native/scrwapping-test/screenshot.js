const puppeteer = require('puppeteer');

(async () => {
  console.log('브라우저 실행 중...');

  // 브라우저 실행
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  console.log('새 페이지 열기...');
  const page = await browser.newPage();

  // 뷰포트 크기 설정
  await page.setViewport({ width: 1920, height: 1080 });

  console.log('구글 홈페이지 접속 중...');
  await page.goto('https://www.google.com', {
    waitUntil: 'networkidle2'
  });

  // 페이지 제목 추출
  const title = await page.title();
  console.log('페이지 제목:', title);

  // 스크린샷 저장
  const screenshotPath = './google_screenshot.png';
  await page.screenshot({ path: screenshotPath, fullPage: true });
  console.log(`스크린샷이 저장되었습니다: ${screenshotPath}`);

  // 브라우저 종료
  await browser.close();
  console.log('완료!');
})();
