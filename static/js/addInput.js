var counter = 1;
var limit = 20;
    
        function addInput(divName){
         if (counter == limit)  {
              alert("You have reached the limit of adding " + counter + " inputs");
         }
         else {
              var newdiv = document.createElement('div');
              newdiv.innerHTML = `Ingredient ${counter + 1} and amount <br><input type="text" name="ingredient_${counter + 1}_name">`;
              document.getElementById(divName).appendChild(newdiv);
              counter++;
         }
        }
    

        

        
