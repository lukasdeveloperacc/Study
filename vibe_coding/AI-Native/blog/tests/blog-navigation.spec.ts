import { test, expect } from '@playwright/test';

test.describe('Blog Navigation E2E Tests', () => {
  test.describe('1. 홈페이지 접속 및 기본 요소 확인', () => {
    test('should display homepage with portfolio title and introduction', async ({ page }) => {
      await page.goto('/');

      // 페이지 제목 확인
      await expect(page).toHaveTitle(/Next.js Portfolio Starter/);

      // 메인 포트폴리오 제목 확인
      const heading = page.getByRole('heading', { name: 'My Portfolio', level: 1 });
      await expect(heading).toBeVisible();

      // 소개 텍스트 확인 (Vim enthusiast 관련 내용)
      const introText = page.getByText(/I'm a Vim enthusiast and tab advocate/);
      await expect(introText).toBeVisible();
    });

    test('should display navigation links', async ({ page }) => {
      await page.goto('/');

      // 네비게이션 링크 확인
      const homeLink = page.getByRole('link', { name: 'home' });
      const blogLink = page.getByRole('link', { name: 'blog' });
      const deployLink = page.getByRole('link', { name: 'deploy' });

      await expect(homeLink).toBeVisible();
      await expect(blogLink).toBeVisible();
      await expect(deployLink).toBeVisible();
    });

    test('should display blog posts preview on homepage', async ({ page }) => {
      await page.goto('/');

      // 블로그 포스트 링크들이 표시되는지 확인
      const vimPost = page.getByRole('link', { name: /Embracing Vim/ });
      const spacesTabsPost = page.getByRole('link', { name: /Spaces vs\. Tabs/ });
      const staticTypingPost = page.getByRole('link', { name: /Static Typing/ });

      await expect(vimPost).toBeVisible();
      await expect(spacesTabsPost).toBeVisible();
      await expect(staticTypingPost).toBeVisible();

      // 각 포스트의 날짜가 표시되는지 확인
      await expect(page.getByText('April 9, 2024').first()).toBeVisible();
      await expect(page.getByText('April 8, 2024').first()).toBeVisible();
      await expect(page.getByText('April 7, 2024').first()).toBeVisible();
    });
  });

  test.describe('2. 블로그 목록 페이지에서 포스트 확인', () => {
    test('should navigate to blog page and display blog list', async ({ page }) => {
      await page.goto('/');

      // 네비게이션에서 blog 링크 클릭
      await page.getByRole('link', { name: 'blog' }).click();

      // URL 확인
      await expect(page).toHaveURL('/blog');

      // 페이지 제목 확인
      await expect(page).toHaveTitle(/Blog/);

      // "My Blog" 제목 확인
      const blogHeading = page.getByRole('heading', { name: 'My Blog', level: 1 });
      await expect(blogHeading).toBeVisible();
    });

    test('should display all blog posts on blog page', async ({ page }) => {
      await page.goto('/blog');

      // 모든 블로그 포스트가 표시되는지 확인
      const vimPost = page.getByRole('link', { name: /Embracing Vim/ });
      const spacesTabsPost = page.getByRole('link', { name: /Spaces vs\. Tabs/ });
      const staticTypingPost = page.getByRole('link', { name: /Static Typing/ });

      await expect(vimPost).toBeVisible();
      await expect(spacesTabsPost).toBeVisible();
      await expect(staticTypingPost).toBeVisible();
    });

    test('should display post dates and titles correctly', async ({ page }) => {
      await page.goto('/blog');

      // 날짜와 제목이 함께 표시되는지 확인
      const firstPost = page.getByRole('link', { name: /April 9, 2024.*Embracing Vim/ });
      await expect(firstPost).toBeVisible();

      // 링크가 올바른 href를 가지는지 확인
      await expect(firstPost).toHaveAttribute('href', '/blog/vim');
    });
  });

  test.describe('3. 개별 블로그 포스트 페이지 접근 및 콘텐츠 확인', () => {
    test('should navigate to individual blog post from homepage', async ({ page }) => {
      await page.goto('/');

      // 홈페이지에서 블로그 포스트 클릭
      const vimPostLink = page.getByRole('link', { name: /Embracing Vim/ });
      await vimPostLink.click();

      // URL 확인
      await expect(page).toHaveURL('/blog/vim');
    });

    test('should navigate to individual blog post from blog page', async ({ page }) => {
      await page.goto('/blog');

      // 블로그 목록 페이지에서 포스트 클릭
      const spacesTabsLink = page.getByRole('link', { name: /Spaces vs\. Tabs/ });
      await spacesTabsLink.click();

      // URL 확인
      await expect(page).toHaveURL('/blog/spaces-vs-tabs');
    });

    test('should display blog post title and date', async ({ page }) => {
      await page.goto('/blog/static-typing');

      // 포스트 제목이 h1으로 표시되는지 확인
      const postTitle = page.getByRole('heading', {
        name: 'The Power of Static Typing in Programming',
        level: 1
      });
      await expect(postTitle).toBeVisible();

      // 게시일 확인
      const publishDate = page.getByText('April 7, 2024');
      await expect(publishDate).toBeVisible();
    });

    test('should display blog post content', async ({ page }) => {
      await page.goto('/blog/static-typing');

      // article 태그가 있는지 확인 (MDX 콘텐츠가 렌더링됨)
      const article = page.locator('article.prose');
      await expect(article).toBeVisible();
    });

    test('should be able to navigate between posts', async ({ page }) => {
      // 첫 번째 포스트로 이동
      await page.goto('/blog/vim');

      // 블로그 링크로 목록으로 돌아가기
      await page.getByRole('link', { name: 'blog' }).click();
      await expect(page).toHaveURL('/blog');

      // 다른 포스트로 이동
      await page.getByRole('link', { name: /Static Typing/ }).click();
      await expect(page).toHaveURL('/blog/static-typing');
    });
  });

  test.describe('통합 시나리오 테스트', () => {
    test('complete user journey: home -> blog list -> blog post -> back to home', async ({ page }) => {
      // 1. 홈페이지 시작
      await page.goto('/');
      await expect(page.getByRole('heading', { name: 'My Portfolio' })).toBeVisible();

      // 2. 블로그 페이지로 이동
      await page.getByRole('link', { name: 'blog' }).click();
      await expect(page).toHaveURL('/blog');
      await expect(page.getByRole('heading', { name: 'My Blog' })).toBeVisible();

      // 3. 개별 포스트로 이동
      await page.getByRole('link', { name: /Embracing Vim/ }).click();
      await expect(page).toHaveURL('/blog/vim');

      // 4. 홈으로 돌아가기
      await page.getByRole('link', { name: 'home' }).click();
      await expect(page).toHaveURL('/');
      await expect(page.getByRole('heading', { name: 'My Portfolio' })).toBeVisible();
    });
  });
});
