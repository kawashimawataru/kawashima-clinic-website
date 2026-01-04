/**
 * 河島医院 Webサイト - メインスクリプト
 * =============================================
 */

document.addEventListener('DOMContentLoaded', function() {
  initMobileMenu();
  initStickyHeader();
  initSmoothScroll();
  initFAQ();
});

/**
 * モバイルメニューの開閉
 */
function initMobileMenu() {
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.nav');
  
  if (!toggle || !nav) return;
  
  toggle.addEventListener('click', function() {
    nav.classList.toggle('active');
    toggle.classList.toggle('active');
    
    // アクセシビリティ対応
    const isOpen = nav.classList.contains('active');
    toggle.setAttribute('aria-expanded', isOpen);
    nav.setAttribute('aria-hidden', !isOpen);
  });
  
  // メニュー外クリックで閉じる
  document.addEventListener('click', function(e) {
    if (!nav.contains(e.target) && !toggle.contains(e.target)) {
      nav.classList.remove('active');
      toggle.classList.remove('active');
    }
  });
  
  // リンククリックで閉じる
  nav.querySelectorAll('a').forEach(function(link) {
    link.addEventListener('click', function() {
      nav.classList.remove('active');
      toggle.classList.remove('active');
    });
  });
}

/**
 * ヘッダーのスティッキー＆スクロール時変化
 */
function initStickyHeader() {
  const header = document.querySelector('.header');
  if (!header) return;
  
  let lastScrollY = 0;
  
  window.addEventListener('scroll', function() {
    const currentScrollY = window.scrollY;
    
    // スクロール位置に応じてクラス付与
    if (currentScrollY > 50) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
    
    lastScrollY = currentScrollY;
  }, { passive: true });
}

/**
 * スムーススクロール
 */
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
    anchor.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href === '#') return;
      
      const target = document.querySelector(href);
      if (!target) return;
      
      e.preventDefault();
      
      const headerHeight = document.querySelector('.header')?.offsetHeight || 0;
      const targetPosition = target.getBoundingClientRect().top + window.scrollY - headerHeight;
      
      window.scrollTo({
        top: targetPosition,
        behavior: 'smooth'
      });
    });
  });
}

/**
 * FAQアコーディオン
 */
function initFAQ() {
  document.querySelectorAll('.faq-question').forEach(function(question) {
    question.addEventListener('click', function() {
      const item = this.closest('.faq-item');
      if (!item) return;
      
      // 他のアイテムを閉じる（シングルオープン）
      document.querySelectorAll('.faq-item').forEach(function(other) {
        if (other !== item) {
          other.classList.remove('active');
        }
      });
      
      // 現在のアイテムをトグル
      item.classList.toggle('active');
    });
  });
}

/**
 * ページ内ナビゲーションのアクティブ状態管理
 */
function updateActiveNav() {
  const path = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach(function(link) {
    const href = link.getAttribute('href');
    if (path.endsWith(href) || (path === '/' && href === 'index.html')) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });
}

// 初期化
updateActiveNav();
