(window.webpackJsonp=window.webpackJsonp||[]).push([[0],{ahb7:function(a,r){!function(){var a={};function r(){return{fromId:$("#from_currency").val(),fromName:$("#from_currency option:selected").text(),toId:$("#to_currency").val(),toName:$("#to_currency option:selected").text(),conversionAmount:$("#conversion-amount").val()}}function c(){var c=r(),o=c.fromId,n=c.fromName,t=c.toId,e=c.toName,l=c.conversionAmount;(isNaN(l)||""==l)&&(l=0);var i=(l=parseFloat(l))*a[o]/a[t];i="__fiat"==t.substring(0,6)?format_fiat(i):format_crypto(i);var u=l+" "+n;$("#conversion-result-left").html(u),$("#conversion-result-value").html(i),$("#conversion-result-value-currency").html(e)}$("#conversion-amount").on("keyup change",c),$("#from_currency,#to_currency").on("change",c),$("#swap-button").on("click",function(){var a=$("#from_currency"),r=$("#to_currency"),o=a.val(),n=r.val();a.val(n).trigger("chosen:updated"),r.val(o).trigger("chosen:updated"),c()}),$(".js-calculator-reset").on("click",function(){$(".js-calculator-field").each(function(a,r){var c=$(r),o=c.attr("id"),n=calculatorDefaults[o]||"";c.val(n).trigger("chosen:updated")}),c()}),$(".js-calculator-permalink").on("click",function(){var a=$(".js-permalink"),c=$(".js-permalink-link"),o=r(),n=[CALCULATOR_HOST+"converter",calculatorOptions[o.fromId],calculatorOptions[o.toId],"?amt="+o.conversionAmount].join("/");c.attr("href",n).html(n),a.removeClass("hide")}),function(){var r=calculatorInitialData["conversion-amount"]||calculatorDefaults["conversion-amount"],o=calculatorInitialData.from_currency||calculatorDefaults.from_currency,n=calculatorInitialData.to_currency||calculatorDefaults.to_currency;$("#conversion-amount").val(r),$("#from_currency").val(o),$("#to_currency").val(n),$(".chosen-select").chosen({search_contains:!0});var t=$("#metadata").data("apidomain");$.ajax({url:t+"/v1/ticker/?limit=0&ref=converter"}).done(function(r){for(i=0;i<r.length;i++)a[r[i].id]=r[i].price_usd;var o=$("#currency-exchange-rates").data();for(currency in o)a["__fiat-"+currency]=o[currency];c(),$("#calculator-loading").addClass("hidden"),$("#calculator").css("visibility","visible")}).fail(function(a){$("#calculator-loading").addClass("hidden"),$("#calculator-nodata").removeClass("hidden")})}()}()}},[["ahb7",1]]]);
//# sourceMappingURL=calculator.fbe9fea7e9.bundle.js.map