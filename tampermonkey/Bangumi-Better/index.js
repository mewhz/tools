// ==UserScript==
// @name         Bangumi Better
// @namespace    http://tampermonkey.net/
// @version      1.2.0
// @description  Bangumi 影评底部增加快速切换上下章节、返回顶部和标记看过本集
// @author       mewhz
// @match        https://bangumi.tv/ep/*
// @icon         https://bangumi.tv/img/favicon.ico
// ==/UserScript==

(function () {
    'use strict';

    function showCustomAlert(msg) {

        const div = document.createElement("div");
        div.textContent = msg;
        div.style.cssText = `
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            align-items: center;
            background-color: #e6ffed;
            color: #2e7d32;
            border: 1px solid #a5d6a7;
            padding: 10px 20px;
            border-radius: 6px;
            font-size: 14px;
            z-index: 9999;
        `;

        document.body.appendChild(div);

        // 2秒后自动消失
        setTimeout(() => {
            div.remove();
        }, 2000);

    }

    const epId = window.location.href.match(/\d+/)[0];
    const singleList = document.getElementById('badgeUserPanel').getElementsByClassName('single');
    const ghStr = singleList[singleList.length - 1].getElementsByTagName('a')[0].href;
    const gh = ghStr.split('/')[ghStr.split('/').length - 1];

    const buttonDiy = document.createElement('diy');
    buttonDiy.style.cssText = `
        position: fixed;
        right: 32px;
        bottom: 35px;
        gap: 10px;
        cursor: pointer;
        color: #fff;
        display: flex;
        z-index: 9999;
    `;

    const buttonCss = `
        padding: 8px 12px;
        font-size: 20px;
        cursor: pointer;
        border: none;
        color: #f09199;
        background: none;
    `;

    const prevBtn = document.createElement('button');
    // prevBtn.textContent = '⬅ 上一章节'
    prevBtn.textContent = '⬅'
    prevBtn.style.cssText = buttonCss;

    const backToTopBtn = document.createElement('button');
    // backToTopBtn.textContent = '⬆ 回到顶部';
    backToTopBtn.textContent = '⬆';
    backToTopBtn.style.cssText = buttonCss

    const nextBtn = document.createElement('button');
    // nextBtn.textContent = '➡ 下一章节'
    nextBtn.textContent = '➡'
    nextBtn.style.cssText = buttonCss

    const readBtn = document.createElement('button');
    readBtn.textContent = '✔';
    readBtn.style.cssText = buttonCss

    const prevLink = document.querySelector('.photoPage .prev');
    const nextLink = document.querySelector('.photoPage .next');

    if (prevLink.href == 'javascript:void(0);') prevBtn.style.background = '#e0e0e0';
    if (nextLink.href == 'javascript:void(0);') nextBtn.style.background = '#e0e0e0';

    prevBtn.onclick = () => window.location.href = prevLink.href;
    nextBtn.onclick = () => window.location.href = nextLink.href;

    buttonDiy.appendChild(readBtn);
    buttonDiy.appendChild(prevBtn);
    buttonDiy.appendChild(backToTopBtn);
    buttonDiy.appendChild(nextBtn);

    document.body.appendChild(buttonDiy);

    // window.addEventListener('scroll', () => {

    //     if (document.documentElement.scrollTop > 200 || document.body.scrollTop > 200) buttonDiy.style.display = 'flex';
    //     else buttonDiy.style.display = 'none';

    // });

    backToTopBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    readBtn.addEventListener('click', () => {
        fetch(`https://bangumi.tv/subject/ep/${epId}/status/watched?gh=${gh}&ajax=1`, {
            "headers": {
                "accept": "*/*",
                "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,ja;q=0.5",
                "cache-control": "no-cache",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "pragma": "no-cache",
                "sec-ch-ua": "\"Chromium\";v=\"140\", \"Not=A?Brand\";v=\"24\", \"Google Chrome\";v=\"140\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "x-requested-with": "XMLHttpRequest"
            },
            "referrer": "https://bangumi.tv/",
            "body": null,
            "method": "POST",
            "mode": "cors",
            "credentials": "include"
        })
            .then(res => res.json()).then(res => {
                if (res.status == 'ok') {
                    showCustomAlert('观看状态已保存为[看过]');
                } else {
                    showCustomAlert('操作失败');
                }
            });
    })

})();