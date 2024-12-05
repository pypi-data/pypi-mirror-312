// ==UserScript==
// @name         Search on AliDB
// @namespace    http://tampermonkey.net/
// @version      1.1
// @description  try to take over the world!
// @author       yiluohan1234
// @match        https://www.qingjiaoclass.com/*
// @connect      124.70.110.14
// @grant        GM_xmlhttpRequest
// ==/UserScript==

(function() {
    'use strict';

    var container = container || document;
    container.onmouseup = function(event){
        var txt = getSelectText();
        if(txt){
            getAnswer(txt).then(res => {
                console.log(res);
                event.target.innerHTML =event.target.innerHTML.replace(txt, txt+res);
            });
        }
    }

    function getSelectText(){
        var txt = window.getSelection?window.getSelection():document.selection.createRange().text;
        return txt.toString();
    }


    function getAnswer(title) {
        return new Promise(resolve => {
            GM_xmlhttpRequest({
                url: 'http://124.70.110.14:8000/data/',
                method: 'POST',
                headers: {'content-type': 'application/json'},
                data: JSON.stringify({'title': title}),
                dataType: "json",
                async: true,
                onload: function (res) {
                    let json = JSON.parse(res.response);
                    if (json.code === 200) {
                        console.log("request success!\nresult:", json.data)
                        resolve(json.data[0].answer+json.data.length)
                    } else {
                        console.log("request failed!\nmsg:", json.msg)
                    }
                }, onerror: function (err) {
                    console.log("request error", err)
                }
            })
        })
    }
})();