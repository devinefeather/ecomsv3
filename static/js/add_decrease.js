const valueInput = document.getElementById('quantity-value')
const incrementButton = document.getElementById('add-button')
const decrmentButton = document.getElementById('minus-button') 

incrementButton.addEventListener('click' ,() =>{
    let currentValue = parseInt(valueInput.value);
    valueInput.value = currenValue + 1;
})

decrmentButton.addEventListener('click', () =>{
    let currentValue = parseInt(valueInput.value);
    if (currentValue >0){
        currentValue.value = currentValue-1;
    }
});