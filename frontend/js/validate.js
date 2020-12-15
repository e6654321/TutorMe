function validateForm(){


    var cardNum = document.forms["myForm"]["cardNum"].value.length;
    if (cardNum > 16 || cardNum < 14) {
        alert("Card number must be composed of 16, 15, or 14 digits");
        return false;
    }

    var month = document.forms["myForm"]["month"].value.length;
    if (month != 2) {
        alert("Month must be in this form 'MM'\n Example: '01' (January)");
        return false;
    }

    var year = document.forms["myForm"]["year"].value.length;
    if (year != 2) {
        alert("Year must be in this form 'YY'\n Example: '27' (2027)");
        return false;
    }

    var cvc = document.forms["myForm"]["cvc"].value.length;
    if (cvc != 3) {
        alert("CVV must be a 3 digit number");
        return false;
    }


}