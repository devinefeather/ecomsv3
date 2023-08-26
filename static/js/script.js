
const decrementButton = document.querySelector("#minus-button");
const valueInput = document.getElementById('quantity-value');
const incrementButton = document.getElementById('add-button');


document.addEventListener("DOMContentLoaded",()=>{

decrementButton.addEventListener('click', () =>{
    let currentValue = parseInt(valueInput.value);
    if (currentValue > 0){
        valueInput.value = currentValue-1;
    }
});


incrementButton.addEventListener('click' ,() =>{
    let currentValue = parseInt(valueInput.value);
    valueInput.value = currentValue + 1;
});



});

