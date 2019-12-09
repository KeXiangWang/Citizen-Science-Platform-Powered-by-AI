/* ================================================================
*   Copyright (C) 2019 OmniSci. All rights reserved.
*
*   Title：giggle.js
*   Author：Yong Bai
*   Time：2019-04-05 10:09:39
*   Description：
*
* ================================================================*/

//浏览器类型判定
function getOs()
{
  if(navigator.userAgent.indexOf("MSIE")>0) {
     return "IE"; //InternetExplor
  }
  else if(isFirefox=navigator.userAgent.indexOf("Firefox")>0){
     return "FF"; //firefox
  }
  else if(isSafari=navigator.userAgent.indexOf("Safari")>0) {
     return "SF"; //Safari
  }
  else if(isCamino=navigator.userAgent.indexOf("Camino")>0){
     return "C"; //Camino
  }
  else if(isMozilla=navigator.userAgent.indexOf("Gecko/")>0){
     return "G"; //Gecko
  }
  else if(isMozilla=navigator.userAgent.indexOf("Opera")>=0){
     return "O"; //opera
  }else{
    return 'Other';
  }
}

