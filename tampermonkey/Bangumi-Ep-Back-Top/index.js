// ==UserScript==
// @name         Bangumi ep back top
// @namespace    http://tampermonkey.net/
// @version      1.0.0
// @description  Bangumi 影评添加回到顶部按钮
// @author       mewhz
// @match        https://bangumi.tv/ep/*
// @icon         https://bangumi.tv/img/favicon.ico
// ==/UserScript==

(function() {
    'use strict';
    const backToTopBtn = document.createElement('button');
    backToTopBtn.textContent = '⬆ 回到顶部';
    backToTopBtn.style.cssText = `
    position: fixed;
    right: 30px;
    bottom: 35px;
    padding: 8px 12px;
    font-size: 14px;
    cursor: pointer;
    border: none;
    border-radius: 5px;
    background: #333;
    color: #fff;
    display: none; /* 默认隐藏 */
    z-index: 9999;
    `;

    // 2. 添加到 DOM
    document.body.appendChild(backToTopBtn);

    // 3. 滚动时显示/隐藏按钮
    window.addEventListener('scroll', () => {
        if (document.documentElement.scrollTop > 200 || document.body.scrollTop > 200) {
            backToTopBtn.style.display = 'block';
        } else {
            backToTopBtn.style.display = 'none';
        }
    });

    // 4. 点击回到顶部（平滑）
    backToTopBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

})();