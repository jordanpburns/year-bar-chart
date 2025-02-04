window.dccFunctions = window.dccFunctions || {}; 
window.dccFunctions.powerOfTen = function(value) { 
    // return Number.isInteger(10 ** value) ? (10 ** value) : (10 ** value).toFixed(0); 
    return (10 ** value).toFixed(0); 
}