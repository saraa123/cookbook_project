
// Event Listener for add new ingredient
document.querySelector('#addIngredient').onclick = () => addInput('dynamicInput');
document.querySelector('#addMethod').onclick = () => addInput('dynamicInputMethod'); 


function addInput(divName) {
  
    // count inputs in div
    let numOfInputs;
    console.log(numOfInputs);
  
    // if ingredients button clicked
    if (divName == 'dynamicInput') {
      
        console.log('Ingredients Ran');
        numOfInputs = document.querySelectorAll(`#dynamicInput .ingredient`).length;
        console.log(document.querySelectorAll(`#dynamicInput .ingredient`));
        console.log(numOfInputs);
        
        if (numOfInputs >= 30)  {
            alert("You have reached the limit of adding " + numOfInputs + " inputs");
        }
        else {
        
          let div = document.createElement('div');
              
          let label = document.createElement('label');
          label.innerText = `Ingredient ${numOfInputs + 1} and amount`;
          
          let input = document.createElement('input');
          input.className = 'ingredient';
          input.name = `ingredient_${numOfInputs + 1}_name_added`;
          input.type = 'text';
          
          div.append(label);
          div.append(input);
          
          document.querySelector('#dynamicInput').appendChild(div);
        }
      
    }
    
    // if methods button clicked
    else {
      
        console.log('Methods Ran');
        // input.name = `method_${numOfInputs + 1}_name`;
      
    }
    console.log(numOfInputs);
}   
    
        

        
