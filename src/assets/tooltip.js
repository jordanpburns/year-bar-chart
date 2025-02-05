window.dccFunctions = window.dccFunctions || {}; 
function KMB_format (num) {
    if (num >= 1000000000) {
        return (num / 1000000000).toFixed(1) + "B";
    }
    else if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + "M";
    }
    return (num / 1000).toFixed(1) + "K";        
}
window.dccFunctions.powerOfTen = function(value) { 
    return KMB_format((10 ** value)); 
}