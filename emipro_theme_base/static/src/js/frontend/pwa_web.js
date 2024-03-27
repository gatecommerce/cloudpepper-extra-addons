/** @odoo-module **/

var html = document.documentElement;
import { cookie } from "@web/core/browser/cookie";
var website_id = html.getAttribute('data-website-id') | 0;

const isIos = () => {
  const userAgent = window.navigator.userAgent.toLowerCase();
  return /iphone|ipad|ipod/.test( userAgent );
}
// Detects if device is in standalone mode
const isInStandaloneMode = () => ('standalone' in window.navigator) && (window.navigator.standalone);

// Checks if should display install popup notification:

if (isIos() && !isInStandaloneMode()) {
    var iosPrompt = $(".ios-prompt");
    var ios_pwa = cookie.get('ios_pwa');
    var pwa_cache_name = cookie.get('pwa_cache_name');
    var is_pwa_enable = $('.is_pwa').val();
    var pwaHeight = $('.mobile_header_component-style-1').outerHeight();
    var pwaStickyHeight = $('.product_details_sticky').outerHeight();
    if(!ios_pwa && is_pwa_enable) {
        if($('.mobile_header_component-style-1').length) {
            $('.ios-prompt').css({'margin-bottom': '0', 'bottom': pwaHeight});
            if($('.product_details_sticky').length){
                $('.ios-prompt').css({'bottom': pwaHeight+pwaStickyHeight});
            }
        }
        if($('.product_details_sticky').length){
            $('.ios-prompt').css({'margin-bottom': '0', 'bottom': pwaStickyHeight});
        }
        iosPrompt.show();
        $(iosPrompt).click(function() {
            iosPrompt.remove();
            // Create a cookie to hide message in ios
            cookie.set('ios_pwa', '1', 365*60*60*24);
        });
    }
    if(pwa_cache_name) {
        cookie.set('ios_pwa', '1', 365*60*60*24);
    }
}

if ('serviceWorker' in navigator) {
    if(!navigator.onLine){
        var dv_offline = $('.ept_is_offline');
        if(dv_offline){
            dv_offline.show();
        }
    }
    navigator.serviceWorker.register('/service_worker').then(res => {
        console.info('service worker registered : ', res)}
    ).catch(error => {
      console.log('ServiceWorker registration failed: ', error)
    });
}
