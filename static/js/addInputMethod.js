var counterMethod = 1;
var limitMethod = 20;
        function addInputMethod(divName){
         if (counterMethod == limitMethod)  {
              alert("You have reached the limit of adding " + counterMethod + " inputs");
         }
         else {
              var newdivMethod = document.createElement('div');
              newdivMethod.innerHTML = `Method ${counterMethod + 1} <br><input type="text" name="recipe_${counterMethod + 1}_method">`;
              document.getElementById(divName).appendChild(newdivMethod);
              counterMethod++;
         }
        }