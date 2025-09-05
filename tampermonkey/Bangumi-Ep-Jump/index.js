// ==UserScript==
// @name         Bangumi ep Jump
// @namespace    http://tampermonkey.net/
// @version      1.1.0
// @description  Bangumi 影评底部增加上一章、下一章和回到顶部按钮
// @author       mewhz
// @match        https://bangumi.tv/ep/*
// @icon         https://bangumi.tv/img/favicon.ico
// ==/UserScript==

(function() {
    'use strict';

    const prevBtn = document.createElement('button');
    prevBtn.textContent = '⬅ 上一章节'
    prevBtn.style.cssText = `
    position: fixed;
    right: 283px;
    bottom: 35px;
    padding: 8px 12px;
    font-size: 14px;
    cursor: pointer;
    border: none;
    border-radius: 5px;
    background: #8332d5;
    color: #fff;
    display: none;
    z-index: 9999;
    `;

    const backToTopBtn = document.createElement('button');
    backToTopBtn.textContent = '⬆ 回到顶部';
    backToTopBtn.style.cssText = `
    position: fixed;
    right: 156px;
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

    const nextBtn = document.createElement('button');
    nextBtn.textContent = '➡ 下一章节'
    nextBtn.style.cssText = `
    position: fixed;
    right: 32px;
    bottom: 35px;
    padding: 8px 12px;
    font-size: 14px;
    cursor: pointer;
    border: none;
    border-radius: 5px;
    background: #007bff;
    color: #fff;
    display: none;
    z-index: 9999;
    `;

    const prevLink = document.querySelector('.photoPage .prev');
    const nextLink = document.querySelector('.photoPage .next');
    
    if (prevLink.href == 'javascript:void(0);') prevBtn.style.background = '#e0e0e0';
    if (nextLink.href == 'javascript:void(0);') nextBtn.style.background = '#e0e0e0';

    prevBtn.onclick = () => {
        window.location.href = prevLink.href;
    }

    nextBtn.onclick = () => {
        window.location.href = nextLink.href;
    }

    document.body.appendChild(prevBtn);
    document.body.appendChild(backToTopBtn);
    document.body.appendChild(nextBtn);

    // window.addEventListener('scroll', () => {
    //     if (document.documentElement.scrollTop > 200 || document.body.scrollTop > 200) {
    //         prevBtn.style.display = 'block';
    //         backToTopBtn.style.display = 'block';
    //         nextBtn.style.display = 'block';
    //     } else {
    //         prevBtn.style.display = 'none';
    //         backToTopBtn.style.display = 'none';
    //         nextBtn.style.display = 'none';
    //     }
    // });

    backToTopBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

})();